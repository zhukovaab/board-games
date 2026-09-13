import { motion } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import type { ReactNode } from 'react'

// Координаты точек для каждой грани кости (1-6), сетка 32×32.
const DIE_PIPS: Record<number, [number, number][]> = {
  1: [[16, 16]],
  2: [[11, 11], [21, 21]],
  3: [[11, 11], [16, 16], [21, 21]],
  4: [[11, 11], [21, 11], [11, 21], [21, 21]],
  5: [[11, 11], [21, 11], [16, 16], [11, 21], [21, 21]],
  6: [[11, 10], [21, 10], [11, 16], [21, 16], [11, 22], [21, 22]],
}

export function Layout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation()
  const isCatalog = pathname === '/'
  const [dieFace, setDieFace] = useState(5)

  // Бросок: сперва проигрывается whileTap-анимация (короткий взмах),
  // а затем, будто кость упала, меняем грань на случайную (не повторяя текущую).
  const rollDie = () => {
    setTimeout(() => {
      setDieFace((prev) => {
        let next = Math.floor(Math.random() * 6) + 1
        while (next === prev) next = Math.floor(Math.random() * 6) + 1
        return next
      })
    }, 150)
  }

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
                на клике — короткий решительный «бросок». Иконка декоративная
                (aria-hidden), кликабелен сам Link вокруг — но framer-motion из-за
                whileTap всё равно делает svg фокусируемым, и клик точно по ней
                (не по всей ссылке) фокусирует именно svg и рисует нативную синюю
                рамку; tabIndex=-1 убирает её только из Tab, а не из клика, поэтому
                дополнительно гасим фокусировку на mousedown через preventDefault. */}
            <motion.svg
              viewBox="0 0 32 32"
              className="h-9 w-9 shrink-0"
              tabIndex={-1}
              onMouseDown={(event) => event.preventDefault()}
              onClick={rollDie}
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
              {DIE_PIPS[dieFace].map(([cx, cy]) => (
                <circle key={`${cx}-${cy}`} cx={cx} cy={cy} r="2.6" fill="#07080C" />
              ))}
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
