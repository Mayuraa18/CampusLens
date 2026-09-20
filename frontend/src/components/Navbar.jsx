import Brand from './Brand'
import Icon from './Icon'
import { useEffect, useRef, useState } from 'react'
import { animate } from 'animejs'

function Navbar({ onSignIn, onGetStarted }) {
  const navRef = useRef(null)
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    if (!navRef.current) return undefined
    const animation = animate(navRef.current, { opacity: [0, 1], translateY: [-16, 0], duration: 700, ease: 'outExpo' })
    return () => animation.revert()
  }, [])

  const closeMenu = () => setIsOpen(false)

  return (
    <header ref={navRef} className="fixed inset-x-0 top-0 z-30 mx-auto px-5 pt-3 sm:px-8 lg:px-10">
      <div className="relative mx-auto flex max-w-7xl items-center justify-between rounded-xl border border-[#dcebc6]/20 bg-[#0c2215]/82 px-4 py-2 shadow-[0_8px_24px_rgba(0,0,0,.18)] backdrop-blur-md sm:px-5">
        <Brand animated wordmarkFont />
        <nav className="hidden items-center gap-7 text-sm font-semibold text-[#e3eadc] md:flex" aria-label="Main navigation">
          <a href="#features" className="transition hover:text-[#d7f46d]">Features</a>
          <a href="#how-it-works" className="transition hover:text-[#d7f46d]">How It Works</a>
        </nav>
        <div className="hidden items-center gap-3 md:flex">
          <button onClick={onSignIn} className="px-2 py-2 text-sm font-bold text-[#f8f1dc] transition hover:text-[#d7f46d]">Login</button>
          <button onClick={onGetStarted} className="rounded-lg bg-[#d7f46d] px-4 py-2 text-sm font-extrabold text-[#1b291b] transition hover:bg-[#edffad]">Get Started</button>
        </div>
        <button onClick={() => setIsOpen(open => !open)} className="grid size-10 place-items-center rounded-xl border border-[#61755a] text-[#f8f1dc] md:hidden" aria-label="Open navigation menu" aria-expanded={isOpen}><Icon name={isOpen ? 'close' : 'menu'} className="size-5" /></button>
        {isOpen && <nav className="absolute inset-x-0 top-[calc(100%+8px)] rounded-2xl border border-[#52684c] bg-[#11281a]/98 p-3 shadow-xl backdrop-blur md:hidden" aria-label="Mobile navigation">
          <a onClick={closeMenu} href="#features" className="block rounded-xl px-3 py-3 text-sm font-bold text-[#e3eadc] hover:bg-[#243d27]">Features</a>
          <a onClick={closeMenu} href="#how-it-works" className="block rounded-xl px-3 py-3 text-sm font-bold text-[#e3eadc] hover:bg-[#243d27]">How It Works</a>
          <button onClick={() => { closeMenu(); onSignIn() }} className="mt-1 w-full rounded-xl border border-[#5c7356] px-3 py-3 text-left text-sm font-bold text-[#f8f1dc]">Login</button>
          <button onClick={() => { closeMenu(); onGetStarted() }} className="mt-2 w-full rounded-xl bg-[#d7f46d] px-3 py-3 text-sm font-extrabold text-[#1b291b]">Get Started</button>
        </nav>}
      </div>
    </header>
  )
}

export default Navbar
