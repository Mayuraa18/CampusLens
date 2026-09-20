import Icon from './Icon'
import { useEffect, useRef } from 'react'
import { animate } from 'animejs'

const styles = { lime: 'bg-[#c9ee6f] text-[#1f2c1e]', sand: 'bg-[#f2dfb7] text-[#42351e]', coral: 'bg-[#eaa17e] text-[#38241e]' }
function FeatureCard({ card }) {
  const cardRef = useRef(null)
  const iconRef = useRef(null)
  useEffect(() => {
    const animations = []
    if (cardRef.current) animations.push(animate(cardRef.current, { opacity: [0, 1], translateY: [20, 0], duration: 650, ease: 'outExpo' }))
    if (iconRef.current) animations.push(animate(iconRef.current, { rotate: [-3, 3], duration: 1800, ease: 'inOutSine', alternate: true, loop: true }))
    return () => animations.forEach(animation => animation.revert())
  }, [])
  return <article ref={cardRef} className="group rounded-[28px] border border-[#475842] bg-[#243024] p-5 transition duration-300 hover:-translate-y-1 hover:border-[#9bb863] hover:bg-[#293728] sm:p-6">
    <span ref={iconRef} className={`mb-8 grid size-12 place-items-center rounded-2xl ${styles[card.tone]}`}><Icon name={card.icon} className="size-6" /></span>
    <h3 className="display-font text-xl font-bold tracking-tight text-[#f8f1dc]">{card.title}</h3>
    <p className="mt-2 max-w-[25ch] text-sm leading-6 text-[#bdc7b7]">{card.description}</p>
    <button className="mt-5 inline-flex items-center gap-2 text-sm font-bold text-[#d7f46d]">{card.action}<Icon name="arrow" className="size-4 transition group-hover:translate-x-1" /></button>
  </article>
}

export default FeatureCard
