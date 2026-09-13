import { useQuery } from '@tanstack/react-query'
import { AnimatePresence, motion } from 'framer-motion'
import { useState, type ReactNode } from 'react'
import { Link, useParams } from 'react-router-dom'

import { api, mediaUrl } from '../api/client'
import { Cover } from '../components/Cover'
import { Tag } from '../components/Tag'
import { ShimmerBlock } from '../components/Skeletons'
import { ComplexityMeter } from '../components/ComplexityMeter'
import { ageLabel, complexityInfo, playersLabel, playtimeLabel } from '../lib/format'

function Stat({ label, value, accent }: { label: string; value: ReactNode; accent?: string }) {
  return (
    <div className="panel p-4">
      <div className="text-[11px] uppercase tracking-[0.14em] text-mist">{label}</div>
      <div className={`mt-1 text-lg font-bold ${accent ?? 'text-slate-50'}`}>{value}</div>
    </div>
  )
}

function RelatedCard({ slug, title, cover }: { slug: string; title: string; cover: string | null }) {
  return (
    <Link
      to={`/game/${slug}`}
      className="panel group flex items-center gap-3 p-3 transition-shadow hover:shadow-glow"
    >
      <div className="h-16 w-12 shrink-0 overflow-hidden rounded-lg">
        <Cover src={cover} title={title} rounded="rounded-lg" />
      </div>
      <span className="text-sm font-semibold text-slate-100 transition-colors group-hover:text-accent-soft">
        {title}
      </span>
    </Link>
  )
}

export function GamePage() {
  const { slug = '' } = useParams()
  const [lightbox, setLightbox] = useState<string | null>(null)

  const { data: game, isLoading, isError } = useQuery({
    queryKey: ['game', slug],
    queryFn: () => api.game(slug),
  })

  if (isLoading) {
    return (
      <div className="grid gap-8 lg:grid-cols-[340px_1fr]">
        <ShimmerBlock className="aspect-[3/4] w-full" />
        <div className="space-y-4">
          <ShimmerBlock className="h-9 w-2/3 rounded-lg" />
          <ShimmerBlock className="h-4 w-1/3 rounded-lg" />
          <ShimmerBlock className="h-28 w-full rounded-2xl" />
        </div>
      </div>
    )
  }

  if (isError || !game) {
    return (
      <div className="panel p-14 text-center">
        <p className="text-sm text-mist">Такой игры на полке нет.</p>
        <Link to="/" className="chip chip-active mt-4 inline-flex">
          вернуться в каталог
        </Link>
      </div>
    )
  }

  const complexity = complexityInfo(game.complexity)

  return (
    <motion.article
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className="space-y-10"
    >
      <div className="grid gap-8 lg:grid-cols-[340px_1fr]">
        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.45 }}
          className="relative"
        >
          <div className="aspect-[3/4] overflow-hidden rounded-2xl shadow-card">
            <Cover src={game.cover} title={game.title} rounded="rounded-2xl" />
          </div>
          <div className="absolute inset-0 -z-10 translate-y-6 scale-95 rounded-2xl bg-accent/25 blur-3xl" />
        </motion.div>

        <div className="space-y-6">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              {game.is_expansion && (
                <span className="rounded-md bg-blush/15 px-2 py-1 text-[11px] font-bold uppercase tracking-wide text-blush">
                  дополнение
                </span>
              )}
              {game.has_solo_mode && (
                <span className="rounded-md bg-emerald-400/15 px-2 py-1 text-[11px] font-bold uppercase tracking-wide text-emerald-300">
                  соло-режим
                </span>
              )}
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">{game.title}</h1>
            {game.title_original && (
              <p className="text-sm text-mist">{game.title_original}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <Stat label="игроки" value={`${playersLabel(game.min_players, game.max_players)}`} />
            <Stat label="партия" value={playtimeLabel(game.playtime)} />
            <Stat label="возраст" value={ageLabel(game.min_age)} />
            <Stat
              label="сложность"
              value={
                game.complexity !== null ? (
                  // Цвет уже несёт сама шкала — общий accent на Stat тут не нужен,
                  // он бы заодно перекрасил и подпись «средне» рядом.
                  <span className="flex items-center gap-2">
                    <ComplexityMeter value={game.complexity} className={`text-2xl ${complexity.className}`} />
                    <span className="text-xs font-semibold text-mist">{complexity.label}</span>
                  </span>
                ) : (
                  '—'
                )
              }
            />
          </div>

          {game.best_players && (
            <p className="text-sm text-mist">
              Оптимальное число игроков: <span className="font-semibold text-slate-100">{game.best_players}</span>
            </p>
          )}

          {(game.categories.length > 0 || game.themes.length > 0 || game.mechanics.length > 0) && (
            <div className="flex flex-wrap gap-2">
              {game.categories.map((item) => (
                <Tag key={`c-${item.id}`} kind="cat" slug={item.slug} name={item.name} />
              ))}
              {game.themes.map((item) => (
                <Tag key={`t-${item.id}`} kind="theme" slug={item.slug} name={item.name} />
              ))}
              {game.mechanics.map((item) => (
                <Tag key={`m-${item.id}`} kind="mech" slug={item.slug} name={item.name} />
              ))}
            </div>
          )}

          {game.description && (
            <p className="max-w-3xl whitespace-pre-line text-[15px] leading-relaxed text-slate-300">
              {game.description}
            </p>
          )}

          {(game.rules_url || game.rules_file) && (
            <div className="flex flex-wrap gap-3">
              {game.rules_url && (
                <a
                  href={game.rules_url}
                  target="_blank"
                  rel="noreferrer"
                  className="chip hover:border-accent/50 hover:text-slate-100"
                >
                  правила онлайн ↗
                </a>
              )}
              {game.rules_file && (
                <a
                  href={mediaUrl(game.rules_file) ?? '#'}
                  target="_blank"
                  rel="noreferrer"
                  className="chip hover:border-accent/50 hover:text-slate-100"
                >
                  правила файлом ↓
                </a>
              )}
            </div>
          )}
        </div>
      </div>

      {(game.location || game.notes) && (
        <section className="panel space-y-3 p-6">
          <h2 className="text-xs font-bold uppercase tracking-[0.14em] text-mist">Дома</h2>
          {game.location && (
            <p className="text-sm text-slate-200">
              <span className="text-mist">Где лежит: </span>
              {game.location}
            </p>
          )}
          {game.notes && (
            <p className="whitespace-pre-line text-sm leading-relaxed text-slate-300">
              {game.notes}
            </p>
          )}
        </section>
      )}

      {game.images.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-xs font-bold uppercase tracking-[0.14em] text-mist">Галерея</h2>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
            {game.images.map((image, index) => (
              <motion.button
                key={image.id}
                type="button"
                onClick={() => setLightbox(mediaUrl(image.image))}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ y: -4 }}
                className="group overflow-hidden rounded-xl border border-line/70"
              >
                <div className="aspect-[4/3] overflow-hidden">
                  <img
                    src={mediaUrl(image.image) ?? ''}
                    alt={image.caption || game.title}
                    loading="lazy"
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                </div>
                {image.caption && (
                  <div className="p-2 text-left text-xs text-mist">{image.caption}</div>
                )}
              </motion.button>
            ))}
          </div>
        </section>
      )}

      {(game.base_game || game.expansions.length > 0) && (
        <section className="space-y-4">
          <h2 className="text-xs font-bold uppercase tracking-[0.14em] text-mist">
            {game.base_game ? 'Базовая игра' : 'Дополнения'}
          </h2>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {game.base_game && (
              <RelatedCard
                slug={game.base_game.slug}
                title={game.base_game.title}
                cover={game.base_game.cover}
              />
            )}
            {game.expansions.map((expansion) => (
              <RelatedCard
                key={expansion.id}
                slug={expansion.slug}
                title={expansion.title}
                cover={expansion.cover}
              />
            ))}
          </div>
        </section>
      )}

      <AnimatePresence>
        {lightbox && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setLightbox(null)}
            className="fixed inset-0 z-50 grid place-items-center bg-ink-950/90 p-6 backdrop-blur"
          >
            <motion.img
              initial={{ scale: 0.94, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.94, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 260, damping: 26 }}
              src={lightbox}
              alt=""
              className="max-h-[85vh] max-w-full rounded-2xl shadow-card"
            />
          </motion.div>
        )}
      </AnimatePresence>
    </motion.article>
  )
}
