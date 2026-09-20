import { useEffect, useState } from 'react'
import AppShell from './components/AppShell'
import AuthModal from './components/AuthModal'
import Chat from './pages/Chat'
import Dashboard from './pages/Dashboard'
import Documents from './pages/Documents'
import Home from './pages/Home'
import Kanban from './pages/Kanban'
import Profile from './pages/Profile'
import { clearSession, deleteDocument as deleteFromBackend, getAccessToken, getCurrentUser, getDocuments, uploadDocument as uploadToBackend } from './services/api'

const colors = ['lime', 'sand', 'coral']
function displayDocument(document, index = 0) {
  return {
    ...document,
    type: 'Campus PDF',
    date: new Date(document.uploaded_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }),
    pages: 'PDF',
    color: colors[index % colors.length],
    status: document.status === 'processed' ? 'Ready' : document.status === 'failed' ? 'Failed' : 'Processing',
    summary: document.status === 'processed' ? 'This document is ready for CampusLens analysis.' : 'Your document is safely stored and awaiting analysis.',
  }
}

function App() {
  const [page, setPage] = useState(getAccessToken() ? 'dashboard' : 'home')
  const [authMode, setAuthMode] = useState(null)
  const [documents, setDocuments] = useState([])
  const [activeDocument, setActiveDocument] = useState(null)
  const [user, setUser] = useState(null)
  const [documentError, setDocumentError] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [chatPrompt, setChatPrompt] = useState('')
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('campuslens-theme')
    return savedTheme === 'violet' ? 'lime' : savedTheme || 'lime'
  })

  function changeTheme(nextTheme) {
    setTheme(nextTheme)
    localStorage.setItem('campuslens-theme', nextTheme)
  }

  async function loadAccount() {
    const [account, savedDocuments] = await Promise.all([getCurrentUser(), getDocuments()])
    const formattedDocuments = savedDocuments.map(displayDocument)
    setUser(account)
    setDocuments(formattedDocuments)
    setActiveDocument(current => current || formattedDocuments[0] || null)
  }

  useEffect(() => {
    if (!getAccessToken()) return
    loadAccount().catch(() => {
      clearSession()
      setPage('home')
    })
  }, [])

  useEffect(() => {
    function handleSessionExpired() {
      setUser(null)
      setDocuments([])
      setActiveDocument(null)
      setPage('home')
      setAuthMode('login')
    }
    window.addEventListener('campuslens:session-expired', handleSessionExpired)
    return () => window.removeEventListener('campuslens:session-expired', handleSessionExpired)
  }, [])

  async function uploadDocument(file, { stayOnDashboard = false } = {}) {
    setDocumentError('')
    setIsUploading(true)
    try {
      const document = displayDocument(await uploadToBackend(file))
      setDocuments(items => [document, ...items])
      setActiveDocument(document)
      if (!stayOnDashboard) setPage('documents')
      return document
    } catch (error) {
      setDocumentError(error.message)
      throw error
    } finally {
      setIsUploading(false)
    }
  }

  function openChat(document, prompt = '') {
    setActiveDocument(document)
    setChatPrompt(prompt)
    setPage('chat')
  }

  async function removeDocument(document) {
    setDocumentError('')
    try {
      await deleteFromBackend(document.id)
      setDocuments(items => items.filter(item => item.id !== document.id))
      setActiveDocument(current => current?.id === document.id ? null : current)
    } catch (error) {
      setDocumentError(error.message)
      throw error
    }
  }

  const content = page === 'dashboard'
    ? <Dashboard onUpload={(file) => uploadDocument(file, { stayOnDashboard: true })} isUploading={isUploading} onNavigate={setPage} user={user} documents={documents} documentCount={documents.length} />
    : page === 'documents'
      ? <Documents documents={documents} onUpload={uploadDocument} onDelete={removeDocument} isUploading={isUploading} error={documentError} onOpenChat={openChat} />
    : page === 'profile'
      ? <Profile user={user} theme={theme} onThemeChange={changeTheme} />
      : page === 'kanban'
        ? <Kanban documents={documents} onAskAi={openChat} />
        : <Chat activeDocument={activeDocument} documents={documents} onSelectDocument={setActiveDocument} initialPrompt={chatPrompt} onPromptUsed={() => setChatPrompt('')} />

  return <>
    {page === 'home'
      ? <Home onSignIn={() => setAuthMode('login')} onGetStarted={() => setAuthMode('register')} />
      : <AppShell page={page} theme={theme} onNavigate={setPage} onSignOut={() => { clearSession(); setUser(null); setDocuments([]); setActiveDocument(null); setChatPrompt(''); setPage('home') }}>{content}</AppShell>}
    {authMode && <AuthModal initialMode={authMode} onClose={() => setAuthMode(null)} onSuccess={(account) => { setUser(account); setAuthMode(null); setPage('dashboard'); loadAccount().catch(error => setDocumentError(error.message)) }} />}
  </>
}

export default App
