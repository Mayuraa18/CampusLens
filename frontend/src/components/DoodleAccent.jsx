function DoodleAccent({ type, className = '' }) {
  if (type === 'star') return <svg viewBox="0 0 74 74" className={className} aria-hidden="true"><path className="doodle-line" d="M37 4c1 23 6 30 33 33-27 2-32 10-33 33-2-23-8-30-33-33 25-3 31-10 33-33Z" stroke="currentColor" strokeWidth="2.3" /></svg>
  if (type === 'arrow') return <svg viewBox="0 0 97 73" className={className} aria-hidden="true"><path className="doodle-line" d="M7 20c20 29 52 35 75 20M71 28l12 12-16 6" stroke="currentColor" strokeWidth="2.3" /></svg>
  return <svg viewBox="0 0 100 58" className={className} aria-hidden="true"><path className="doodle-line" d="M4 31C26 2 74 4 96 29 76 57 28 59 4 31Z" stroke="currentColor" strokeWidth="2" /></svg>
}

export default DoodleAccent
