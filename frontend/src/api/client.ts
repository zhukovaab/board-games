import type { FiltersMeta, GameDetail, GamesPage } from './types'

const API_URL = (import.meta.env.VITE_API_URL ?? 'http://localhost:8000').replace(/\/$/, '')

export function mediaUrl(path: string | null): string | null {
  if (!path) return null
  if (path.startsWith('http')) return path
  return `${API_URL}${path}`
}

async function request<T>(path: string, params?: URLSearchParams): Promise<T> {
  const query = params && [...params.keys()].length ? `?${params.toString()}` : ''
  const response = await fetch(`${API_URL}/api${path}${query}`)
  if (!response.ok) {
    throw new Error(
      response.status === 404 ? 'Не найдено' : `Ошибка запроса: ${response.status}`,
    )
  }
  return (await response.json()) as T
}

export const api = {
  games: (params: URLSearchParams) => request<GamesPage>('/games', params),
  game: (slug: string) => request<GameDetail>(`/games/${slug}`),
  filters: () => request<FiltersMeta>('/filters'),
}
