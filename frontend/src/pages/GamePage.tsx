import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { useEffect, useRef, useState, type ReactNode, type UIEvent } from 'react'
import { Link, useParams } from 'react-router-dom'
import Lightbox from 'yet-another-react-lightbox'
import Captions from 'yet-another-react-lightbox/plugins/captions'
import Thumbnails from 'yet-another-react-lightbox/plugins/thumbnails'
import Zoom from 'yet-another-react-lightbox/plugins/zoom'
import 'yet-another-react-lightbox/styles.css'
import 'yet-another-react-lightbox/plugins/captions.css'
import 'yet-another-react-lightbox/plugins/thumbnails.css'

import { api, mediaUrl } from '../api/client'
import { Cover } from '../components/Cover'
import { Markdown } from '../components/Markdown'
import { Tag } from '../components/Tag'
import { ShimmerBlock } from '../components/Skeletons'
import { ComplexityMeter } from '../components/ComplexityMeter'
import { ageLabel, complexityInfo, playersLabel, playtimeLabel } from '../lib/format'

function ExternalLinkIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-3.5 w-3.5 shrink-0" fill="none" aria-hidden>
      <path
        d="M9 6H6.75A1.75 1.75 0 0 0 5 7.75v9.5c0 .966.784 1.75 1.75 1.75h9.5A1.75 1.75 0 0 0 18 17.25V15"
        stroke="currentColor"
        strokeWidth={1.8}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path d="M13 5h6v6M18.5 5.5 11 13" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function ZoomIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-4 w-4 shrink-0" fill="none" aria-hidden>
      <circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" strokeWidth={1.8} />
      <path d="M15.5 15.5 20 20" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" />
      <path d="M10.5 8v5M8 10.5h5" stroke="currentColor" strokeWidth={1.6} strokeLinecap="round" />
    </svg>
  )
}

function ChevronLeftIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-5 w-5 shrink-0" fill="none" aria-hidden>
      <path d="M15 5.5 8 12l7 6.5" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function ChevronRightIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-5 w-5 shrink-0" fill="none" aria-hidden>
      <path d="M9 5.5 16 12l-7 6.5" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function DocumentIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-3.5 w-3.5 shrink-0" fill="none" aria-hidden>
      <path
        d="M7 3.75h7.5L19 8.25V19.5a.75.75 0 0 1-.75.75H7a.75.75 0 0 1-.75-.75V4.5A.75.75 0 0 1 7 3.75Z"
        stroke="currentColor"
        strokeWidth={1.8}
        strokeLinejoin="round"
      />
      <path d="M14 3.75V8h4.25" stroke="currentColor" strokeWidth={1.8} strokeLinejoin="round" />
      <path d="M9 13h6M9 16.5h6" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" />
    </svg>
  )
}

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
  const [lightboxIndex, setLightboxIndex] = useState<number | null>(null)
  const [scrollState, setScrollState] = useState({ atStart: true, atEnd: true })
  const galleryScrollRef = useRef<HTMLDivElement>(null)

  const { data: game, isLoading, isError } = useQuery({
    queryKey: ['game', slug],
    queryFn: () => api.game(slug),
  })

  const handleGalleryScroll = (event: UIEvent<HTMLDivElement>) => {
    const el = event.currentTarget
    setScrollState({
      atStart: el.scrollLeft <= 8,
      atEnd: el.scrollLeft + el.clientWidth >= el.scrollWidth - 8,
    })
  }

  useEffect(() => {
    const el = galleryScrollRef.current
    if (!el) return
    setScrollState({
      atStart: el.scrollLeft <= 8,
      atEnd: el.scrollLeft + el.clientWidth >= el.scrollWidth - 8,
    })
  }, [game?.images.length])

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

          {(game.rules_url || game.rules_file) && (
            <div className="flex flex-wrap gap-3">
              {game.rules_url && (
                <a
                  href={game.rules_url}
                  target="_blank"
                  rel="noreferrer"
                  className="chip hover:border-accent/50 hover:text-slate-100"
                >
                  <ExternalLinkIcon />
                  правила на сайте
                </a>
              )}
              {game.rules_file && (
                <a
                  href={mediaUrl(game.rules_file) ?? '#'}
                  target="_blank"
                  rel="noreferrer"
                  className="chip hover:border-accent/50 hover:text-slate-100"
                >
                  <DocumentIcon />
                  правила
                </a>
              )}
            </div>
          )}
        </div>
      </div>

      {game.description && (
        <section className="space-y-3">
          <h2 className="text-xs font-bold uppercase tracking-[0.14em] text-mist">Описание</h2>
          <Markdown>{game.description}</Markdown>
        </section>
      )}

      {(game.location || game.notes) && (
        <section className="panel space-y-3 p-6">
          <h2 className="text-xs font-bold uppercase tracking-[0.14em] text-mist">Заметки</h2>
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
          <div className="relative">
            <div
              aria-hidden
              className={`pointer-events-none absolute inset-y-0 left-0 z-10 w-10 bg-gradient-to-r from-ink-950 to-transparent transition-opacity duration-300 sm:w-16 ${
                scrollState.atStart ? 'opacity-0' : 'opacity-100'
              }`}
            />
            <div
              aria-hidden
              className={`pointer-events-none absolute inset-y-0 right-0 z-10 w-10 bg-gradient-to-l from-ink-950 to-transparent transition-opacity duration-300 sm:w-16 ${
                scrollState.atEnd ? 'opacity-0' : 'opacity-100'
              }`}
            />
            <div
              ref={galleryScrollRef}
              onScroll={handleGalleryScroll}
              className="flex snap-x snap-mandatory gap-4 overflow-x-auto scroll-smooth px-1 pb-2"
            >
              {game.images.map((image, index) => (
                <motion.button
                  key={image.id}
                  type="button"
                  onClick={() => setLightboxIndex(index)}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="group relative h-40 w-56 shrink-0 snap-start overflow-hidden rounded-2xl border border-line/70 shadow-card transition-colors duration-300 hover:border-accent/50"
                >
                  <img
                    src={mediaUrl(image.image) ?? ''}
                    alt={image.caption || game.title}
                    loading="lazy"
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-ink-950/80 via-ink-950/0 to-ink-950/0 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
                  <div className="absolute right-2.5 top-2.5 flex h-7 w-7 -translate-y-1 items-center justify-center rounded-full bg-ink-950/70 text-slate-100 opacity-0 backdrop-blur transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                    <ZoomIcon />
                  </div>
                  {image.caption && (
                    <div className="absolute inset-x-0 bottom-0 translate-y-2 p-2.5 text-left text-xs font-medium text-slate-100 opacity-0 transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                      {image.caption}
                    </div>
                  )}
                </motion.button>
              ))}
            </div>
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

      <Lightbox
        open={lightboxIndex !== null}
        index={lightboxIndex ?? 0}
        close={() => setLightboxIndex(null)}
        plugins={[Zoom, Captions, Thumbnails]}
        animation={{ swipe: 350 }}
        carousel={{ finite: true }}
        thumbnails={{ border: 0, borderRadius: 12, gap: 8, padding: 0, vignette: false }}
        render={{
          iconPrev: () => <ChevronLeftIcon />,
          iconNext: () => <ChevronRightIcon />,
        }}
        slides={game.images.map((image) => ({
          src: mediaUrl(image.image) ?? '',
          alt: image.caption || game.title,
          description: image.caption || undefined,
        }))}
      />
    </motion.article>
  )
}
