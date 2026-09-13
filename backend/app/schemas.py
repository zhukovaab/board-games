"""Схемы ответов API и конвертеры из ORM-моделей."""
from __future__ import annotations

import msgspec

from app.config import settings
from app.models import Game, GameImage, Mechanic, Theme, Category


def media_url(path: str) -> str | None:
    if not path:
        return None
    return f"{settings.media_url_path}/{path.lstrip('/')}"


class TaxonomyOut(msgspec.Struct):
    id: int
    name: str
    slug: str
    description: str = ""
    games_count: int | None = None


class TaxonomyWithCount(msgspec.Struct):
    id: int
    name: str
    slug: str
    games_count: int


class GameImageOut(msgspec.Struct):
    id: int
    image: str | None
    caption: str
    order: int


class GameBrief(msgspec.Struct):
    id: int
    title: str
    slug: str
    cover: str | None


class GameListItem(msgspec.Struct):
    id: int
    title: str
    title_original: str
    slug: str
    cover: str | None
    min_players: int
    max_players: int
    best_players: str
    playtime: int | None
    min_age: int | None
    complexity: float | None
    has_solo_mode: bool
    is_expansion: bool
    categories: list[TaxonomyOut]
    themes: list[TaxonomyOut]
    mechanics: list[TaxonomyOut]


class GameDetail(GameListItem):
    description: str = ""
    location: str = ""
    notes: str = ""
    rules_url: str = ""
    rules_file: str | None = None
    images: list[GameImageOut] = []
    base_game: GameBrief | None = None
    expansions: list[GameBrief] = []


class GamesPage(msgspec.Struct):
    items: list[GameListItem]
    total: int
    total_games: int
    total_expansions: int
    page: int
    page_size: int
    pages: int


class FiltersOut(msgspec.Struct):
    categories: list[TaxonomyWithCount]
    themes: list[TaxonomyWithCount]
    mechanics: list[TaxonomyWithCount]
    max_players: int
    max_playtime: int
    min_age_min: int
    min_age_max: int
    total_games: int
    total_expansions: int


def taxonomy_out(item: Category | Theme | Mechanic) -> TaxonomyOut:
    return TaxonomyOut(
        id=item.id, name=item.name, slug=item.slug, description=item.description
    )


def image_out(item: GameImage) -> GameImageOut:
    return GameImageOut(
        id=item.id,
        image=media_url(item.image),
        caption=item.caption,
        order=item.order,
    )


def game_brief(game: Game) -> GameBrief:
    return GameBrief(
        id=game.id, title=game.title, slug=game.slug, cover=media_url(game.cover)
    )


def _base_fields(game: Game) -> dict:
    return {
        "id": game.id,
        "title": game.title,
        "title_original": game.title_original,
        "slug": game.slug,
        "cover": media_url(game.cover),
        "min_players": game.min_players,
        "max_players": game.max_players,
        "best_players": game.best_players,
        "playtime": game.playtime,
        "min_age": game.min_age,
        "complexity": float(game.complexity) if game.complexity is not None else None,
        "has_solo_mode": game.has_solo_mode,
        "is_expansion": game.is_expansion,
        "categories": [taxonomy_out(i) for i in game.categories],
        "themes": [taxonomy_out(i) for i in game.themes],
        "mechanics": [taxonomy_out(i) for i in game.mechanics],
    }


def game_list_item(game: Game) -> GameListItem:
    return GameListItem(**_base_fields(game))


def game_detail(game: Game) -> GameDetail:
    return GameDetail(
        **_base_fields(game),
        description=game.description,
        location=game.location,
        notes=game.notes,
        rules_url=game.rules_url,
        rules_file=media_url(game.rules_file),
        images=[image_out(i) for i in game.images],
        base_game=game_brief(game.base_game) if game.base_game else None,
        expansions=[game_brief(i) for i in game.expansions],
    )
