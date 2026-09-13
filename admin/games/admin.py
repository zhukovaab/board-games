"""Админка коллекции."""
from __future__ import annotations

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.utils.html import format_html

from games.models import Category, Game, GameImage, Mechanic, Theme


class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "games_count")
    search_fields = ("name",)
    ordering = ("name",)
    fields = ("name", "slug", "description")

    def get_queryset(self, request) -> QuerySet:
        return super().get_queryset(request).annotate(_games_count=Count("games"))

    @admin.display(description="игр в коллекции", ordering="_games_count")
    def games_count(self, obj) -> int:
        return obj._games_count


@admin.register(Category)
class CategoryAdmin(TaxonomyAdmin):
    pass


@admin.register(Theme)
class ThemeAdmin(TaxonomyAdmin):
    pass


@admin.register(Mechanic)
class MechanicAdmin(TaxonomyAdmin):
    pass


class GameImageInline(admin.TabularInline):
    model = GameImage
    extra = 1
    fields = ("image", "preview", "caption", "sort_order")
    readonly_fields = ("preview",)

    @admin.display(description="превью")
    def preview(self, obj) -> str:
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" style="height:70px;border-radius:6px;object-fit:cover" />',
            obj.image.url,
        )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "cover_preview",
        "title",
        "players_display",
        "playtime_display",
        "min_age",
        "complexity",
        "is_expansion",
        "location",
    )
    list_display_links = ("cover_preview", "title")
    list_filter = (
        "categories",
        "themes",
        "mechanics",
        "has_solo_mode",
        "is_expansion",
    )
    search_fields = ("title", "title_original", "description", "notes")
    filter_horizontal = ("categories", "themes", "mechanics")
    autocomplete_fields = ("base_game",)
    inlines = (GameImageInline,)
    list_per_page = 30
    save_on_top = True

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "title_original",
                    "slug",
                    "cover",
                    "cover_preview_big",
                    "description",
                )
            },
        ),
        (
            "Параметры партии",
            {
                "fields": (
                    ("min_players", "max_players", "best_players"),
                    ("playtime", "min_age", "complexity"),
                    "has_solo_mode",
                )
            },
        ),
        (
            "Классификация",
            {"fields": ("categories", "themes", "mechanics")},
        ),
        (
            "Дополнение",
            {
                "fields": ("is_expansion", "base_game"),
                "description": "Если указана базовая игра, признак дополнения проставится сам.",
            },
        ),
        (
            "Дома",
            {"fields": ("location", "notes")},
        ),
        (
            "Правила",
            {"fields": ("rules_url", "rules_file")},
        ),
    )
    readonly_fields = ("cover_preview_big",)

    def get_queryset(self, request) -> QuerySet:
        return (
            super()
            .get_queryset(request)
            .prefetch_related("categories", "themes", "mechanics")
        )

    @admin.display(description="")
    def cover_preview(self, obj) -> str:
        if not obj.cover:
            return format_html(
                '<div style="width:40px;height:56px;border-radius:6px;'
                'background:linear-gradient(135deg,#3b3663,#1f1d33);"></div>'
            )
        return format_html(
            '<img src="{}" style="width:40px;height:56px;border-radius:6px;object-fit:cover" />',
            obj.cover.url,
        )

    @admin.display(description="текущая обложка")
    def cover_preview_big(self, obj) -> str:
        if not obj.cover:
            return "Обложка не загружена"
        return format_html(
            '<img src="{}" style="max-height:220px;border-radius:10px" />', obj.cover.url
        )

    @admin.display(description="игроки")
    def players_display(self, obj) -> str:
        if obj.min_players == obj.max_players:
            return f"{obj.min_players}"
        return f"{obj.min_players}–{obj.max_players}"

    @admin.display(description="время", ordering="playtime")
    def playtime_display(self, obj) -> str:
        return f"{obj.playtime} мин" if obj.playtime else "—"
