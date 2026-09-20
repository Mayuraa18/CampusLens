import { useEffect, useRef, useState } from 'react'
import Navbar from '../components/Navbar'

const features = [
  ['01', 'Academic Support', 'Notes, PYQs, syllabi and more.', '⌁'],
  ['02', 'Student Community', 'Clubs, peers, discussions.', '◎'],
  ['03', 'Campus Updates', 'Events, workshops, announcements.', '◫'],
  ['04', 'Opportunities', 'Internships, jobs, hackathons.', '↗'],
]

const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value))
const range = (progress, start, end) => clamp((progress - start) / (end - start))
const mix = (from, to, amount) => from + (to - from) * amount
const smooth = value => value * value * (3 - 2 * value)

function Home({ onSignIn, onGetStarted }) {
  const storyRef = useRef(null)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const updateProgress = () => {
      const node = storyRef.current
      if (!node) return
      const distance = node.offsetHeight - window.innerHeight
      setProgress(clamp(-node.getBoundingClientRect().top / Math.max(distance, 1)))
    }
    updateProgress()
    window.addEventListener('scroll', updateProgress, { passive: true })
    window.addEventListener('resize', updateProgress)
    return () => { window.removeEventListener('scroll', updateProgress); window.removeEventListener('resize', updateProgress) }
  }, [])

  const approach = smooth(range(progress, 0, .24))
  const headingExit = smooth(range(progress, .1, .3))
  const callouts = range(progress, .32, .4) * (1 - range(progress, .42, .48))
  const screenScroll = range(progress, .4, .9)
  const transform = range(progress, .94, 1)
  const board = range(progress, .985, 1)
  const laptopStyle = {
    '--story-x': `${mix(14, 0, approach)}vw`,
    '--story-y': `${mix(9, 0, approach)}vh`,
    '--story-scale': mix(.72, 1, approach),
    '--story-rotate': `${mix(-8, 0, approach)}deg`,
    '--story-opacity': mix(.8, 1, approach),
    '--screen-offset': `${mix(0, -75, screenScroll)}%`,
    '--laptop-fade': 1 - transform,
    '--board-opacity': transform,
    '--board-scale': mix(.9, 1, transform),
  }

  return <main id="top" className="bg-[#102319] text-white">
    <section ref={storyRef} className="story-section relative h-[900vh]">
      <div className="story-sticky sticky top-0 h-screen overflow-hidden">
        <div className="story-desk absolute inset-x-0 bottom-0 h-[35%]" />
        <div className="story-doodle left-[4%] top-[25%] hidden lg:block">⌁</div><div className="story-doodle right-[7%] top-[22%] hidden lg:block">⚙</div><div className="story-doodle left-[9%] bottom-[19%] hidden lg:block">⌘</div><div className="story-doodle right-[8%] bottom-[17%] hidden lg:block">⚕</div>
        <Navbar onSignIn={onSignIn} onGetStarted={onGetStarted} />
        <div className="story-copy absolute left-5 top-[25%] z-10 max-w-xl sm:left-8 lg:left-[max(2.5rem,calc((100vw-80rem)/2))]" style={{ opacity: 1 - headingExit, transform: `translateY(${-headingExit * 180}px) scale(${1 - headingExit * .12})`, visibility: progress > .28 ? 'hidden' : 'visible' }}><p className="text-[11px] font-extrabold uppercase tracking-[.24em] text-[#d7f46d]">Your campus companion</p><h1 className="editorial-font mt-5 text-[4rem] leading-[.82] tracking-[-.065em] text-[#fff7e3] sm:text-[5.4rem] lg:text-[6.1rem]">Your Campus.<br /><em className="font-normal text-[#d7f46d]">Simplified.</em></h1><p className="mt-7 text-lg leading-7 text-[#dce6d4]">Find information, manage documents,<br />and stay connected — all in one place.</p><button onClick={onGetStarted} className="mt-8 rounded-full bg-[#d7f46d] px-6 py-3.5 text-sm font-extrabold text-[#18301b] shadow-[4px_4px_0_#f2b693] transition hover:-translate-y-0.5">Get Started →</button><p className="mt-8 text-[10px] font-bold tracking-[.22em] text-[#aebca4]">STUDY · BELONG · EXPLORE · GROW</p></div>
        <StoryLaptop style={laptopStyle} screenScroll={screenScroll} callouts={callouts} board={board} />
        <div className="story-progress" aria-hidden="true"><span style={{ transform: `scaleX(${progress})` }} /></div>
      </div>
    </section>
    <section id="features" className="paper-texture px-5 py-20 sm:px-8 lg:px-10 lg:py-28"><div className="mx-auto max-w-7xl"><p className="text-xs font-extrabold uppercase tracking-[.2em] text-[#d7f46d]">CampusLens, beyond the desk</p><h2 className="editorial-font mt-4 max-w-3xl text-4xl leading-none text-[#fff7e3] sm:text-5xl">One calm place for every important campus moment.</h2><div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{features.map(([number, title, copy, icon]) => <article key={title} className="landing-feature-card"><div className="flex justify-between"><span className="text-2xl text-[#d7f46d]">{icon}</span><span className="text-xs text-[#9ead98]">{number}</span></div><h3 className="editorial-font mt-12 text-2xl text-[#fff7e3]">{title}</h3><p className="mt-3 text-sm leading-6 text-[#c6d2c0]">{copy}</p></article>)}</div></div></section>
    <footer className="border-t border-[#40503c] bg-[#102319] px-5 py-7 text-sm text-[#aeb9a7] sm:px-8 lg:px-10"><div className="mx-auto flex max-w-7xl justify-between"><p>CampusLens · Your campus, understood.</p><p>Study · Belong · Explore · Grow</p></div></footer>
  </main>
}

function StoryLaptop({ style, screenScroll, callouts, board }) {
  return <div className="story-device-wrap" style={style}>
    <div className="story-callouts" style={{ opacity: callouts * (1 - board) }} aria-hidden="true"><Callout className="callout-support" label="Academic Support" /><Callout className="callout-updates" label="Campus Updates" /><Callout className="callout-opportunities" label="Find opportunities" /><Callout className="callout-ask" label="Ask CampusLens" /><Callout className="callout-all" label="Everything in one place" /></div>
    <div className="story-laptop"><div className="story-screen"><div className="story-screen-scroll" style={{ transform: `translateY(${style['--screen-offset']})` }}><ScreenTop /><ScreenJourney /><ScreenGathered /></div></div><div className="story-laptop-base"><span /></div></div>
    <NoticeBoard opacity={board} />
  </div>
}

function Callout({ className, label }) { return <div className={`story-callout ${className}`}><span>{label}</span><i /></div> }

function ScreenTop() { return <div className="screen-top"><div className="flex items-center justify-between border-b border-[#4a6147] pb-3"><div className="flex items-center gap-2"><b className="grid size-7 place-items-center rounded-lg bg-[#d7f46d] text-xs text-[#18301b]">C</b><strong className="text-sm text-[#fff8e7]">CampusLens</strong></div><small className="rounded-full bg-[#314931] px-2 py-1 text-[8px]">MAYURA</small></div><div className="mt-4 rounded-xl border border-[#52694d] bg-[#1c3421] px-3 py-2.5 text-xs text-[#9fae9a]">⌕&nbsp; Search your campus</div><div className="mt-4 grid grid-cols-4 gap-2">{[['Academic','⌁'],['Updates','◫'],['Ask','◌'],['Opportunities','↗']].map(([label, icon]) => <div key={label} className="screen-tool"><span>{icon}</span>{label}</div>)}</div><div className="mt-4 grid gap-3 sm:grid-cols-[1.05fr_.95fr]"><div className="rounded-xl border border-[#50694d] bg-[#1a3120] p-3"><p className="text-[9px] font-extrabold uppercase tracking-[.16em] text-[#d7f46d]">Campus dashboard</p><div className="mt-3 grid grid-cols-2 gap-2"><div className="rounded-lg bg-[#2a472e] p-2"><b className="text-lg">06</b><p className="text-[9px] text-[#aebca8]">documents</p></div><div className="rounded-lg bg-[#2a472e] p-2"><b className="text-lg text-[#f2b693]">03</b><p className="text-[9px] text-[#aebca8]">deadlines</p></div></div></div><div className="rounded-xl border border-[#50694d] bg-[#213d27] p-3"><p className="text-[9px] font-bold uppercase tracking-[.14em] text-[#f2b693]">Ask CampusLens</p><p className="mt-3 text-xs font-bold">What is the registration deadline?</p><p className="mt-2 text-[9px] text-[#d7f46d]">Source · Page 2</p></div></div></div> }

function ScreenJourney() { return <div className="screen-journey"><ScreenStage eyebrow="Academic Support" title="Study smarter, without the scramble." cards={['Notes', 'PYQs', 'Syllabus', 'Study resources']} /><ScreenStage eyebrow="Campus Updates" title="The notices worth knowing." cards={['Exam form opens 05 Oct', 'Design workshop · Friday', 'Library hours extended', 'Robotics exhibition']} /><ScreenStage eyebrow="Student Community" title="Find your people on campus." cards={['Coding Club', 'Design Circle', 'Student discussions', 'Weekend activities']} /><ScreenStage eyebrow="Opportunities" title="The next good thing might be here." cards={['Summer internships', 'Bharat Builds hackathon', 'Merit scholarships', 'Campus jobs']} /></div> }

function ScreenStage({ eyebrow, title, cards }) { return <section className="screen-stage"><p className="text-[9px] font-extrabold uppercase tracking-[.2em] text-[#d7f46d]">{eyebrow}</p><h2 className="editorial-font mt-3 max-w-[80%] text-2xl leading-none text-[#fff7e3]">{title}</h2><div className="mt-5 grid grid-cols-2 gap-2">{cards.map((card, index) => <div key={card} className="screen-stage-card"><span className="text-[#f2b693]">0{index + 1}</span><p>{card}</p></div>)}</div><p className="mt-5 text-[9px] text-[#aebca8]">Keep scrolling to explore <span className="text-[#d7f46d]">↓</span></p></section> }

function ScreenGathered() { return <section className="screen-gathered"><p className="text-[9px] font-extrabold uppercase tracking-[.2em] text-[#d7f46d]">The Campus, Gathered</p><h2 className="editorial-font mt-3 text-2xl leading-none text-[#fff7e3]">Everything you need to make a little more sense of the semester.</h2><div className="mt-5 grid grid-cols-2 gap-2">{features.map(([number, title, copy, icon]) => <article key={title} className="screen-feature"><div className="flex justify-between"><span className="text-lg text-[#d7f46d]">{icon}</span><span className="text-[8px] text-[#9ead98]">{number}</span></div><h3 className="editorial-font mt-6 text-base text-[#fff7e3]">{title}</h3><p className="mt-2 text-[9px] leading-3 text-[#c6d2c0]">{copy}</p></article>)}</div><p className="screen-settle">A little time to take it all in.</p></section> }

function NoticeBoard({ opacity }) { return <div className="notice-board" style={{ opacity, pointerEvents: opacity > .5 ? 'auto' : 'none' }}><div className="board-paper board-title"><span className="board-pin" /><p className="text-[8px] font-extrabold uppercase tracking-[.16em] text-[#57704b]">Made for the in-between moments</p><h2 className="editorial-font mt-3 text-2xl leading-none text-[#1e3822]">Less searching.<br />More showing up.</h2></div><div className="board-paper board-quote"><span className="board-pin peach" /><p className="text-[8px] font-bold uppercase tracking-[.14em] text-[#68815d]">A calm place to begin</p><p className="editorial-font mt-4 text-lg leading-none text-[#1d3620]">“I knew what I needed to do before the noticeboard got crowded.”</p><div className="mt-4 border-t border-[#b9c8a6] pt-2 text-[8px] text-[#567052]">A student’s campus companion</div></div><div className="board-note"><span className="board-pin" />NEW CLUBS<br />WORKSHOPS<br />SCHOLARSHIPS</div></div> }

export default Home
