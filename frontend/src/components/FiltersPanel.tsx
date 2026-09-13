import { AnimatePresence, motion } from 'framer-motion'
import { useState, type ReactNode } from 'react'

import type { FiltersMeta, TaxonomyWithCount } from '../api/types'
import type { CatalogState, ExpansionsMode } from '../hooks/useCatalogParams'
import { playtimeLabel, plural } from '../lib/format'
import { DualRangeSlider, RangeSlider } from './RangeSlider'

interface Props {
  meta: FiltersMeta | undefined
  state: CatalogState
  update: (patch: Partial<CatalogState>) => void
  toggleInList: (key: 'cat' | 'theme' | 'mech', value: string) => void
  reset: () => void
  activeCount: number
}

const EXPANSION_OPTIONS: { label: string; value: ExpansionsMode }[] = [
  { label: 'только базовые игры', value: 'hide' },
  { label: 'игры и дополнения к ним', value: 'show' },
  { label: 'только дополнения', value: 'only' },
]

const COMPLEXITY_MIN = 1
const COMPLEXITY_MAX = 5
const TIME_STEP = 15

function Section({
  title,
  children,
  defaultOpen = true,
}: {
  title: string
  children: ReactNode
  defaultOpen?: boolean
}) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="border-b border-line/70 py-4 last:border-none">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="flex w-full items-center justify-between text-left"
      >
        <span className="text-xs font-bold uppercase tracking-[0.14em] text-mist">{title}</span>
        <motion.span
          animate={{ rotate: open ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="text-mist"
        >
          ▾
        </motion.span>
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
            className="overflow-hidden"
          >
            <div className="pt-3">{children}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

function ChipButton({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: ReactNode
}) {
  return (
    <motion.button
      type="button"
      onClick={onClick}
      whileTap={{ scale: 0.94 }}
      className={`chip ${active ? 'chip-active' : 'hover:border-accent/40 hover:text-slate-200'}`}
    >
      {children}
    </motion.button>
  )
}

function TaxonomyGroup({
  items,
  selected,
  onToggle,
}: {
  items: TaxonomyWithCount[]
  selected: string[]
  onToggle: (slug: string) => void
}) {
  const [expanded, setExpanded] = useState(false)
  const visible = expanded ? items : items.slice(0, 8)

  return (
    <div className="flex flex-wrap gap-2">
      {visible.map((item) => (
        <ChipButton
          key={item.slug}
          active={selected.includes(item.slug)}
          onClick={() => onToggle(item.slug)}
        >
          {item.name}
          <span className="text-[10px] opacity-60">{item.games_count}</span>
        </ChipButton>
      ))}
      {items.length > 8 && (
        <button
          type="button"
          onClick={() => setExpanded((value) => !value)}
          className="text-xs font-medium text-accent-soft transition-opacity hover:opacity-80"
        >
          {expanded ? 'свернуть' : `ещё ${items.length - 8}`}
        </button>
      )}
    </div>
  )
}

export function FiltersPanel({
  meta,
  state,
  update,
  toggleInList,
  reset,
  activeCount,
}: Props) {
  const maxPlayers = Math.min(meta?.max_players ?? 8, 10)
  const maxTime = Math.min(
    Math.ceil((meta?.max_playtime ?? 180) / TIME_STEP) * TIME_STEP,
    240,
  )
  const minAge = Math.max(meta?.min_age_min ?? 4, 3)
  const maxAge = Math.max(meta?.min_age_max ?? 16, minAge + 1)

  return (
    <div className="panel p-5">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-bold text-slate-100">Фильтры</h2>
        <AnimatePresence>
          {activeCount > 0 && (
            <motion.button
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              type="button"
              onClick={reset}
              className="text-xs font-medium text-blush transition-opacity hover:opacity-80"
            >
              сбросить ({activeCount})
            </motion.button>
          )}
        </AnimatePresence>
      </div>

      <Section title="Количество игроков">
        <RangeSlider
          value={state.players}
          min={1}
          max={maxPlayers}
          ariaLabel="Количество игроков"
          format={(value) => `${value} ${plural(value, ['игрок', 'игрока', 'игроков'])}`}
          onChange={(value) => update({ players: value })}
        />
      </Section>

      <Section title="Время партии">
        <RangeSlider
          value={state.time}
          min={TIME_STEP}
          max={maxTime}
          step={TIME_STEP}
          ariaLabel="Время партии"
          format={(value) => `до ${playtimeLabel(value)}`}
          onChange={(value) => update({ time: value })}
        />
      </Section>

      <Section title="Возраст">
        <RangeSlider
          value={state.age}
          min={minAge}
          max={maxAge}
          ariaLabel="Возраст"
          format={(value) => `от ${value} лет`}
          onChange={(value) => update({ age: value })}
        />
      </Section>

      <Section title="Сложность">
        <DualRangeSlider
          from={state.cmin}
          to={state.cmax}
          min={COMPLEXITY_MIN}
          max={COMPLEXITY_MAX}
          ariaLabel="Сложность"
          format={(from, to) => `${from.toFixed(1)}–${to.toFixed(1)} из 5`}
          onChange={(from, to) => update({ cmin: from, cmax: to })}
        />
      </Section>

      <Section title="Категория">
        <TaxonomyGroup
          items={meta?.categories ?? []}
          selected={state.cat}
          onToggle={(slug) => toggleInList('cat', slug)}
        />
      </Section>

      <Section title="Тематика">
        <TaxonomyGroup
          items={meta?.themes ?? []}
          selected={state.theme}
          onToggle={(slug) => toggleInList('theme', slug)}
        />
      </Section>

      <Section title="Механика">
        <TaxonomyGroup
          items={meta?.mechanics ?? []}
          selected={state.mech}
          onToggle={(slug) => toggleInList('mech', slug)}
        />
      </Section>

      <Section title="Игра в одиночку">
        <ChipButton active={state.solo} onClick={() => update({ solo: !state.solo })}>
          есть соло-режим
        </ChipButton>
      </Section>

      <Section title="Дополнения">
        {/* Радиогруппа, а не чипы: режим всегда ровно один, и видно, какой именно. */}
        <div role="radiogroup" aria-label="Дополнения" className="space-y-0.5">
          {EXPANSION_OPTIONS.map((option) => {
            const active = state.exp === option.value
            return (
              <button
                key={option.value}
                type="button"
                role="radio"
                aria-checked={active}
                onClick={() => update({ exp: option.value })}
                className={`flex w-full items-center gap-2.5 rounded-lg px-2 py-2 text-left text-sm
                            transition-colors duration-150 ${
                              active
                                ? 'bg-accent/10 text-slate-50'
                                : 'text-mist hover:bg-ink-800/60 hover:text-slate-200'
                            }`}
              >
                <span
                  className={`grid h-4 w-4 shrink-0 place-items-center rounded-full border transition-colors
                              ${active ? 'border-accent-soft' : 'border-ink-600'}`}
                >
                  {active && (
                    <motion.span
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring', stiffness: 480, damping: 24 }}
                      className="h-2 w-2 rounded-full bg-accent-gradient"
                    />
                  )}
                </span>
                {option.label}
              </button>
            )
          })}
        </div>
      </Section>
    </div>
  )
}
