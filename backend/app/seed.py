"""Наполнение базы демо-данными: python -m app.seed

Скрипт идемпотентен: существующие записи (ищутся по slug) не перезаписываются.
"""
from __future__ import annotations

import asyncio
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import session_factory
from app.models import Category, Game, Mechanic, Theme
from app.seed_data import CATEGORIES, EXPANSIONS, GAMES, MECHANICS, THEMES


async def _sync_taxonomy(session: AsyncSession, model, rows) -> dict[str, object]:
    existing = {
        item.slug: item for item in (await session.execute(select(model))).scalars()
    }
    for name, slug, description in rows:
        if slug in existing:
            continue
        item = model(name=name, slug=slug, description=description)
        session.add(item)
        existing[slug] = item
    await session.flush()
    return existing


async def _create_game(
    session: AsyncSession,
    data: dict,
    categories: dict,
    themes: dict,
    mechanics: dict,
    base_games: dict,
) -> Game:
    game = Game(
        title=data["title"],
        title_original=data.get("title_original", ""),
        slug=data["slug"],
        description=data.get("description", ""),
        min_players=data.get("min_players", 1),
        max_players=data.get("max_players", 4),
        best_players=data.get("best_players", ""),
        playtime=data.get("playtime"),
        min_age=data.get("min_age"),
        complexity=Decimal(data["complexity"]) if data.get("complexity") else None,
        has_solo_mode=data.get("has_solo_mode", False),
        is_expansion=bool(data.get("base_game")),
        location=data.get("location", ""),
        notes=data.get("notes", ""),
    )
    base_slug = data.get("base_game")
    if base_slug:
        # Назначаем FK напрямую: relationship объявлен с lazy="raise".
        game.base_game_id = base_games[base_slug].id
    game.categories = [categories[s] for s in data.get("categories", [])]
    game.themes = [themes[s] for s in data.get("themes", [])]
    game.mechanics = [mechanics[s] for s in data.get("mechanics", [])]
    session.add(game)
    return game


async def seed() -> None:
    async with session_factory() as session:
        categories = await _sync_taxonomy(session, Category, CATEGORIES)
        themes = await _sync_taxonomy(session, Theme, THEMES)
        mechanics = await _sync_taxonomy(session, Mechanic, MECHANICS)

        existing_games = {
            game.slug: game for game in (await session.execute(select(Game))).scalars()
        }

        created = 0
        for data in GAMES:
            if data["slug"] in existing_games:
                continue
            game = await _create_game(
                session, data, categories, themes, mechanics, existing_games
            )
            existing_games[data["slug"]] = game
            created += 1

        await session.flush()

        for data in EXPANSIONS:
            if data["slug"] in existing_games:
                continue
            if data["base_game"] not in existing_games:
                continue
            game = await _create_game(
                session, data, categories, themes, mechanics, existing_games
            )
            existing_games[data["slug"]] = game
            created += 1

        await session.commit()
        print(f"Готово. Добавлено игр: {created}. Всего в базе: {len(existing_games)}.")


if __name__ == "__main__":
    asyncio.run(seed())
