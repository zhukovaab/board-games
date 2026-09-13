"""Админка коллекции."""
from __future__ import annotations

from django import forms
from django.contrib import admin
from django.db.models import Count, QuerySet
from django.utils.html import format_html
from martor.widgets import AdminMartorWidget

from games.models import Category, Game, GameImage, GameVideo, Mechanic, Theme, is_remote_url


def _image_src(value) -> str | None:
    """Ссылка для <img>: как есть для внешнего URL, иначе через файловое хранилище."""
    if not value:
        return None
    text = str(value)
    return text if is_remote_url(text) else value.url


class DescriptionMartorWidget(AdminMartorWidget):
    """Панель превью martor не учитывает тёмную тему админки Django 5 —
    без явных цветов текст превью наследует светлый --body-fg и становится
    нечитаемым на белом фоне. Добавляем поверх фикс-стили."""

    class Media:
        css = {"all": ("games/css/martor-admin-fix.css",)}


class MarkdownDescriptionMixin:
    """Показывает поле description как markdown-редактор с панелью инструментов."""

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "description":
            kwargs["widget"] = DescriptionMartorWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class TaxonomyAdmin(MarkdownDescriptionMixin, admin.ModelAdmin):
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


class GameImageInlineForm(forms.ModelForm):
    image_url = forms.URLField(
        required=False,
        label="Ссылка на изображение",
        help_text="Альтернатива загрузке файла: заполни, если картинка уже лежит по URL.",
    )

    class Meta:
        model = GameImage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False
        current = str(self.instance.image) if self.instance and self.instance.pk else ""
        self._image_is_url = is_remote_url(current)
        if self._image_is_url:
            self.initial["image_url"] = current
            self.initial["image"] = None

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("DELETE"):
            return cleaned
        has_file = bool(cleaned.get("image"))
        has_url = bool(cleaned.get("image_url", "").strip())
        has_existing = bool(self.instance.pk and self.instance.image) and not has_file
        if not (has_file or has_url or has_existing) and self.has_changed():
            raise forms.ValidationError("Укажи файл изображения или ссылку на него.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        url = self.cleaned_data.get("image_url", "").strip()
        if url:
            instance.image = url
        elif self._image_is_url and not self.cleaned_data.get("image"):
            instance.image = ""
        if commit:
            instance.save()
        return instance


class GameImageInline(admin.TabularInline):
    model = GameImage
    form = GameImageInlineForm
    extra = 1
    fields = ("image", "image_url", "preview", "caption", "sort_order")
    readonly_fields = ("preview",)

    @admin.display(description="превью")
    def preview(self, obj) -> str:
        src = _image_src(obj.image)
        if not src:
            return "—"
        return format_html(
            '<img src="{}" style="height:70px;border-radius:6px;object-fit:cover" />', src
        )


class GameVideoInline(admin.TabularInline):
    model = GameVideo
    extra = 1
    fields = ("title", "url", "sort_order")


class GameAdminForm(forms.ModelForm):
    cover_url = forms.URLField(
        required=False,
        label="Ссылка на обложку",
        help_text="Альтернатива загрузке файла: заполни, если обложка уже лежит по URL.",
    )

    class Meta:
        model = Game
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current = str(self.instance.cover) if self.instance and self.instance.pk else ""
        self._cover_is_url = is_remote_url(current)
        if self._cover_is_url:
            self.initial["cover_url"] = current
            self.initial["cover"] = None


@admin.register(Game)
class GameAdmin(MarkdownDescriptionMixin, admin.ModelAdmin):
    form = GameAdminForm
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
    inlines = (GameImageInline, GameVideoInline)
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
                    "cover_url",
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

    def save_model(self, request, obj, form, change) -> None:
        cover_url = form.cleaned_data.get("cover_url", "").strip()
        if cover_url:
            obj.cover = cover_url
        elif form._cover_is_url and not form.cleaned_data.get("cover"):
            obj.cover = ""
        super().save_model(request, obj, form, change)

    @admin.display(description="")
    def cover_preview(self, obj) -> str:
        src = _image_src(obj.cover)
        if not src:
            return format_html(
                '<div style="width:40px;height:56px;border-radius:6px;'
                'background:linear-gradient(135deg,#3b3663,#1f1d33);"></div>'
            )
        return format_html(
            '<img src="{}" style="width:40px;height:56px;border-radius:6px;object-fit:cover" />',
            src,
        )

    @admin.display(description="текущая обложка")
    def cover_preview_big(self, obj) -> str:
        src = _image_src(obj.cover)
        if not src:
            return "Обложка не загружена"
        return format_html(
            '<img src="{}" style="max-height:220px;border-radius:10px" />', src
        )

    @admin.display(description="игроки")
    def players_display(self, obj) -> str:
        if obj.min_players == obj.max_players:
            return f"{obj.min_players}"
        return f"{obj.min_players}–{obj.max_players}"

    @admin.display(description="время", ordering="playtime")
    def playtime_display(self, obj) -> str:
        return f"{obj.playtime} мин" if obj.playtime else "—"
