import { motion } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'
import type { ReactNode } from 'react'

export function Layout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation()
  const isCatalog = pathname === '/'

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-line/60 bg-ink-950/70 backdrop-blur-xl">
        <div className="mx-auto flex max-w-[1400px] items-center justify-between gap-4 px-4 py-4 sm:px-6">
          <Link
            to="/"
            className="group flex items-center gap-3 rounded-lg outline-none
                       focus-visible:ring-2 focus-visible:ring-accent/60 focus-visible:ring-offset-2
                       focus-visible:ring-offset-ink-950"
          >
            {/* Игральная кость сама по себе, без плашки-подложки: заливка градиентом,
                вокруг — прозрачно. На наведении делает вид, что вот-вот бросится,
                на клике — короткий решительный «бросок». tabIndex=-1 — иконка
                декоративная (aria-hidden), кликабелен сам Link вокруг; без этого
                framer-motion из-за whileTap сам делает svg точкой табуляции, и
                по клику браузер рисует на ней нативную синюю рамку фокуса. */}
            <motion.svg
              viewBox="0 0 32 32"
              className="h-9 w-9 shrink-0"
              tabIndex={-1}
              whileHover={{ rotate: 18, scale: 1.08 }}
              whileTap={{ rotate: -22, scale: 0.92 }}
              transition={{ type: 'spring', stiffness: 420, damping: 12 }}
              aria-hidden
            >
              <defs>
                <linearGradient id="header-die-gradient" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#A78BFA" />
                  <stop offset="100%" stopColor="#F472B6" />
                </linearGradient>
              </defs>
              <rect x="3" y="3" width="26" height="26" rx="8" fill="url(#header-die-gradient)" />
              <circle cx="11" cy="11" r="2.6" fill="#07080C" />
              <circle cx="21" cy="11" r="2.6" fill="#07080C" />
              <circle cx="16" cy="16" r="2.6" fill="#07080C" />
              <circle cx="11" cy="21" r="2.6" fill="#07080C" />
              <circle cx="21" cy="21" r="2.6" fill="#07080C" />
            </motion.svg>
            <div className="text-sm font-extrabold tracking-tight text-slate-50">
              Домашняя библиотека
            </div>
          </Link>

          {!isCatalog && (
            <Link
              to="/"
              className="chip hover:border-accent/50 hover:text-slate-100"
            >
              ← ко всем играм
            </Link>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-[1400px] px-4 pb-20 pt-6 sm:px-6">{children}</main>
    </div>
  )
}
