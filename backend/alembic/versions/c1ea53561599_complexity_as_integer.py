"""complexity as integer

Revision ID: c1ea53561599
Revises: 0001
Create Date: 2026-09-13 01:52:35.882717

Автогенерация заодно подхватила служебные таблицы Django (их не должно быть в
этой миграции — ими управляет сам Django, см. README) и косметическое
несовпадение unique-индексов на slug, не связанное с этой правкой. Оставлен
только реальный сдвиг схемы: сложность игры — целое число, а не 1 знак после
запятой.
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = 'c1ea53561599'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        'games',
        'complexity',
        existing_type=sa.NUMERIC(precision=2, scale=1),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using='round(complexity)::integer',
    )


def downgrade() -> None:
    op.alter_column(
        'games',
        'complexity',
        existing_type=sa.Integer(),
        type_=sa.NUMERIC(precision=2, scale=1),
        existing_nullable=True,
    )
