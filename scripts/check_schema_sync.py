"""Сверка схемы: SQLAlchemy (источник истины) против Django-моделей админки.

Запуск из корня репозитория:
    python scripts/check_schema_sync.py

Скрипту нужны зависимости обоих сервисов (backend/requirements.txt и
admin/requirements.txt). Падает с ненулевым кодом, если таблицы или колонки
разошлись — удобно повесить в CI или прогонять после правки моделей.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "admin"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("MEDIA_ROOT", "/tmp/media")

from app.models import Base  # noqa: E402

import django  # noqa: E402

django.setup()

from django.apps import apps  # noqa: E402


def django_tables() -> dict[str, set[str]]:
    tables: dict[str, set[str]] = {}
    for model in apps.get_app_config("games").get_models():
        columns = {
            field.column
            for field in model._meta.local_fields
        }
        tables[model._meta.db_table] = columns
        for m2m in model._meta.local_many_to_many:
            through = m2m.remote_field.through
            tables[through._meta.db_table] = {
                field.column for field in through._meta.local_fields
            }
    return tables


def sqlalchemy_tables() -> dict[str, set[str]]:
    return {
        name: {column.name for column in table.columns}
        for name, table in Base.metadata.tables.items()
    }


def main() -> int:
    orm = sqlalchemy_tables()
    admin = django_tables()

    problems: list[str] = []

    for table in sorted(set(admin) - set(orm)):
        problems.append(f"Таблица «{table}» есть в Django, но её нет в SQLAlchemy")
    for table in sorted(set(orm) - set(admin)):
        problems.append(f"Таблица «{table}» есть в SQLAlchemy, но её нет в Django")

    for table in sorted(set(orm) & set(admin)):
        missing_in_admin = orm[table] - admin[table]
        missing_in_orm = admin[table] - orm[table]
        if missing_in_admin:
            problems.append(
                f"{table}: в Django-модели нет колонок {sorted(missing_in_admin)}"
            )
        if missing_in_orm:
            problems.append(
                f"{table}: в SQLAlchemy-модели нет колонок {sorted(missing_in_orm)}"
            )

    if problems:
        print("Схемы разошлись:")
        for problem in problems:
            print(f"  — {problem}")
        return 1

    print(f"Схемы совпадают: {len(orm)} таблиц.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
