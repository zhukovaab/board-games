export interface Taxonomy {
  id: number
  name: string
  slug: string
  description?: string
}

export interface TaxonomyWithCount {
  id: number
  name: string
  slug: string
  games_count: number
}

export interface GameImage {
  id: number
  image: string | null
  caption: string
  order: number
}

export interface GameBrief {
  id: number
  title: string
  slug: string
  cover: string | null
}

export interface GameListItem {
  id: number
  title: string
  title_original: string
  slug: string
  cover: string | null
  min_players: number
  max_players: number
  best_players: string
  playtime: number | null
  min_age: number | null
  complexity: number | null
  has_solo_mode: boolean
  is_expansion: boolean
  categories: Taxonomy[]
  themes: Taxonomy[]
  mechanics: Taxonomy[]
}

export interface GameDetail extends GameListItem {
  description: string
  location: string
  notes: string
  rules_url: string
  rules_file: string | null
  images: GameImage[]
  base_game: GameBrief | null
  expansions: GameBrief[]
}

export interface GamesPage {
  items: GameListItem[]
  total: number
  total_games: number
  total_expansions: number
  page: number
  page_size: number
  pages: number
}

export interface FiltersMeta {
  categories: TaxonomyWithCount[]
  themes: TaxonomyWithCount[]
  mechanics: TaxonomyWithCount[]
  max_players: number
  max_playtime: number
  min_age_min: number
  min_age_max: number
  total_games: number
  total_expansions: number
}
