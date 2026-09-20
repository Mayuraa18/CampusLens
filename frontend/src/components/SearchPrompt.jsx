import { useEffect, useRef, useState } from 'react'
import { animate, stagger } from 'animejs'
import Icon from './Icon'
import { checkBackendConnection } from '../services/api'

function SearchPrompt({ prompts }) {
  const [value, setValue] = useState('')
  const [status, setStatus] = useState(null)
  const formRef = useRef(null)
  const promptsRef = useRef(null)

  useEffect(() => {
    const animations = []
    if (formRef.current) animations.push(animate(formRef.current, { opacity: [0, 1], translateY: [16, 0], duration: 700, ease: 'outExpo' }))
    if (promptsRef.current) animations.push(animate(promptsRef.current.children, { opacity: [0, 1], translateY: [10, 0], delay: stagger(80), duration: 450, ease: 'outExpo' }))
    return () => animations.forEach(animation => animation.revert())
  }, [])

  const submit = async (event) => {
    event.preventDefault()
    if (!value.trim()) return

    setStatus('checking')
    try {
      await checkBackendConnection()
      setStatus('connected')
    } catch {
      setStatus('unavailable')
    }
  }
  return (
    <div className="w-full max-w-2xl">
      <form ref={formRef} onSubmit={submit} className="flex items-center gap-2 rounded-[22px] border border-[#62725b] bg-[#263125]/90 p-2 pl-4 shadow-[0_12px_30px_rgba(0,0,0,.18)]">
        <Icon name="search" className="size-5 shrink-0 text-[#b7c5ad]" />
        <input value={value} onChange={(event) => { setValue(event.target.value); setStatus(null) }} aria-label="Ask CampusLens" placeholder="Ask anything about your campus..." className="min-w-0 flex-1 bg-transparent py-2 text-sm text-white outline-none placeholder:text-[#aeb8a5] sm:text-base" />
        <button className="grid size-10 shrink-0 place-items-center rounded-2xl bg-[#d7f46d] text-[#1e291e] transition hover:scale-105" aria-label="Send question"><Icon name="arrow" className="size-5" /></button>
      </form>
      {status === 'checking' && <p className="mt-2 text-center text-xs text-[#c8d0be]">Connecting to CampusLens…</p>}
      {status === 'connected' && <p className="mt-2 text-center text-xs text-[#d7f46d]">CampusLens service is online. Sign in to access your document shelf.</p>}
      {status === 'unavailable' && <p className="mt-2 text-center text-xs text-[#f2b693]">Backend is not running yet. Start Django, then try again.</p>}
      <div ref={promptsRef} className="mt-4 flex flex-wrap justify-center gap-2">
        {prompts.map((prompt) => <button key={prompt} onClick={() => { setValue(prompt); setStatus(null) }} className="rounded-full border border-[#53624e] px-3 py-1.5 text-xs text-[#d9dfd1] transition hover:border-[#d7f46d] hover:bg-[#2b382a]">{prompt}</button>)}
      </div>
    </div>
  )
}

export default SearchPrompt
