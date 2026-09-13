import { motion } from 'framer-motion'
import { forwardRef } from 'react'
import { Link } from 'react-router-dom'

import type { GameListItem } from '../api/types'
import { complexityInfo, playersLabel, playtimeCompactLabel } from '../lib/format'
import { Cover } from './Cover'
import { ComplexityMeter } from './ComplexityMeter'

function PlayersIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-3 w-3 shrink-0" fill="none" aria-hidden>
      <circle cx="9" cy="8" r="3.2" stroke="currentColor" strokeWidth={1.8} />
      <path
        d="M3.5 20c0-3.6 2.9-6 5.5-6s5.5 2.4 5.5 6"
        stroke="currentColor"
        strokeWidth={1.8}
        strokeLinecap="round"
      />
      <path
        d="M15.5 4.8c1.6.4 2.7 1.8 2.7 3.4 0 1.6-1.1 3-2.7 3.4M18 14.4c2 .6 3.5 2.6 3.5 5"
        stroke="currentColor"
        strokeWidth={1.8}
        strokeLinecap="round"
      />
    </svg>
  )
}

function ClockIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-3 w-3 shrink-0" fill="none" aria-hidden>
      <circle cx="12" cy="12" r="8.5" stroke="currentColor" strokeWidth={1.8} />
      <path d="M12 7.5V12l3 2" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

const cardVariants = {
  hidden: { opacity: 0, y: 14 },
  visible: (index: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: Math.min(index * 0.035, 0.35), duration: 0.35, ease: [0.22, 1, 0.36, 1] },
  }),
}

interface Props {
  game: GameListItem
  index: number
}

// forwardRef обязателен: AnimatePresence mode="popLayout" вешает на карточку ref,
// чтобы измерить её перед выходом из сетки.
export const GameCard = forwardRef<HTMLDivElement, Props>(function GameCard(
  { game, index },
  ref,
) {
  const complexity = complexityInfo(game.complexity)

  return (
    <motion.div
      ref={ref}
      custom={index}
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      layout
      whileHover={{ y: -6 }}
      transition={{ type: 'spring', stiffness: 320, damping: 26 }}
      className="group"
    >
      <Link
        to={`/game/${game.slug}`}
        className="panel block overflow-hidden p-3 shadow-card transition-shadow duration-300 hover:shadow-glow"
      >
        <div className="relative aspect-[3/4] overflow-hidden rounded-xl">
          <div className="h-full w-full transition-transform duration-500 group-hover:scale-[1.04]">
            <Cover src={game.cover} title={game.title} />
          </div>

          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-ink-950/90 to-transparent" />

          <div className="absolute left-2 top-2 flex flex-col items-start gap-1">
            {game.is_expansion && (
              <span className="rounded-md bg-ink-950/80 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-blush backdrop-blur">
                дополнение
              </span>
            )}
            {game.has_solo_mode && (
              <span className="rounded-md bg-ink-950/80 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-emerald-300 backdrop-blur">
                соло
              </span>
            )}
          </div>

          <div className="absolute inset-x-2 bottom-2 flex items-center justify-between text-[11px] font-semibold text-slate-200">
            <span className="flex items-center gap-1 rounded-md bg-ink-950/70 px-2 py-1 backdrop-blur">
              <PlayersIcon />
              {playersLabel(game.min_players, game.max_players)}
            </span>
            {game.playtime !== null && (
              <span className="flex items-center gap-1 rounded-md bg-ink-950/70 px-2 py-1 backdrop-blur">
                <ClockIcon />
                {playtimeCompactLabel(game.playtime)}
              </span>
            )}
          </div>
        </div>

        <div className="mt-3 space-y-1.5">
          <h3 className="line-clamp-2 text-sm font-bold leading-snug text-slate-50 transition-colors duration-200 group-hover:text-accent-soft">
            {game.title}
          </h3>
          {(game.categories.length > 0 || game.complexity !== null) && (
            <div className="flex items-center justify-between gap-2 text-[11px] text-mist">
              <span className="line-clamp-1">
                {game.categories.map((c) => c.name).join(' · ')}
              </span>
              {game.complexity !== null && (
                <ComplexityMeter value={game.complexity} className={`shrink-0 text-[13px] ${complexity.className}`} />
              )}
            </div>
          )}
        </div>
      </Link>
    </motion.div>
  )
})
