import { useEffect, useRef, useState } from 'react'
import { animate, stagger } from 'animejs'
import DoodleAccent from '../components/DoodleAccent'
import Icon from '../components/Icon'
import UploadCard from '../components/UploadCard'

const colorStyles = { lime: 'bg-[#d7f46d] text-[#1f2c1e]', sand: 'bg-[#f2dfb7] text-[#563d1e]', coral: 'bg-[#eaa17e] text-[#43261e]' }
function Documents({ documents, onUpload, onOpenChat, onDelete, isUploading, error }) {
  const [filter, setFilter] = useState('All')
  const [deletingId, setDeletingId] = useState(null)
  const [documentToDelete, setDocumentToDelete] = useState(null)
  const gridRef = useRef(null)
  const visible = filter === 'All' ? documents : documents.filter(doc => doc.status === filter)
  useEffect(() => {
    if (!gridRef.current) return undefined
    const animation = animate(gridRef.current.children, { opacity: [0, 1], scale: [.94, 1], translateY: [28, 0], delay: stagger(105), duration: 650, ease: 'outExpo' })
    return () => animation.revert()
  }, [filter, documents.length])
  async function remove() {
    const document = documentToDelete
    if (!document) return
    setDeletingId(document.id)
    try { await onDelete(document); setDocumentToDelete(null) } finally { setDeletingId(null) }
  }
  return <div className="paper-texture min-h-screen px-5 py-8 sm:px-8 lg:px-10 lg:py-10"><div className="mx-auto max-w-6xl"><div className="relative"><DoodleAccent type="arrow" className="absolute -right-4 -top-8 w-20 text-[#f2b693]" /><p className="text-sm font-bold uppercase tracking-[.15em] text-[#d7f46d]">Your study shelf</p><h1 className="display-font mt-1 text-4xl font-bold tracking-[-.06em] text-[#f8f1dc] sm:text-5xl">My documents</h1><p className="mt-3 max-w-xl text-sm leading-6 text-[#bec8b6]">Keep every circular, syllabus and opportunity in one calm, easy-to-search place.</p></div>
    <div className="mt-7"><UploadCard onUpload={onUpload} isUploading={isUploading} compact /></div>
    {error && <p className="mt-4 rounded-xl border border-[#eaa17e] bg-[#43261e]/40 px-4 py-3 text-sm text-[#f2dfb7]">{error}</p>}
    <div className="mt-8 flex flex-wrap items-center justify-between gap-3"><p className="text-sm text-[#c4cdbd]"><span className="font-bold text-[#f8f1dc]">{documents.length}</span> documents in your shelf</p><div className="flex gap-2">{['All', 'Ready', 'Processing'].map(item => <button key={item} onClick={() => setFilter(item)} className={`rounded-full px-3 py-1.5 text-xs font-bold ${filter === item ? 'bg-[#d7f46d] text-[#1e291d]' : 'border border-[#53644f] text-[#c4cdbd]'}`}>{item}</button>)}</div></div>
    <div ref={gridRef} className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">{visible.map(doc => <article key={doc.id} className="group rounded-[25px] border border-[#455740] bg-[#243024] p-5 transition hover:-translate-y-1 hover:border-[#91ac5e]"><div className="flex items-start justify-between"><span className={`grid size-12 place-items-center rounded-2xl ${colorStyles[doc.color]}`}><Icon name="file" className="size-6" /></span><button onClick={() => setDocumentToDelete(doc)} disabled={deletingId === doc.id} className="rounded-lg px-2 py-1 text-xs font-bold text-[#f2b693] transition hover:bg-[#43261e] disabled:cursor-wait disabled:opacity-60" aria-label={`Delete ${doc.title}`}>{deletingId === doc.id ? 'Deleting…' : 'Delete'}</button></div><div className="mt-6"><span className="text-[10px] font-extrabold uppercase tracking-[.13em] text-[#d7f46d]">{doc.type}</span><h2 className="display-font mt-2 text-xl font-bold leading-6 tracking-[-.04em] text-[#f7f0dc]">{doc.title}</h2><p className="mt-2 text-sm leading-5 text-[#aebaa7]">{doc.summary}</p></div><div className="mt-5 flex items-center justify-between border-t border-[#40503d] pt-4 text-xs text-[#aebaa7]"><span>{doc.pages} pages · {doc.date}</span><span className={doc.status === 'Ready' ? 'text-[#d7f46d]' : 'text-[#f2dfb7]'}>{doc.status}</span></div><button onClick={() => onOpenChat(doc)} className="mt-4 inline-flex items-center gap-2 text-sm font-bold text-[#d7f46d]">Open assistant <Icon name="arrow" className="size-4 transition group-hover:translate-x-1" /></button></article>)}</div>
    {documentToDelete && <div className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-5 backdrop-blur-sm" role="dialog" aria-modal="true" aria-labelledby="delete-title"><div className="w-full max-w-sm rounded-[28px] border border-[#765246] bg-[#243024] p-6 shadow-2xl"><span className="grid size-11 place-items-center rounded-2xl bg-[#f2b693] text-[#4e2e23]"><Icon name="close" className="size-5" /></span><h2 id="delete-title" className="display-font mt-5 text-2xl font-bold text-[#f8f1dc]">Delete this file?</h2><p className="mt-2 text-sm leading-6 text-[#c9d2c3]">“{documentToDelete.title}” and its saved conversation will be permanently removed.</p><div className="mt-6 flex justify-end gap-3"><button onClick={() => setDocumentToDelete(null)} disabled={Boolean(deletingId)} className="rounded-xl px-4 py-2.5 text-sm font-bold text-[#d7e3d1] hover:bg-white/10">Cancel</button><button onClick={remove} disabled={Boolean(deletingId)} className="rounded-xl bg-[#eaa17e] px-4 py-2.5 text-sm font-bold text-[#40251c] disabled:opacity-60">{deletingId ? 'Deleting…' : 'Delete file'}</button></div></div></div>}
  </div></div>
}
export default Documents
