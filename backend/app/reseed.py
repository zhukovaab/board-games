"""Ручное обновление уже засеянных игр под текущий seed_data.py:

    python -m app.reseed

В отличие от app.seed (только добавляет новые записи и не трогает
существующие), это апсерт по slug: объективные поля — название,
title_original, обложка, описание, число игроков, возраст, время партии,
сложность, has_solo_mode, флаг дополнения, категории/темы/механики —
перезаписываются под текущее содержимое seed_data.py для КАЖДОЙ игры,
включая уже существующие. Личные поля (location, notes, best_players) при
обновлении существующей записи не трогаются — их заполняют через админку,
и этот скрипт их не затрёт.

Запускать только вручную, когда сознательно хочешь дотянуть до базы правки
описаний/тегов/обложек, которые я внесла в seed_data.py уже после того, как
игра была засеяна. Не подключён к SEED_ON_START и не запускается сам по
себе при деплое.
"""
from __future__ import annotations

import asyncio

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
        item = existing.get(slug)
        if item is None:
            item = model(name=name, slug=slug, description=description)
            session.add(item)
            existing[slug] = item
        else:
            item.name = name
            item.description = description
    await session.flush()
    return existing


async def _apply_game(
    session: AsyncSession,
    data: dict,
    categories: dict,
    themes: dict,
    mechanics: dict,
    existing_games: dict,
) -> bool:
    """Создаёт игру или обновляет уже существующую (по slug). Возвращает
    True, если запись была создана заново."""
    slug = data["slug"]
    game = existing_games.get(slug)
    is_new = game is None
    if game is None:
        game = Game(slug=slug)
        session.add(game)
        existing_games[slug] = game

    game.title = data["title"]
    game.title_original = data.get("title_original", "")
    game.cover = data.get("cover", "")
    game.description = data.get("description", "")
    game.min_players = data.get("min_players", 1)
    game.max_players = data.get("max_players", 4)
    game.playtime = data.get("playtime")
    game.min_age = data.get("min_age")
    game.complexity = data.get("complexity")
    game.has_solo_mode = data.get("has_solo_mode", False)
    game.is_expansion = bool(data.get("base_game"))

    if is_new:
        # Личные поля — только при первом создании, чтобы не затирать
        # то, что потом впишут через админку.
        game.best_players = data.get("best_players", "")
        game.location = data.get("location", "")
        game.notes = data.get("notes", "")

    base_slug = data.get("base_game")
    if base_slug:
        # Назначаем FK напрямую: relationship объявлен с lazy="raise".
        game.base_game_id = existing_games[base_slug].id

    game.categories = [categories[s] for s in data.get("categories", [])]
    game.themes = [themes[s] for s in data.get("themes", [])]
    game.mechanics = [mechanics[s] for s in data.get("mechanics", [])]
    return is_new


async def reseed() -> None:
    async with session_factory() as session:
        categories = await _sync_taxonomy(session, Category, CATEGORIES)
        themes = await _sync_taxonomy(session, Theme, THEMES)
        mechanics = await _sync_taxonomy(session, Mechanic, MECHANICS)

        existing_games = {
            game.slug: game for game in (await session.execute(select(Game))).scalars()
        }

        created = updated = 0
        for data in GAMES:
            is_new = await _apply_game(
                session, data, categories, themes, mechanics, existing_games
            )
            created += is_new
            updated += not is_new

        await session.flush()

        for data in EXPANSIONS:
            if data["base_game"] not in existing_games:
                continue
            is_new = await _apply_game(
                session, data, categories, themes, mechanics, existing_games
            )
            created += is_new
            updated += not is_new

        await session.commit()
        print(
            f"Готово. Добавлено игр: {created}. Обновлено: {updated}. "
            f"Всего в базе: {len(existing_games)}."
        )


if __name__ == "__main__":
    asyncio.run(reseed())
