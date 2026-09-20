import { useEffect, useRef } from 'react'
import { animate } from 'animejs'

function Brand({ animated = false, wordmarkFont = false }) {
  const iconRef = useRef(null)
  useEffect(() => {
    if (!animated || !iconRef.current) return undefined
    const animation = animate(iconRef.current, { rotate: [-5, 5], translateY: [-2, 2], duration: 1800, ease: 'inOutSine', alternate: true, loop: true })
    return () => animation.revert()
  }, [animated])
  return (
    <a href="#top" className="group flex items-center gap-2.5 text-[#f8f1dc]" aria-label="CampusLens home">
      <span ref={iconRef} className="grid size-9 place-items-center rounded-[13px] bg-[#d7f46d] text-[#1b251c] shadow-[3px_3px_0_#f6dfad] transition-transform group-hover:-translate-y-0.5">
        <span className="display-font text-[18px] font-bold leading-none">C</span>
      </span>
      <span className={wordmarkFont ? 'brand-fruktur text-xl leading-none' : 'display-font text-lg font-bold tracking-[-0.05em]'}>CampusLens</span>
    </a>
  )
}

export default Brand
