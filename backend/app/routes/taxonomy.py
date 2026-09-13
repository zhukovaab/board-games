"""Справочники и границы диапазонов — всё, что нужно панели фильтров."""
from __future__ import annotations

from litestar import get
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Category,
    Game,
    Mechanic,
    Theme,
    game_categories,
    game_mechanics,
    game_themes,
)
from app.schemas import FiltersOut, TaxonomyWithCount


async def _with_counts(session: AsyncSession, model, table, column: str) -> list[TaxonomyWithCount]:
    stmt = (
        select(model.id, model.name, model.slug, func.count(table.c.game_id))
        .select_from(model)
        .outerjoin(table, table.c[column] == model.id)
        .group_by(model.id, model.name, model.slug)
        .order_by(model.name)
    )
    rows = (await session.execute(stmt)).all()
    return [
        TaxonomyWithCount(id=row[0], name=row[1], slug=row[2], games_count=row[3])
        for row in rows
    ]


@get("/filters", summary="Справочники и границы фильтров")
async def get_filters(session: AsyncSession) -> FiltersOut:
    categories = await _with_counts(session, Category, game_categories, "category_id")
    themes = await _with_counts(session, Theme, game_themes, "theme_id")
    mechanics = await _with_counts(session, Mechanic, game_mechanics, "mechanic_id")

    bounds = (
        await session.execute(
            select(
                func.coalesce(func.max(Game.max_players), 8),
                func.coalesce(func.max(Game.playtime), 180),
                func.coalesce(func.min(Game.min_age), 3),
                func.coalesce(func.max(Game.min_age), 18),
                func.count(Game.id).filter(Game.is_expansion.is_(False)),
                func.count(Game.id).filter(Game.is_expansion.is_(True)),
            )
        )
    ).one()

    return FiltersOut(
        categories=categories,
        themes=themes,
        mechanics=mechanics,
        max_players=int(bounds[0]),
        max_playtime=int(bounds[1]),
        min_age_min=int(bounds[2]),
        min_age_max=int(bounds[3]),
        total_games=int(bounds[4]),
        total_expansions=int(bounds[5]),
    )
