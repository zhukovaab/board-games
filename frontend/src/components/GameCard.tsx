import { motion } from 'framer-motion'
import { forwardRef } from 'react'
import { Link } from 'react-router-dom'

import type { GameListItem } from '../api/types'
import { complexityInfo, playersLabel, playtimeLabel } from '../lib/format'
import { Cover } from './Cover'
import { ComplexityMeter } from './ComplexityMeter'

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

          <div className="absolute left-2 top-2 flex flex-col gap-1">
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
            <span className="rounded-md bg-ink-950/70 px-2 py-1 backdrop-blur">
              {playersLabel(game.min_players, game.max_players)} чел.
            </span>
            <span className="rounded-md bg-ink-950/70 px-2 py-1 backdrop-blur">
              {playtimeLabel(game.playtime)}
            </span>
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
                // На карточке — только шкала, без числа: места мало, а цвет и
                // заливка сами по себе понятно передают уровень сложности.
                <ComplexityMeter value={game.complexity} className={`shrink-0 text-[13px] ${complexity.className}`} />
              )}
            </div>
          )}
        </div>
      </Link>
    </motion.div>
  )
})
