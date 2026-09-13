"""Ждёт, пока Alembic создаст доменные таблицы (их владелец — backend)."""
from __future__ import annotations

import time

from django.core.management.base import BaseCommand
from django.db import connection

REQUIRED_TABLES = {"games", "categories", "themes", "mechanics", "game_images"}


class Command(BaseCommand):
    help = "Дожидается появления таблиц, которые создаёт Alembic в backend"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--timeout", type=int, default=90)

    def handle(self, *args, **options) -> None:
        deadline = time.monotonic() + options["timeout"]
        while time.monotonic() < deadline:
            try:
                existing = set(connection.introspection.table_names())
            except Exception:
                existing = set()
            if REQUIRED_TABLES.issubset(existing):
                self.stdout.write(self.style.SUCCESS("Схема на месте."))
                return
            time.sleep(2)
        self.stdout.write(
            self.style.WARNING(
                "Не дождался таблиц из Alembic. Проверь логи сервиса backend."
            )
        )
