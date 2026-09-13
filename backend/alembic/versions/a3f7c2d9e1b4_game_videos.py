"""game videos (разборы правил на ютубе)

Revision ID: a3f7c2d9e1b4
Revises: c1ea53561599
Create Date: 2026-09-13 12:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = 'a3f7c2d9e1b4'
down_revision = 'c1ea53561599'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "game_videos",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("game_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=200), server_default="", nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_game_videos_game_id", "game_videos", ["game_id"])


def downgrade() -> None:
    op.drop_table("game_videos")
