"""SQLAlchemy-модели. Это источник истины для схемы БД (миграции — Alembic).

Django-приложение в admin/ описывает те же таблицы с managed = False
и используется только как админка. При изменении схемы здесь — правь и там.
"""
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def _m2m(table_name: str, target_table: str, target_column: str) -> Table:
    """Промежуточная таблица в том виде, в каком её ожидает Django ORM:
    суррогатный id + <model>_id колонки."""
    return Table(
        table_name,
        Base.metadata,
        Column("id", BigInteger, primary_key=True, autoincrement=True),
        Column(
            "game_id",
            BigInteger,
            ForeignKey("games.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        Column(
            target_column,
            BigInteger,
            ForeignKey(f"{target_table}.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        UniqueConstraint("game_id", target_column, name=f"uq_{table_name}"),
    )


game_categories = _m2m("game_categories", "categories", "category_id")
game_themes = _m2m("game_themes", "themes", "theme_id")
game_mechanics = _m2m("game_mechanics", "mechanics", "mechanic_id")


class TaxonomyMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="", server_default="")


class Category(TaxonomyMixin, Base):
    """Тип игры: пати, стратегия, семейная, дуэльная..."""

    __tablename__ = "categories"



class Theme(TaxonomyMixin, Base):
    """Тематика: фэнтези, детектив, космос..."""

    __tablename__ = "themes"



class Mechanic(TaxonomyMixin, Base):
    """Механика: кооператив, дедукция, деклбилдинг..."""

    __tablename__ = "mechanics"



class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(200), index=True)
    title_original: Mapped[str] = mapped_column(String(200), default="", server_default="")
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True)
    cover: Mapped[str] = mapped_column(String(255), default="", server_default="")
    description: Mapped[str] = mapped_column(Text, default="", server_default="")

    min_players: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    max_players: Mapped[int] = mapped_column(Integer, default=4, server_default="4")
    best_players: Mapped[str] = mapped_column(String(50), default="", server_default="")
    playtime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    complexity: Mapped[Decimal | None] = mapped_column(Numeric(2, 1), nullable=True)
    has_solo_mode: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    is_expansion: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    base_game_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("games.id", ondelete="SET NULL"), nullable=True, index=True
    )

    location: Mapped[str] = mapped_column(String(200), default="", server_default="")
    notes: Mapped[str] = mapped_column(Text, default="", server_default="")
    rules_url: Mapped[str] = mapped_column(String(500), default="", server_default="")
    rules_file: Mapped[str] = mapped_column(String(255), default="", server_default="")

    categories: Mapped[list[Category]] = relationship(
        secondary=game_categories, lazy="selectin"
    )
    themes: Mapped[list[Theme]] = relationship(
        secondary=game_themes, lazy="selectin"
    )
    mechanics: Mapped[list[Mechanic]] = relationship(
        secondary=game_mechanics, lazy="selectin"
    )

    # Самоссылка грузится явно через selectinload в детальном роуте,
    # чтобы не устраивать рекурсивную подгрузку в списках.
    base_game: Mapped["Game | None"] = relationship(
        remote_side=[id], back_populates="expansions", lazy="raise"
    )
    expansions: Mapped[list["Game"]] = relationship(
        back_populates="base_game", lazy="raise"
    )
    images: Mapped[list["GameImage"]] = relationship(
        back_populates="game",
        lazy="selectin",
        order_by="GameImage.order",
        cascade="all, delete-orphan",
    )


class GameImage(Base):
    __tablename__ = "game_images"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("games.id", ondelete="CASCADE"), index=True
    )
    image: Mapped[str] = mapped_column(String(255))
    caption: Mapped[str] = mapped_column(String(200), default="", server_default="")
    # "order" — зарезервированное слово в SQL, в БД колонка называется sort_order
    order: Mapped[int] = mapped_column(
        "sort_order", Integer, default=0, server_default="0"
    )

    game: Mapped[Game] = relationship(back_populates="images")
