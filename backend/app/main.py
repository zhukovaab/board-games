"""Точка входа Litestar-приложения."""
from __future__ import annotations

import os

from litestar import Litestar, Router
from litestar.config.cors import CORSConfig
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from litestar.static_files import create_static_files_router

from app.config import settings
from app.db import provide_session
from app.routes.games import get_game, list_games
from app.routes.taxonomy import get_filters

os.makedirs(settings.media_root, exist_ok=True)

api_router = Router(
    path="/api",
    route_handlers=[list_games, get_game, get_filters],
)

media_router = create_static_files_router(
    path=settings.media_url_path,
    directories=[settings.media_root],
    name="media",
)

app = Litestar(
    route_handlers=[api_router, media_router],
    dependencies={"session": Provide(provide_session)},
    cors_config=CORSConfig(allow_origins=settings.cors_origins, allow_credentials=True),
    openapi_config=OpenAPIConfig(
        title="Домашняя библиотека настолок",
        version="1.0.0",
        path="/api/docs",
    ),
)
