import { useEffect, useMemo, useRef, useState } from 'react'
import { animate } from 'animejs'
import Icon from '../components/Icon'
import { createDocumentChat, getChatMessages, getDocumentChats, getDocumentInsights, sendChatMessage } from '../services/api'

function makeMessage(message) {
  return {
    id: message.id,
    role: message.role,
    text: message.content,
    time: message.created_at ? new Date(message.created_at).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }) : 'Now',
  }
}

function Chat({ activeDocument, documents = [], onSelectDocument, initialPrompt = '', onPromptUsed }) {
  const [messages, setMessages] = useState([])
  const [insights, setInsights] = useState(null)
  const [chatId, setChatId] = useState(null)
  const [value, setValue] = useState('')
  const [query, setQuery] = useState('')
  const [important, setImportant] = useState([])
  const [loading, setLoading] = useState(false)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
  const listRef = useRef(null)
  const documentId = activeDocument?.id
  const visible = useMemo(() => messages.filter((item) => !query || item.text.toLowerCase().includes(query.toLowerCase())), [messages, query])

  useEffect(() => {
    if (!initialPrompt) return
    setValue(initialPrompt)
    onPromptUsed?.()
  }, [initialPrompt, onPromptUsed])

  useEffect(() => {
    let cancelled = false
    setMessages([]); setInsights(null); setChatId(null); setError('')
    if (!documentId) return undefined
    setLoading(true)
    async function loadChat() {
      try {
        const [chats, loadedInsights] = await Promise.all([getDocumentChats(documentId), getDocumentInsights(documentId).catch(() => null)])
        if (cancelled) return
        setInsights(loadedInsights)
        const chat = chats[0]
        // A conversation is created only after the student sends a first message.
        // This keeps a newly selected file calm and free from empty default chats.
        if (!chat) return
        const saved = await getChatMessages(chat.id)
        if (!cancelled) {
          setChatId(chat.id)
          setMessages(saved.map(makeMessage))
        }
      } catch (requestError) {
        if (!cancelled) setError(requestError.message || 'CampusLens could not load this conversation.')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    loadChat()
    return () => { cancelled = true }
  }, [documentId, activeDocument?.title])

  async function send(event) {
    event.preventDefault()
    if (!value.trim() || !documentId || sending) return
    const content = value.trim()
    setSending(true); setError(''); setValue('')
    try {
      let currentChatId = chatId
      if (!currentChatId) {
        const chat = await createDocumentChat(documentId, activeDocument.title || 'Document questions')
        currentChatId = chat.id
        setChatId(currentChatId)
      }
      const result = await sendChatMessage(currentChatId, content)
      const assistant = makeMessage(result.assistant_message)
      const firstSource = result.sources?.[0]
      if (firstSource?.page_number || firstSource?.page) assistant.source = 'Source · Page ' + (firstSource.page_number || firstSource.page)
      setMessages((items) => [...items, makeMessage(result.user_message), assistant])
      requestAnimationFrame(() => listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' }))
    } catch (requestError) {
      setValue(content)
      setError(requestError.message || 'CampusLens could not answer that question.')
    } finally {
      setSending(false)
    }
  }
  function toggleImportant(message, target) {
    setImportant((items) => items.some((item) => item.id === message.id) ? items.filter((item) => item.id !== message.id) : [...items, { ...message, savedAt: new Date().toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) }])
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) animate(target, { scale: [1, 1.18, 1], duration: 260, ease: 'outExpo' })
  }
  function showText(text) {
    if (!query) return text
    const escaped = query.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')
    return text.split(new RegExp(`(${escaped})`, 'ig')).map((part, index) => part.toLowerCase() === query.toLowerCase() ? <mark key={index} className="rounded bg-[#d7f46d]/60 px-0.5 text-[#19311e]">{part}</mark> : part)
  }

  const title = activeDocument?.title || 'No document selected'
  const summary = insights?.summary || activeDocument?.summary || 'Select a processed document to see its generated summary, deadlines, and actions.'
  return <div className="dashboard-light min-h-screen px-5 py-8 sm:px-8 lg:h-dvh lg:min-h-0 lg:overflow-hidden lg:px-10 lg:py-10"><div className="mx-auto grid max-w-6xl gap-5 xl:h-full xl:min-h-0 xl:grid-cols-[.72fr_1.28fr]">
    <aside className="dashboard-side-card rounded-[28px] p-5 sm:p-6 xl:overflow-y-auto">
      <div className="border-b border-[#c4d3ad] pb-5"><div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-[.14em] text-[#5c7c45]">Your files</p><h2 className="display-font mt-1 text-xl font-bold text-[#1d422a]">Document space</h2></div><span className="rounded-full bg-[#dce8c4] px-2 py-1 text-[10px] font-bold text-[#315235]">{documents.length}</span></div><div className="mt-3 max-h-44 space-y-2 overflow-y-auto pr-1">{documents.length ? documents.map((document) => <button key={document.id} onClick={() => onSelectDocument?.(document)} className={`flex w-full items-center gap-3 rounded-xl border p-3 text-left transition ${document.id === documentId ? 'border-[#789c57] bg-[#e5efd3]' : 'border-transparent bg-[#f7f5e9] hover:border-[#bdcfaa]'}`}><span className="grid size-8 shrink-0 place-items-center rounded-lg bg-[#dce8c4] text-[#315235]"><Icon name="file" className="size-4" /></span><span className="min-w-0"><span className="block truncate text-sm font-bold text-[#29452f]">{document.title}</span><span className="block text-[11px] text-[#71806b]">{document.status === 'Ready' ? 'Ready to chat' : document.status}</span></span></button>) : <p className="rounded-xl border border-dashed border-[#bdcfaa] bg-[#f8f8ef] p-3 text-sm leading-5 text-[#647765]">Upload a file from My documents to start a focused conversation.</p>}</div></div>
      <div className="flex items-center gap-3"><span className="grid size-11 place-items-center rounded-2xl bg-[#dce8c4] text-[#315235]"><Icon name="file" className="size-5" /></span><div className="min-w-0"><p className="text-xs font-bold uppercase tracking-[.14em] text-[#5c7c45]">Selected document</p><h1 className="display-font truncate text-lg font-bold text-[#1d422a]">{title}</h1></div></div>
      <div className="mt-5 rounded-2xl border border-[#c4d3ad] bg-[#f7f5e9] p-4"><p className="text-xs font-bold uppercase tracking-[.13em] text-[#597640]">Document summary</p><p className="mt-2 text-sm leading-6 text-[#536c59]">{summary}</p>{insights?.deadlines?.length > 0 && <p className="mt-3 text-xs font-semibold text-[#597640]">{insights.deadlines.length} extracted deadline{insights.deadlines.length === 1 ? '' : 's'} available</p>}</div>
      <div className="mt-7"><div className="flex items-center justify-between"><h2 className="display-font text-xl font-bold text-[#1d422a]">Important chats</h2><span className="rounded-full bg-[#dce8c4] px-2 py-1 text-[10px] font-bold text-[#315235]">{important.length}</span></div>{important.length ? <div className="mt-3 space-y-2">{important.map((item) => <div key={item.id} className="rounded-xl border border-[#c8d7b4] bg-[#f8f8ef] p-3"><div className="flex gap-2"><Icon name="bookmark" className="mt-0.5 size-4 shrink-0 text-[#a65e45]" /><p className="line-clamp-2 text-sm font-medium leading-5 text-[#334d38]">{item.text}</p></div><p className="mt-2 text-[11px] text-[#71806b]">Saved {item.savedAt}</p></div>)}</div> : <div className="mt-3 rounded-xl border border-dashed border-[#bdcfaa] bg-[#f8f8ef] p-4 text-sm leading-6 text-[#647765]">Save a useful answer with the bookmark to find it here later.</div>}</div>
    </aside>
    <section className="flex min-h-[620px] flex-col overflow-hidden rounded-[28px] border border-[#b7cba0] bg-[#f9f7eb] shadow-[0_18px_42px_rgba(29,54,31,.12)] xl:h-full xl:min-h-0">
      <header className="flex flex-col gap-4 border-b border-[#c8d6b8] px-5 py-4 sm:flex-row sm:items-center sm:justify-between"><div><p className="text-xs font-bold uppercase tracking-[.15em] text-[#5c7c45]">Campus assistant</p><h2 className="display-font mt-1 text-xl font-bold text-[#1d422a]">Ask about this file</h2></div><label className="relative block"><span className="sr-only">Search conversation</span><Icon name="search" className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-[#667c69]" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search chat" className="w-full rounded-xl border border-[#b8cba7] bg-white py-2 pl-9 pr-8 text-sm text-[#28432e] outline-none placeholder:text-[#829182] focus:border-[#789c57] sm:w-52" />{query && <button onClick={() => setQuery('')} className="absolute right-2 top-1/2 -translate-y-1/2 text-[#5c745d]" aria-label="Clear search"><Icon name="close" className="size-4" /></button>}</label></header>
      <div ref={listRef} className="min-h-0 flex-1 space-y-5 overflow-y-auto overscroll-contain p-5 sm:p-7">{loading && <p className="text-sm text-[#657d66]">Loading document conversation…</p>}{error && <p className="rounded-xl border border-[#e9b09c] bg-[#fff0e9] p-3 text-sm text-[#9b4e3b]">{error}</p>}{query && <p className="text-xs font-semibold text-[#657d66]">{visible.length} matching {visible.length === 1 ? 'message' : 'messages'}</p>}{visible.map((message) => { const saved = important.some((item) => item.id === message.id); return <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}><div className={`max-w-[86%] rounded-2xl px-4 py-3 text-sm leading-6 ${message.role === 'user' ? 'rounded-br-sm bg-[#d7f46d] text-[#20301e]' : 'rounded-bl-sm border border-[#c2d1b5] bg-white text-[#35523b]'}`}><div className="flex items-start gap-3"><p className="flex-1">{showText(message.text)}</p><button onClick={(event) => toggleImportant(message, event.currentTarget)} className={`grid size-7 shrink-0 place-items-center rounded-lg transition ${saved ? 'bg-[#f3d5a9] text-[#8e4c35]' : 'text-[#799076] hover:bg-[#e6eed9]'}`} aria-label={saved ? 'Remove from important chats' : 'Mark message important'}><Icon name="bookmark" className="size-4" /></button></div>{message.source && <p className="mt-2 border-t border-[#d7e1cf] pt-2 text-xs font-bold text-[#557b42]">{message.source}</p>}<p className="mt-1 text-[10px] text-[#829182]">{message.time}</p></div></div> })}{!loading && !error && !visible.length && <div className="grid min-h-48 place-items-center rounded-2xl border border-dashed border-[#bdcfaa] text-center text-sm text-[#687b69]">{query ? 'No messages match “' + query + '”.' : documentId ? 'Ask a question to begin this document conversation.' : 'Choose a file from your document space to begin.'}</div>}</div>
      <form onSubmit={send} className="border-t border-[#c8d6b8] bg-[#f2f5e7] p-4"><div className="flex items-center gap-2 rounded-2xl border border-[#b7cba0] bg-white p-2 pl-4"><input disabled={!documentId || sending} value={value} onChange={(event) => setValue(event.target.value)} placeholder={documentId ? 'Ask about this document...' : 'Choose a file to begin'} className="min-w-0 flex-1 bg-transparent py-2 text-sm text-[#29452f] outline-none placeholder:text-[#879687] disabled:cursor-not-allowed" /><button disabled={!documentId || sending || !value.trim()} className="grid size-10 place-items-center rounded-xl bg-[#285137] text-[#fbf8e9] transition hover:opacity-90 disabled:cursor-wait disabled:opacity-50" aria-label="Send message"><Icon name="send" className="size-5" /></button></div><p className="mt-2 text-center text-[10px] text-[#71806b]">{sending ? 'CampusLens is preparing a source-aware answer…' : 'Answers use the selected document and its saved conversation.'}</p></form>
    </section>
  </div></div>
}
export default Chat
