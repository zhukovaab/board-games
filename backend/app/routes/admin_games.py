"""Запись данных под токеном: POST/PATCH/DELETE /api/admin/games.

Предназначено для автоматизации наполнения каталога (скрипты, импорт из BGG
и т.п.), а не для браузера — поэтому авторизация простым Bearer-токеном
(ADMIN_API_TOKEN), а не сессией Django. Обложка и фото галереи задаются
ссылками (cover/images.url) — загрузка файлов по-прежнему делается только
через Django-админку.
"""
from __future__ import annotations

import hmac

import msgspec
from litestar import Router, delete, patch, post
from litestar.connection import ASGIConnection
from litestar.exceptions import (
    ClientException,
    NotAuthorizedException,
    NotFoundException,
    PermissionDeniedException,
)
from litestar.handlers.base import BaseRouteHandler
from litestar.status_codes import HTTP_204_NO_CONTENT
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models import Category, Game, GameImage, GameVideo, Mechanic, Theme
from app.schemas import GameCreate, GameDetail, GameUpdate, game_detail

_UPDATE_FIELDS = (
    "title",
    "title_original",
    "cover",
    "description",
    "min_players",
    "max_players",
    "best_players",
    "playtime",
    "min_age",
    "complexity",
    "has_solo_mode",
    "location",
    "notes",
    "rules_url",
)


def require_admin_token(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    if not settings.admin_api_token:
        raise PermissionDeniedException(
            detail="ADMIN_API_TOKEN не задан на сервере — ручки записи отключены"
        )
    scheme, _, token = connection.headers.get("Authorization", "").partition(" ")
    if scheme.lower() != "bearer" or not hmac.compare_digest(token, settings.admin_api_token):
        raise NotAuthorizedException(detail="Нужен заголовок Authorization: Bearer <token>")


async def _taxonomy_by_names(session: AsyncSession, model, names: list[str]) -> list:
    """Находит справочники по названию; недостающие создаёт (как в Django-админке)."""
    if not names:
        return []
    existing = {
        item.name: item
        for item in (
            await session.execute(select(model).where(model.name.in_(names)))
        ).scalars()
    }
    result = []
    for name in names:
        item = existing.get(name)
        if item is None:
            item = model(name=name, slug=slugify(name)[:120])
            session.add(item)
            await session.flush()
            existing[name] = item
        result.append(item)
    return result


async def _unique_slug(session: AsyncSession, base_text: str, *, exclude_id: int | None = None) -> str:
    base = slugify(base_text)[:200] or "game"
    slug = base
    counter = 2
    while True:
        stmt = select(Game.id).where(Game.slug == slug)
        if exclude_id is not None:
            stmt = stmt.where(Game.id != exclude_id)
        if (await session.execute(stmt)).first() is None:
            return slug
        slug = f"{base}-{counter}"
        counter += 1


async def _resolve_base_game_id(session: AsyncSession, slug: str | None) -> int | None:
    if not slug:
        return None
    base_id = (await session.execute(select(Game.id).where(Game.slug == slug))).scalar_one_or_none()
    if base_id is None:
        raise NotFoundException(detail=f"base_game_slug «{slug}» не найден")
    return base_id


async def _load_detail(session: AsyncSession, game_id: int) -> GameDetail:
    stmt = (
        select(Game)
        .where(Game.id == game_id)
        .options(selectinload(Game.base_game), selectinload(Game.expansions))
    )
    game = (await session.execute(stmt)).scalars().unique().one()
    return game_detail(game)


@post("/games", summary="Создать игру (под токеном)")
async def create_game(session: AsyncSession, data: GameCreate) -> GameDetail:
    slug = data.slug or await _unique_slug(session, data.title_original or data.title)
    base_game_id = await _resolve_base_game_id(session, data.base_game_slug)

    game = Game(
        title=data.title,
        title_original=data.title_original,
        slug=slug,
        cover=data.cover,
        description=data.description,
        min_players=data.min_players,
        max_players=data.max_players,
        best_players=data.best_players,
        playtime=data.playtime,
        min_age=data.min_age,
        complexity=data.complexity,
        has_solo_mode=data.has_solo_mode,
        is_expansion=base_game_id is not None,
        base_game_id=base_game_id,
        location=data.location,
        notes=data.notes,
        rules_url=data.rules_url,
    )
    game.categories = await _taxonomy_by_names(session, Category, data.categories)
    game.themes = await _taxonomy_by_names(session, Theme, data.themes)
    game.mechanics = await _taxonomy_by_names(session, Mechanic, data.mechanics)
    game.videos = [GameVideo(url=v.url, title=v.title, order=v.order) for v in data.videos]
    game.images = [
        GameImage(image=i.url, caption=i.caption, order=i.order) for i in data.images
    ]

    session.add(game)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ClientException(detail=f"Игру с таким slug/полями не создать: {exc.orig}") from exc

    return await _load_detail(session, game.id)


@patch("/games/{game_id:int}", summary="Изменить игру (под токеном)")
async def update_game(session: AsyncSession, game_id: int, data: GameUpdate) -> GameDetail:
    game = await session.get(Game, game_id)
    if game is None:
        raise NotFoundException(detail=f"Игра #{game_id} не найдена")

    for attr in _UPDATE_FIELDS:
        value = getattr(data, attr)
        if value is not msgspec.UNSET:
            setattr(game, attr, value)

    if data.slug is not msgspec.UNSET:
        game.slug = data.slug or await _unique_slug(
            session, game.title_original or game.title, exclude_id=game.id
        )

    if data.base_game_slug is not msgspec.UNSET:
        game.base_game_id = await _resolve_base_game_id(session, data.base_game_slug)
        game.is_expansion = game.base_game_id is not None

    if data.categories is not msgspec.UNSET:
        game.categories = await _taxonomy_by_names(session, Category, data.categories)
    if data.themes is not msgspec.UNSET:
        game.themes = await _taxonomy_by_names(session, Theme, data.themes)
    if data.mechanics is not msgspec.UNSET:
        game.mechanics = await _taxonomy_by_names(session, Mechanic, data.mechanics)
    if data.videos is not msgspec.UNSET:
        game.videos = [GameVideo(url=v.url, title=v.title, order=v.order) for v in data.videos]
    if data.images is not msgspec.UNSET:
        game.images = [
            GameImage(image=i.url, caption=i.caption, order=i.order) for i in data.images
        ]

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ClientException(detail=f"Не удалось сохранить: {exc.orig}") from exc

    return await _load_detail(session, game.id)


@delete("/games/{game_id:int}", summary="Удалить игру (под токеном)", status_code=HTTP_204_NO_CONTENT)
async def delete_game(session: AsyncSession, game_id: int) -> None:
    game = await session.get(Game, game_id)
    if game is None:
        raise NotFoundException(detail=f"Игра #{game_id} не найдена")
    await session.delete(game)
    await session.commit()


admin_router = Router(
    path="/admin",
    route_handlers=[create_game, update_game, delete_game],
    guards=[require_admin_token],
)
