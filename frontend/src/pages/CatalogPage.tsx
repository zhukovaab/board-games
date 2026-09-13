import { useQuery } from '@tanstack/react-query'
import { AnimatePresence, motion } from 'framer-motion'
import { useCallback, useState } from 'react'

import { api } from '../api/client'
import { FiltersPanel } from '../components/FiltersPanel'
import { GameCard } from '../components/GameCard'
import { Pagination } from '../components/Pagination'
import { SearchBar } from '../components/SearchBar'
import { GridSkeleton } from '../components/Skeletons'
import { SortSelect } from '../components/SortSelect'
import { useCatalogParams } from '../hooks/useCatalogParams'
import { plural } from '../lib/format'

export function CatalogPage() {
  const { state, update, toggleInList, reset, activeCount, apiParams } = useCatalogParams()
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false)

  const filtersQuery = useQuery({
    queryKey: ['filters'],
    queryFn: api.filters,
    staleTime: 5 * 60 * 1000,
  })

  const gamesQuery = useQuery({
    queryKey: ['games', apiParams.toString()],
    queryFn: () => api.games(apiParams),
    placeholderData: (previous) => previous,
  })

  const onSearch = useCallback((value: string) => update({ q: value }), [update])

  const total = gamesQuery.data?.total ?? 0
  const shelfGames = gamesQuery.data?.total_games ?? 0
  const shelfExpansions = gamesQuery.data?.total_expansions ?? 0
  const shelfLabel = gamesQuery.data
    ? [
        `${shelfGames} ${plural(shelfGames, ['игра', 'игры', 'игр'])}`,
        shelfExpansions > 0 &&
          `${shelfExpansions} ${plural(shelfExpansions, ['дополнение', 'дополнения', 'дополнений'])}`,
      ]
        .filter(Boolean)
        .join(' и ')
    : ''
  const panel = (
    <FiltersPanel
      meta={filtersQuery.data}
      state={state}
      update={update}
      toggleInList={toggleInList}
      reset={reset}
      activeCount={activeCount}
    />
  )

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="gradient-text text-3xl font-extrabold tracking-tight sm:text-4xl">
          Настольные игры
        </h1>
        {/* min-h держит строку до первой загрузки, чтобы ничего не прыгало. */}
        <p className="min-h-5 text-sm text-mist">
          {shelfLabel}
          <span
            className={`text-accent-soft transition-opacity duration-200 ${
              gamesQuery.isFetching && !gamesQuery.isLoading ? 'opacity-100' : 'opacity-0'
            }`}
          >
            {' · обновляем…'}
          </span>
        </p>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <SearchBar value={state.q} onChange={onSearch} />
        <div className="flex w-full items-center gap-3 sm:w-auto">
          <SortSelect value={state.sort} onChange={(value) => update({ sort: value })} />
          <button
            type="button"
            onClick={() => setMobileFiltersOpen(true)}
            className="chip shrink-0 lg:hidden"
          >
            Фильтры{activeCount > 0 ? ` · ${activeCount}` : ''}
          </button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-[300px_1fr]">
        {/* Никакой своей прокрутки: панель едет вместе со страницей, скролл один на всех. */}
        <aside className="hidden lg:block">{panel}</aside>

        <section>
          {gamesQuery.isLoading ? (
            <GridSkeleton />
          ) : gamesQuery.isError ? (
            <div className="panel p-10 text-center text-sm text-mist">
              Не получилось загрузить игры. Проверь, запущен ли бэкенд.
            </div>
          ) : total === 0 ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              className="panel flex flex-col items-center gap-3 p-14 text-center"
            >
              <div className="text-4xl">🎲</div>
              <p className="text-sm text-mist">
                Под такие условия на полке ничего нет.
              </p>
              {(activeCount > 0 || state.q) && (
                <button type="button" onClick={reset} className="chip chip-active">
                  сбросить фильтры
                </button>
              )}
            </motion.div>
          ) : (
            <motion.div
              layout
              className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5"
            >
              <AnimatePresence mode="popLayout">
                {gamesQuery.data?.items.map((game, index) => (
                  <GameCard key={game.id} game={game} index={index} />
                ))}
              </AnimatePresence>
            </motion.div>
          )}

          <Pagination
            page={gamesQuery.data?.page ?? 1}
            pages={gamesQuery.data?.pages ?? 1}
            onChange={(page) => {
              update({ page })
              window.scrollTo({ top: 0, behavior: 'smooth' })
            }}
          />
        </section>
      </div>

      <AnimatePresence>
        {mobileFiltersOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileFiltersOpen(false)}
              className="fixed inset-0 z-40 bg-ink-950/80 backdrop-blur-sm lg:hidden"
            />
            <motion.div
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              transition={{ type: 'spring', stiffness: 320, damping: 34 }}
              className="fixed inset-x-0 bottom-0 z-50 max-h-[85vh] overflow-y-auto rounded-t-3xl border-t border-line bg-ink-900 p-4 lg:hidden"
            >
              <div className="mx-auto mb-3 h-1 w-10 rounded-full bg-ink-600" />
              {panel}
              <button
                type="button"
                onClick={() => setMobileFiltersOpen(false)}
                className="mt-4 w-full rounded-xl bg-accent-gradient py-3 text-sm font-bold text-ink-950"
              >
                Показать {total} {plural(total, ['игру', 'игры', 'игр'])}
              </button>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}
