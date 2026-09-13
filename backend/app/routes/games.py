"""Каталог игр: список с фильтрами и детальная карточка."""
from __future__ import annotations

from typing import Annotated, Literal

from litestar import get
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from sqlalchemy import Select, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Category, Game, Mechanic, Theme, game_categories, game_mechanics, game_themes
from app.schemas import GameDetail, GamesPage, game_detail, game_list_item

SortKey = Literal[
    "title", "-title", "complexity", "-complexity", "playtime", "-playtime", "new", "old"
]

SORT_MAP = {
    "title": (Game.title.asc(),),
    "-title": (Game.title.desc(),),
    "complexity": (Game.complexity.asc().nulls_last(), Game.title.asc()),
    "-complexity": (Game.complexity.desc().nulls_last(), Game.title.asc()),
    "playtime": (Game.playtime.asc().nulls_last(), Game.title.asc()),
    "-playtime": (Game.playtime.desc().nulls_last(), Game.title.asc()),
    "new": (Game.id.desc(),),
    "old": (Game.id.asc(),),
}


def _taxonomy_filter(
    stmt: Select, table, model, column: str, slugs: list[str] | None
) -> Select:
    """Игра должна быть связана хотя бы с одним из выбранных значений справочника."""
    if not slugs:
        return stmt
    exists = (
        select(1)
        .select_from(table.join(model, table.c[column] == model.id))
        .where(table.c.game_id == Game.id, model.slug.in_(slugs))
        .exists()
    )
    return stmt.where(exists)


def _apply_filters(
    stmt: Select,
    *,
    search: str | None,
    players: int | None,
    playtime_max: int | None,
    age: int | None,
    complexity_min: float | None,
    complexity_max: float | None,
    categories: list[str] | None,
    themes: list[str] | None,
    mechanics: list[str] | None,
    solo: bool | None,
    expansions: str,
) -> Select:
    if search:
        pattern = f"%{search.strip()}%"
        stmt = stmt.where(
            or_(
                Game.title.ilike(pattern),
                Game.title_original.ilike(pattern),
                Game.description.ilike(pattern),
            )
        )
    if players:
        stmt = stmt.where(Game.min_players <= players, Game.max_players >= players)
    if playtime_max:
        stmt = stmt.where(Game.playtime.is_not(None), Game.playtime <= playtime_max)
    if age is not None:
        stmt = stmt.where(Game.min_age.is_not(None), Game.min_age <= age)
    if complexity_min is not None:
        stmt = stmt.where(Game.complexity.is_not(None), Game.complexity >= complexity_min)
    if complexity_max is not None:
        stmt = stmt.where(Game.complexity.is_not(None), Game.complexity <= complexity_max)
    if solo:
        stmt = stmt.where(Game.has_solo_mode.is_(True))

    stmt = _taxonomy_filter(stmt, game_categories, Category, "category_id", categories)
    stmt = _taxonomy_filter(stmt, game_themes, Theme, "theme_id", themes)
    stmt = _taxonomy_filter(stmt, game_mechanics, Mechanic, "mechanic_id", mechanics)

    if expansions == "hide":
        stmt = stmt.where(Game.is_expansion.is_(False))
    elif expansions == "only":
        stmt = stmt.where(Game.is_expansion.is_(True))
    return stmt


@get("/games", summary="Список игр с фильтрами")
async def list_games(
    session: AsyncSession,
    search: Annotated[str | None, Parameter(query="search")] = None,
    players: int | None = None,
    playtime_max: int | None = None,
    age: int | None = None,
    complexity_min: float | None = None,
    complexity_max: float | None = None,
    categories: list[str] | None = None,
    themes: list[str] | None = None,
    mechanics: list[str] | None = None,
    solo: bool | None = None,
    expansions: Literal["hide", "show", "only"] = "hide",
    sort: SortKey = "title",
    page: int = 1,
    page_size: int = 24,
) -> GamesPage:
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)

    filters = {
        "search": search,
        "players": players,
        "playtime_max": playtime_max,
        "age": age,
        "complexity_min": complexity_min,
        "complexity_max": complexity_max,
        "categories": categories,
        "themes": themes,
        "mechanics": mechanics,
        "solo": solo,
        "expansions": expansions,
    }

    # Счётчики считаем без учёта переключателя дополнений — он про то, что показать
    # в выдаче, а не про то, сколько всего подходит под фильтры.
    counts_stmt = _apply_filters(
        select(
            func.count(Game.id).filter(Game.is_expansion.is_(False)),
            func.count(Game.id).filter(Game.is_expansion.is_(True)),
        ),
        **{**filters, "expansions": "show"},
    )
    counts = (await session.execute(counts_stmt)).one()
    total_games, total_expansions = int(counts[0]), int(counts[1])
    total = {
        "hide": total_games,
        "only": total_expansions,
    }.get(expansions, total_games + total_expansions)

    stmt = _apply_filters(select(Game), **filters)
    stmt = stmt.order_by(*SORT_MAP[sort]).limit(page_size).offset((page - 1) * page_size)
    games = (await session.execute(stmt)).scalars().unique().all()

    return GamesPage(
        items=[game_list_item(game) for game in games],
        total=total,
        total_games=total_games,
        total_expansions=total_expansions,
        page=page,
        page_size=page_size,
        pages=max((total + page_size - 1) // page_size, 1),
    )


@get("/games/{slug:str}", summary="Детальная карточка игры")
async def get_game(session: AsyncSession, slug: str) -> GameDetail:
    stmt = (
        select(Game)
        .where(Game.slug == slug)
        .options(selectinload(Game.base_game), selectinload(Game.expansions))
    )
    game = (await session.execute(stmt)).scalars().unique().one_or_none()
    if game is None:
        raise NotFoundException(detail=f"Игра «{slug}» не найдена")
    return game_detail(game)
