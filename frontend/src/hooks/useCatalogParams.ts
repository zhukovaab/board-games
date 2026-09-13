import { useCallback, useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'

export type ExpansionsMode = 'hide' | 'show' | 'only'

export interface CatalogState {
  q: string
  players: number | null
  time: number | null
  age: number | null
  cmin: number | null
  cmax: number | null
  cat: string[]
  theme: string[]
  mech: string[]
  solo: boolean
  exp: ExpansionsMode
  sort: string
  page: number
}

const DEFAULTS: CatalogState = {
  q: '',
  players: null,
  time: null,
  age: null,
  cmin: null,
  cmax: null,
  cat: [],
  theme: [],
  mech: [],
  solo: false,
  exp: 'hide',
  sort: 'title',
  page: 1,
}

function num(value: string | null): number | null {
  if (value === null || value === '') return null
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : null
}

export function useCatalogParams() {
  const [searchParams, setSearchParams] = useSearchParams()

  const state = useMemo<CatalogState>(() => {
    const exp = searchParams.get('exp')
    return {
      q: searchParams.get('q') ?? '',
      players: num(searchParams.get('players')),
      time: num(searchParams.get('time')),
      age: num(searchParams.get('age')),
      cmin: num(searchParams.get('cmin')),
      cmax: num(searchParams.get('cmax')),
      cat: searchParams.getAll('cat'),
      theme: searchParams.getAll('theme'),
      mech: searchParams.getAll('mech'),
      solo: searchParams.get('solo') === '1',
      exp: exp === 'show' || exp === 'only' ? exp : 'hide',
      sort: searchParams.get('sort') ?? DEFAULTS.sort,
      page: num(searchParams.get('page')) ?? 1,
    }
  }, [searchParams])

  const update = useCallback(
    (patch: Partial<CatalogState>, options?: { keepPage?: boolean }) => {
      const next = { ...state, ...patch }
      if (!options?.keepPage && !('page' in patch)) next.page = 1

      const params = new URLSearchParams()
      if (next.q.trim()) params.set('q', next.q.trim())
      if (next.players) params.set('players', String(next.players))
      if (next.time) params.set('time', String(next.time))
      if (next.age !== null) params.set('age', String(next.age))
      if (next.cmin !== null) params.set('cmin', String(next.cmin))
      if (next.cmax !== null) params.set('cmax', String(next.cmax))
      next.cat.forEach((value) => params.append('cat', value))
      next.theme.forEach((value) => params.append('theme', value))
      next.mech.forEach((value) => params.append('mech', value))
      if (next.solo) params.set('solo', '1')
      if (next.exp !== 'hide') params.set('exp', next.exp)
      if (next.sort !== DEFAULTS.sort) params.set('sort', next.sort)
      if (next.page > 1) params.set('page', String(next.page))

      setSearchParams(params, { replace: true })
    },
    [state, setSearchParams],
  )

  const toggleInList = useCallback(
    (key: 'cat' | 'theme' | 'mech', value: string) => {
      const current = state[key]
      const next = current.includes(value)
        ? current.filter((item) => item !== value)
        : [...current, value]
      update({ [key]: next } as Partial<CatalogState>)
    },
    [state, update],
  )

  const reset = useCallback(() => setSearchParams(new URLSearchParams(), { replace: true }), [
    setSearchParams,
  ])

  const activeCount = useMemo(() => {
    let count = 0
    if (state.players) count += 1
    if (state.time) count += 1
    if (state.age !== null) count += 1
    if (state.cmin !== null || state.cmax !== null) count += 1
    if (state.solo) count += 1
    if (state.exp !== 'hide') count += 1
    count += state.cat.length + state.theme.length + state.mech.length
    return count
  }, [state])

  const apiParams = useMemo(() => {
    const params = new URLSearchParams()
    if (state.q.trim()) params.set('search', state.q.trim())
    if (state.players) params.set('players', String(state.players))
    if (state.time) params.set('playtime_max', String(state.time))
    if (state.age !== null) params.set('age', String(state.age))
    if (state.cmin !== null) params.set('complexity_min', String(state.cmin))
    if (state.cmax !== null) params.set('complexity_max', String(state.cmax))
    state.cat.forEach((value) => params.append('categories', value))
    state.theme.forEach((value) => params.append('themes', value))
    state.mech.forEach((value) => params.append('mechanics', value))
    if (state.solo) params.set('solo', 'true')
    params.set('expansions', state.exp)
    params.set('sort', state.sort)
    params.set('page', String(state.page))
    params.set('page_size', '24')
    return params
  }, [state])

  return { state, update, toggleInList, reset, activeCount, apiParams }
}
