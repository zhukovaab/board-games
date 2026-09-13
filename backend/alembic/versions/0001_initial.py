"""Первая миграция: игры, справочники, галерея.

Revision ID: 0001
Revises:
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def _taxonomy_table(name: str) -> None:
    op.create_table(
        name,
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(f"ix_{name}_slug", name, ["slug"])


def _m2m_table(table: str, target: str, target_column: str) -> None:
    op.create_table(
        table,
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("game_id", sa.BigInteger(), nullable=False),
        sa.Column(target_column, sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint([target_column], [f"{target}.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("game_id", target_column, name=f"uq_{table}"),
    )
    op.create_index(f"ix_{table}_game_id", table, ["game_id"])
    op.create_index(f"ix_{table}_{target_column}", table, [target_column])


def upgrade() -> None:
    for name in ("categories", "themes", "mechanics"):
        _taxonomy_table(name)

    op.create_table(
        "games",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("title_original", sa.String(length=200), server_default="", nullable=False),
        sa.Column("slug", sa.String(length=220), nullable=False),
        sa.Column("cover", sa.String(length=255), server_default="", nullable=False),
        sa.Column("description", sa.Text(), server_default="", nullable=False),
        sa.Column("min_players", sa.Integer(), server_default="1", nullable=False),
        sa.Column("max_players", sa.Integer(), server_default="4", nullable=False),
        sa.Column("best_players", sa.String(length=50), server_default="", nullable=False),
        sa.Column("playtime", sa.Integer(), nullable=True),
        sa.Column("min_age", sa.Integer(), nullable=True),
        sa.Column("complexity", sa.Numeric(precision=2, scale=1), nullable=True),
        sa.Column("has_solo_mode", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("is_expansion", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("base_game_id", sa.BigInteger(), nullable=True),
        sa.Column("location", sa.String(length=200), server_default="", nullable=False),
        sa.Column("notes", sa.Text(), server_default="", nullable=False),
        sa.Column("rules_url", sa.String(length=500), server_default="", nullable=False),
        sa.Column("rules_file", sa.String(length=255), server_default="", nullable=False),
        sa.ForeignKeyConstraint(["base_game_id"], ["games.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_games_title", "games", ["title"])
    op.create_index("ix_games_slug", "games", ["slug"])
    op.create_index("ix_games_base_game_id", "games", ["base_game_id"])

    op.create_table(
        "game_images",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("game_id", sa.BigInteger(), nullable=False),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column("caption", sa.String(length=200), server_default="", nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_game_images_game_id", "game_images", ["game_id"])

    _m2m_table("game_categories", "categories", "category_id")
    _m2m_table("game_themes", "themes", "theme_id")
    _m2m_table("game_mechanics", "mechanics", "mechanic_id")


def downgrade() -> None:
    for table in ("game_mechanics", "game_themes", "game_categories", "game_images", "games"):
        op.drop_table(table)
    for table in ("mechanics", "themes", "categories"):
        op.drop_table(table)
