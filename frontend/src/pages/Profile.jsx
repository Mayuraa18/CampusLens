import { useEffect, useRef, useState } from 'react'
import { animate, stagger } from 'animejs'
import Icon from '../components/Icon'

const themes = [
  ['lime', 'Original green', '#193a25', '#d7f46d'],
  ['magenta', 'Magenta rose', '#4a163d', '#ff78c8'],
  ['turquoise', 'Turquoise', '#123e43', '#67e5df'],
  ['navy', 'Navy cyan', '#173650', '#92e6ed'],
  ['burgundy', 'Burgundy peach', '#5b2831', '#ffc7a5'],
  ['ocean', 'Blue gold', '#1f3b67', '#f6d365'],
  ['mint', 'Forest mint', '#25483a', '#a8ebc5'],
  ['cocoa', 'Brown cream', '#4a3429', '#f3dfbd'],
  ['slate', 'Slate green', '#263539', '#b6ed89'],
]

function Profile({ user, theme = 'lime', onThemeChange }) {
  const [email, setEmail] = useState(user?.email || '')
  const [flow, setFlow] = useState('idle')
  const [otp, setOtp] = useState('')
  const [password, setPassword] = useState('')
  const [notice, setNotice] = useState('')
  const cardsRef = useRef(null)
  const username = user?.username || 'CampusLens student'

  useEffect(() => { setEmail(user?.email || '') }, [user?.email])
  useEffect(() => {
    if (!cardsRef.current || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return undefined
    const animation = animate(cardsRef.current.children, { opacity: [0, 1], translateY: [18, 0], delay: stagger(90), duration: 520, ease: 'outExpo' })
    return () => animation.revert()
  }, [])

  function beginEmail(event) {
    event.preventDefault()
    if (!email.includes('@')) return setNotice('Enter a valid email address.')
    setFlow('email-otp')
    setNotice('Verification delivery needs a profile-update endpoint from the backend. This UI is ready for it.')
  }
  function verifyEmail(event) {
    event.preventDefault()
    if (otp.trim().length !== 6) return setNotice('Enter the 6-digit verification code.')
    setFlow('email-success')
    setNotice('Email verification completed in the interface. A backend verification endpoint is needed to save this change.')
  }
  function finishReset(event) {
    event.preventDefault()
    if (password.length < 8) return setNotice('Your new password must contain at least 8 characters.')
    setFlow('password-success')
    setNotice('Password reset is ready to submit when the backend supports OTP password recovery.')
  }

  return (
    <div className="dashboard-light min-h-screen px-5 py-8 sm:px-8 lg:px-10 lg:py-10">
      <div className="mx-auto max-w-5xl">
        <header className="dashboard-side-card rounded-[32px] p-6 sm:p-9">
          <div className="flex items-center gap-4">
            <span className="grid size-14 place-items-center rounded-2xl bg-[#dce8c4] text-xl font-bold text-[#315235]">{username.slice(0, 1).toUpperCase()}</span>
            <div><p className="text-xs font-bold uppercase tracking-[.16em] text-[#5c7c45]">Your CampusLens space</p><p className="mt-1 text-sm font-semibold text-[#dfead5]">{username}</p></div>
          </div>
          <h1 className="editorial-font mt-6 text-4xl tracking-[-.06em] text-[#f8f1dc] sm:text-5xl">My profile</h1>
          <p className="mt-3 max-w-xl text-sm leading-6 text-[#c7d2c2]">Keep the account details for your campus companion up to date.</p>
        </header>

        <div ref={cardsRef} className="mt-6 grid gap-5 lg:grid-cols-2">
          <section className="dashboard-side-card rounded-[28px] p-6">
            <div className="flex items-center gap-3"><span className="grid size-11 place-items-center rounded-2xl bg-[#dce8c4] text-[#315235]"><Icon name="user" className="size-5" /></span><div><p className="text-xs font-bold uppercase tracking-[.14em] text-[#c6d8b7]">Account details</p><h2 className="display-font text-xl font-bold text-[#f8f1dc]">Email address</h2></div></div>
            <p className="mt-5 rounded-xl bg-[#f4f6e9] px-3 py-2 text-sm text-[#38533c]">Signed in as <strong>{user?.email || 'Email unavailable until account data loads.'}</strong></p>
            {flow === 'email-otp' ? <form onSubmit={verifyEmail} className="mt-5"><label className="block text-sm font-semibold text-[#e6ecdf]">Verification code<input value={otp} onChange={(event) => setOtp(event.target.value)} inputMode="numeric" maxLength="6" placeholder="6-digit OTP" className="mt-2 w-full rounded-xl border border-[#8fa882] bg-white px-4 py-3 text-[#28432e] outline-none focus:border-[#d7f46d]" /></label><button className="mt-4 rounded-xl bg-[#d7f46d] px-4 py-3 text-sm font-bold text-[#1d281c]">Verify OTP</button></form> : flow === 'email-success' ? <p className="mt-5 rounded-xl bg-[#e5f2cd] px-4 py-3 text-sm text-[#426b2d]">Email verification complete. Your account API will need to persist this update.</p> : <form onSubmit={beginEmail} className="mt-5"><label className="block text-sm font-semibold text-[#e6ecdf]">New college email<input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 w-full rounded-xl border border-[#8fa882] bg-white px-4 py-3 text-[#28432e] outline-none focus:border-[#d7f46d]" /></label><button className="mt-4 rounded-xl bg-[#d7f46d] px-4 py-3 text-sm font-bold text-[#1d281c]">Update email</button></form>}
          </section>
          <section className="dashboard-side-card rounded-[28px] p-6">
            <div className="flex items-center gap-3"><span className="grid size-11 place-items-center rounded-2xl bg-[#f3d5a9] text-[#6a402e]"><Icon name="lock" className="size-5" /></span><div><p className="text-xs font-bold uppercase tracking-[.14em] text-[#f3d5a9]">Security</p><h2 className="display-font text-xl font-bold text-[#f8f1dc]">Change password</h2></div></div>
            {flow === 'password-email' ? <form onSubmit={finishReset} className="mt-5 space-y-3"><label className="block text-sm font-semibold text-[#e6ecdf]">New password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} minLength="8" className="mt-2 w-full rounded-xl border border-[#8fa882] bg-white px-4 py-3 text-[#28432e] outline-none focus:border-[#d7f46d]" /></label><p className="text-xs text-[#c7d2c2]">A verification email/OTP will be used when the account API supports password reset.</p><button className="rounded-xl bg-[#d7f46d] px-4 py-3 text-sm font-bold text-[#1d281c]">Save new password</button></form> : flow === 'password-success' ? <p className="mt-5 rounded-xl bg-[#e5f2cd] px-4 py-3 text-sm text-[#426b2d]">Password reset flow complete in the interface.</p> : <div className="mt-5"><p className="text-sm leading-6 text-[#c7d2c2]">Reset your password through an email and verification-code flow.</p><button onClick={() => { setFlow('password-email'); setNotice('') }} className="mt-4 rounded-xl border border-[#d7f46d] px-4 py-3 text-sm font-bold text-[#d7f46d]">Reset password</button></div>}
          </section>
        </div>

        <section className="dashboard-side-card mt-6 rounded-[28px] p-6">
          <p className="text-xs font-bold uppercase tracking-[.14em] text-[#c6d8b7]">Personalise your app</p><h2 className="display-font mt-1 text-2xl font-bold text-[#f8f1dc]">Authenticated theme</h2><p className="mt-2 text-sm text-[#c7d2c2]">This preference changes only the signed-in workspace—not the public landing page.</p>
          <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">{themes.map(([id, name, base, accent]) => <button key={id} onClick={() => onThemeChange?.(id)} className={`rounded-xl border p-3 text-left transition ${theme === id ? 'border-[#d7f46d] ring-2 ring-[#d7f46d]/50' : 'border-[#718b69] hover:border-[#d7f46d]'}`}><span className="mb-2 block h-7 rounded-lg" style={{ background: `linear-gradient(135deg, ${base} 0 65%, ${accent} 65%)` }} /><span className="text-xs font-bold text-[#edf4e6]">{name}</span></button>)}</div>
        </section>
        {notice && <p className="mt-5 rounded-xl border border-[#8fa882] bg-[#203a24] px-4 py-3 text-sm text-[#e6f4ce]">{notice}</p>}
      </div>
    </div>
  )
}
export default Profile
