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
          <Link to="/" className="group flex items-center gap-3">
            <motion.div
              whileHover={{ rotate: 12, scale: 1.06 }}
              transition={{ type: 'spring', stiffness: 360, damping: 18 }}
              className="grid h-10 w-10 place-items-center rounded-xl bg-accent-gradient text-lg font-black text-ink-950 shadow-glow"
            >
              ⚄
            </motion.div>
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
