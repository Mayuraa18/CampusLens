import Brand from './Brand'
import Icon from './Icon'
import { cloneElement, isValidElement, useEffect, useRef, useState } from 'react'
import { animate } from 'animejs'

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: 'home' },
  { id: 'documents', label: 'My documents', icon: 'document' },
  { id: 'chat', label: 'Campus chat', icon: 'chat' },
  { id: 'kanban', label: 'Kanban board', icon: 'calendar' },
  { id: 'profile', label: 'My profile', icon: 'user' },
]

function AppShell({ page, onNavigate, onSignOut, children, theme = 'lime' }) {
  const contentRef = useRef(null)
  const navigationLock = useRef(false)
  const [logoutOpen, setLogoutOpen] = useState(false)

  useEffect(() => {
    if (!contentRef.current) return undefined
    const animation = animate(contentRef.current, { opacity: [0, 1], scale: [.86, 1], translateY: [18, 0], duration: 720, ease: 'outExpo' })
    return () => animation.revert()
  }, [page])

  function navigate(target) {
    if (target === page || navigationLock.current) return
    navigationLock.current = true
    const exitAnimation = contentRef.current && animate(contentRef.current, { opacity: [1, 0], scale: [1, .82], translateY: [0, -18], duration: 360, ease: 'inOutQuint' })
    window.setTimeout(() => {
      window.scrollTo(0, 0)
      onNavigate(target)
    }, 360)
    window.setTimeout(() => { navigationLock.current = false }, 820)
    return exitAnimation
  }

  function confirmSignOut() {
    setLogoutOpen(false)
    onSignOut()
  }

  const content = isValidElement(children) ? cloneElement(children, { onNavigate: navigate }) : children
  return (
    <main data-campus-theme={theme} className="authenticated-shell min-h-screen bg-[#102319] text-white">
      <header className="sticky top-0 z-30 flex h-[70px] items-center justify-between border-b border-[#40503c] bg-[#102319]/95 px-5 backdrop-blur lg:hidden"><Brand /><button onClick={() => setLogoutOpen(true)} className="text-sm font-bold text-[#d7f46d]">Log out</button></header>
      <aside className="paper-texture fixed inset-y-0 left-0 z-30 hidden w-64 border-r border-[#40503c] bg-[#132b1c] p-5 lg:flex lg:flex-col">
        <Brand />
        <nav className="mt-11 space-y-2">{navItems.map((item) => <button key={item.id} onClick={() => navigate(item.id)} className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-bold transition ${page === item.id ? 'bg-[#d7f46d] text-[#1b291b] shadow-[3px_3px_0_#f2b693]' : 'text-[#c3ccb9] hover:bg-[#2b382a] hover:text-white'}`}><Icon name={item.icon} className="size-5" />{item.label}</button>)}</nav>
        <div className="paper-texture mt-auto rounded-2xl border border-[#50624c] bg-[#293629] p-4"><p className="text-xs font-bold uppercase tracking-wider text-[#d7f46d]">Study smart</p><p className="mt-2 text-sm leading-5 text-[#d9e0d2]">Your next important deadline could be one document away.</p><Icon name="book" className="mt-3 size-5 text-[#f2b693]" /></div>
        <button onClick={() => setLogoutOpen(true)} className="mt-5 flex items-center gap-2 px-3 py-2 text-sm font-bold text-[#bbc6b4] hover:text-[#f8f1dc]"><Icon name="user" className="size-4" />Log out</button>
      </aside>
      <div ref={contentRef} className="pb-20 lg:pl-64">{content}</div>
      <nav className="fixed inset-x-3 bottom-3 z-30 flex justify-around rounded-2xl border border-[#52634d] bg-[#223022]/95 p-2 shadow-xl backdrop-blur lg:hidden">{navItems.map((item) => <button key={item.id} onClick={() => navigate(item.id)} className={`grid place-items-center gap-1 rounded-xl px-4 py-2 text-[10px] font-bold ${page === item.id ? 'bg-[#d7f46d] text-[#1e291d]' : 'text-[#c1cbb9]'}`}><Icon name={item.icon} className="size-5" />{item.label}</button>)}</nav>
      {logoutOpen && <div className="fixed inset-0 z-50 grid place-items-center bg-[#071009]/70 p-5 backdrop-blur-sm" role="dialog" aria-modal="true" aria-labelledby="logout-title"><div className="w-full max-w-sm rounded-[28px] border border-[#6c8466] bg-[#17301e] p-6 shadow-2xl"><div className="grid size-11 place-items-center rounded-2xl bg-[#f2b693] text-[#40291f]"><Icon name="user" className="size-5" /></div><h2 id="logout-title" className="display-font mt-5 text-2xl font-bold text-[#f8f1dc]">Log out of CampusLens?</h2><p className="mt-2 text-sm leading-6 text-[#c7d2c2]">Your work is saved. You will need to sign in again to return to your study space.</p><div className="mt-6 flex justify-end gap-3"><button onClick={() => setLogoutOpen(false)} className="rounded-xl px-4 py-2.5 text-sm font-bold text-[#d7e3d1] hover:bg-white/10">Stay signed in</button><button onClick={confirmSignOut} className="rounded-xl bg-[#d7f46d] px-4 py-2.5 text-sm font-bold text-[#17301e]">Log out</button></div></div></div>}
    </main>
  )
}

export default AppShell
