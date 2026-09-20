// In development, /api is proxied by Vite to the new CampusLens backend.
// Set VITE_API_BASE_URL for a deployed API (for example, https://api.example.com/api).
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '')
const ACCESS_TOKEN_KEY = 'campuslens.accessToken'
const REFRESH_TOKEN_KEY = 'campuslens.refreshToken'
let refreshInFlight = null

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function clearSession() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

function notifySessionExpired() {
  window.dispatchEvent(new CustomEvent('campuslens:session-expired'))
}

function messageFrom(payload, fallback) {
  if (!payload || typeof payload !== 'object') return fallback
  if (typeof payload.detail === 'string') return payload.detail
  const [field, errors] = Object.entries(payload)[0] || []
  if (Array.isArray(errors) && errors[0]) return `${field}: ${errors[0]}`
  return fallback
}

async function refreshAccessToken() {
  const refresh = localStorage.getItem(REFRESH_TOKEN_KEY)
  if (!refresh) throw new Error('Your session has expired. Please sign in again.')
  if (!refreshInFlight) {
    refreshInFlight = fetch(`${API_BASE_URL}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    }).then(async (response) => {
      const payload = await response.json().catch(() => null)
      if (!response.ok || !payload?.access) throw new Error(messageFrom(payload, 'Your session has expired. Please sign in again.'))
      localStorage.setItem(ACCESS_TOKEN_KEY, payload.access)
      return payload.access
    }).finally(() => { refreshInFlight = null })
  }
  return refreshInFlight
}

async function request(path, options = {}, retryAfterRefresh = true) {
  const headers = new Headers(options.headers)
  const token = getAccessToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers })
  if (response.status === 204) return null

  const payload = await response.json().catch(() => null)
  if (!response.ok) {
    if (response.status === 401 && token && retryAfterRefresh && path !== '/auth/token/refresh/') {
      try {
        await refreshAccessToken()
        return request(path, options, false)
      } catch (refreshError) {
        clearSession()
        notifySessionExpired()
        throw refreshError
      }
    }
    throw new Error(messageFrom(payload, 'CampusLens could not complete that request.'))
  }
  return payload
}

export async function checkBackendConnection() {
  return request('/health/')
}

export async function signIn(username, password) {
  const session = await request('/auth/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  localStorage.setItem(ACCESS_TOKEN_KEY, session.access)
  localStorage.setItem(REFRESH_TOKEN_KEY, session.refresh)
  return getCurrentUser()
}

export async function register({ username, email, password }) {
  return request('/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  })
}

export function getCurrentUser() {
  return request('/auth/me/')
}

export function getDocuments() {
  return request('/documents/')
}

export function uploadDocument(file) {
  const body = new FormData()
  body.append('title', file.name.replace(/\.pdf$/i, ''))
  body.append('file', file)
  return request('/documents/', { method: 'POST', body })
}

export function deleteDocument(id) {
  return request(`/documents/${id}/`, { method: 'DELETE' })
}

export function getDocument(id) {
  return request(`/documents/${id}/`)
}

export function getDocumentInsights(id) {
  return request(`/documents/${id}/insights/`)
}

export function getDocumentChats(documentId) {
  return request(`/documents/${documentId}/chats/`)
}

export function createDocumentChat(documentId, title = 'New Chat') {
  return request(`/documents/${documentId}/chats/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  })
}

export function getChat(id) {
  return request(`/chats/${id}/`)
}

export function deleteChat(id) {
  return request(`/chats/${id}/`, { method: 'DELETE' })
}

export function getChatMessages(id) {
  return request(`/chats/${id}/messages/`)
}

export function sendChatMessage(id, content) {
  return request(`/chats/${id}/messages/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content }),
  })
}
