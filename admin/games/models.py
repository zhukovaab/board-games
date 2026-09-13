"""Зеркала таблиц, которыми владеет Litestar-бэкенд (SQLAlchemy + Alembic).

managed = False: Django не создаёт и не меняет эти таблицы, только читает и пишет
данные через админку. При изменении схемы правь backend/app/models.py,
добавляй миграцию Alembic и синхронизируй описание здесь.
"""
from __future__ import annotations

from django.db import models
from slugify import slugify


class SluggedModel(models.Model):
    name = models.CharField("название", max_length=100, unique=True)
    slug = models.SlugField(
        "код для URL",
        max_length=120,
        unique=True,
        blank=True,
        help_text="Оставь пустым — сгенерируется из названия",
    )
    description = models.TextField("описание", blank=True, default="")

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:120]
        super().save(*args, **kwargs)


class Category(SluggedModel):
    """Тип игры: пати, стратегия, семейная, дуэльная."""

    class Meta(SluggedModel.Meta):
        managed = False
        db_table = "categories"
        verbose_name = "категория (тип игры)"
        verbose_name_plural = "категории (типы игр)"


class Theme(SluggedModel):
    """Тематика: фэнтези, детектив, космос."""

    class Meta(SluggedModel.Meta):
        managed = False
        db_table = "themes"
        verbose_name = "тематика"
        verbose_name_plural = "тематики"


class Mechanic(SluggedModel):
    """Механика: кооператив, дедукция, деклбилдинг."""

    class Meta(SluggedModel.Meta):
        managed = False
        db_table = "mechanics"
        verbose_name = "механика"
        verbose_name_plural = "механики"


class Game(models.Model):
    title = models.CharField("название", max_length=200)
    title_original = models.CharField(
        "оригинальное название", max_length=200, blank=True, default=""
    )
    slug = models.SlugField(
        "код для URL",
        max_length=220,
        unique=True,
        blank=True,
        help_text="Оставь пустым — сгенерируется из названия",
    )
    cover = models.ImageField("обложка", upload_to="covers/", blank=True, default="")
    description = models.TextField("описание", blank=True, default="")

    min_players = models.PositiveIntegerField("игроков от", default=1)
    max_players = models.PositiveIntegerField("игроков до", default=4)
    best_players = models.CharField(
        "оптимально игроков",
        max_length=50,
        blank=True,
        default="",
        help_text="Свободный текст, например «3–4»",
    )
    playtime = models.PositiveIntegerField("время партии, мин", null=True, blank=True)
    min_age = models.PositiveIntegerField("возраст от", null=True, blank=True)
    complexity = models.DecimalField(
        "сложность",
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="От 1.0 (совсем просто) до 5.0 (хардкор)",
    )
    has_solo_mode = models.BooleanField("есть соло-режим", default=False)

    is_expansion = models.BooleanField("это дополнение", default=False)
    base_game = models.ForeignKey(
        "self",
        verbose_name="базовая игра",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="expansions",
        db_column="base_game_id",
    )

    categories = models.ManyToManyField(
        Category,
        verbose_name="категории",
        blank=True,
        related_name="games",
        db_table="game_categories",
    )
    themes = models.ManyToManyField(
        Theme,
        verbose_name="тематики",
        blank=True,
        related_name="games",
        db_table="game_themes",
    )
    mechanics = models.ManyToManyField(
        Mechanic,
        verbose_name="механики",
        blank=True,
        related_name="games",
        db_table="game_mechanics",
    )

    location = models.CharField(
        "где лежит", max_length=200, blank=True, default="", help_text="Полка, шкаф, коробка"
    )
    notes = models.TextField("заметки", blank=True, default="")
    rules_url = models.URLField("ссылка на правила", max_length=500, blank=True, default="")
    rules_file = models.FileField("файл правил", upload_to="rules/", blank=True, default="")

    class Meta:
        managed = False
        db_table = "games"
        ordering = ["title"]
        verbose_name = "настольная игра"
        verbose_name_plural = "настольные игры"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_original or self.title)[:200] or "game"
            slug = base
            counter = 2
            while Game.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        if self.base_game_id:
            self.is_expansion = True
        super().save(*args, **kwargs)


class GameImage(models.Model):
    game = models.ForeignKey(
        Game,
        verbose_name="игра",
        on_delete=models.CASCADE,
        related_name="images",
        db_column="game_id",
    )
    image = models.ImageField("изображение", upload_to="gallery/")
    caption = models.CharField("подпись", max_length=200, blank=True, default="")
    sort_order = models.PositiveIntegerField("порядок", default=0)

    class Meta:
        managed = False
        db_table = "game_images"
        ordering = ["sort_order", "id"]
        verbose_name = "фотография"
        verbose_name_plural = "галерея"

    def __str__(self) -> str:
        return self.caption or f"Фото #{self.pk}"
