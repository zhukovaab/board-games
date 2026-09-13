"""Демонстрационные данные: справочники и несколько игр из домашней полки."""
from __future__ import annotations

CATEGORIES = [
    ("Пати-игра", "party", "Шумные игры для компании"),
    ("Стратегия", "strategy", "Игры с глубоким планированием"),
    ("Семейная", "family", "Правила понятны всем, играется вместе с детьми"),
    ("Дуэльная", "duel", "Рассчитана ровно на двоих"),
    ("Детская", "kids", "Для самых маленьких"),
    ("Филлер", "filler", "Короткая игра между делом"),
]

THEMES = [
    ("Фэнтези", "fantasy", ""),
    ("Детектив", "detective", ""),
    ("Космос", "space", ""),
    ("История", "history", ""),
    ("Животные и природа", "nature", ""),
    ("Средневековье", "medieval", ""),
    ("Путешествия", "travel", ""),
    ("Античность", "antiquity", ""),
    ("Вестерн", "western", ""),
    ("Абстрактная", "abstract", ""),
    ("Сказка", "fairytale", ""),
    ("Цивилизация", "civilization", ""),
    ("Наука", "science", ""),
    ("Ренессанс", "renaissance", ""),
    ("Юмор", "humor", ""),
    ("Хоррор", "horror", ""),
]

MECHANICS = [
    ("Выкладывание тайлов", "tile-laying", ""),
    ("Контроль территории", "area-control", ""),
    ("Коллекционирование наборов", "set-collection", ""),
    ("Движок", "engine-building", ""),
    ("Ассоциации", "associations", ""),
    ("Командная игра", "teams", ""),
    ("Экономика и торговля", "trading", ""),
    ("Броски кубиков", "dice", ""),
    ("Кооператив", "cooperative", ""),
    ("Управление рукой", "hand-management", ""),
    ("Голосование", "voting", ""),
    ("Драфт", "drafting", ""),
    ("Блеф", "bluffing", ""),
    ("Дедукция", "deduction", ""),
    ("Скрытые роли", "hidden-roles", ""),
]

GAMES = [
    {
        "title": "Каркассон",
        "title_original": "Carcassonne",
        "slug": "carcassonne",
        "description": (
            "Классика выкладывания тайлов: игроки по очереди достраивают карту "
            "средневековой Франции и расставляют подданных на дорогах, городах и полях. "
            "Правила объясняются за пять минут, но борьба за крупный город идёт до последнего тайла."
        ),
        "min_players": 2,
        "max_players": 5,
        "best_players": "2–3",
        "playtime": 45,
        "min_age": 7,
        "complexity": "1.9",
        "location": "Полка в гостиной, верхний ряд",
        "notes": "Играем сразу с «Рекой» — партия получается ровнее.",
        "categories": ["family"],
        "themes": ["medieval"],
        "mechanics": ["tile-laying", "area-control"],
    },
    {
        "title": "Билет на поезд: Европа",
        "title_original": "Ticket to Ride: Europe",
        "slug": "ticket-to-ride-europe",
        "description": (
            "Собираем цветные вагоны и строим железные дороги между европейскими городами, "
            "стараясь тайком закрыть свои маршруты раньше, чем соперник займёт нужный участок."
        ),
        "min_players": 2,
        "max_players": 5,
        "best_players": "4",
        "playtime": 60,
        "min_age": 8,
        "complexity": "1.9",
        "location": "Полка в гостиной, верхний ряд",
        "notes": "",
        "categories": ["family"],
        "themes": ["travel"],
        "mechanics": ["set-collection", "area-control"],
    },
    {
        "title": "Крылья",
        "title_original": "Wingspan",
        "slug": "wingspan",
        "description": (
            "Орнитологический пасьянс: каждая птица, попадая в вольер, усиливает "
            "одно из трёх действий, и к концу партии поле работает как отлаженный механизм."
        ),
        "min_players": 1,
        "max_players": 5,
        "best_players": "3",
        "playtime": 60,
        "min_age": 10,
        "complexity": "2.4",
        "has_solo_mode": True,
        "location": "Полка в гостиной, верхний ряд",
        "notes": "Соло-режим против автомы — отличный вариант на вечер.",
        "categories": ["strategy"],
        "themes": ["nature"],
        "mechanics": ["engine-building", "set-collection"],
    },
    {
        "title": "Кодовые имена",
        "title_original": "Codenames",
        "slug": "codenames",
        "description": (
            "Два капитана дают ассоциации одним словом, команды угадывают своих агентов "
            "на поле из двадцати пяти карточек. Главное — не наткнуться на убийцу."
        ),
        "min_players": 2,
        "max_players": 8,
        "best_players": "6+",
        "playtime": 15,
        "min_age": 10,
        "complexity": "1.3",
        "location": "Шкаф в спальне, коробка с филлерами",
        "notes": "Безотказный вариант, когда гостей больше шести.",
        "categories": ["party"],
        "themes": ["abstract"],
        "mechanics": ["associations", "teams"],
    },
    {
        "title": "Колонизаторы",
        "title_original": "Catan",
        "slug": "catan",
        "description": (
            "Остров из шестиугольников, кубики решают урожай, а всё остальное решает торговля. "
            "Игра, с которой у многих начинались настолки."
        ),
        "min_players": 3,
        "max_players": 4,
        "best_players": "4",
        "playtime": 90,
        "min_age": 10,
        "complexity": "2.3",
        "location": "Полка в гостиной, нижний ряд",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["civilization"],
        "mechanics": ["trading", "dice"],
    },
    {
        "title": "Пандемия",
        "title_original": "Pandemic",
        "slug": "pandemic",
        "description": (
            "Кооператив, в котором команда специалистов гасит вспышки четырёх вирусов "
            "по всему миру. Проигрываем или выигрываем только вместе."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "4",
        "playtime": 45,
        "min_age": 8,
        "complexity": "2.4",
        "has_solo_mode": True,
        "location": "Полка в гостиной, нижний ряд",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["science"],
        "mechanics": ["cooperative", "hand-management"],
    },
    {
        "title": "Диксит",
        "title_original": "Dixit",
        "slug": "dixit",
        "description": (
            "Сюрреалистичные иллюстрации и одна фраза-ассоциация к своей карте: "
            "нужно, чтобы угадали не все и не никто."
        ),
        "min_players": 3,
        "max_players": 6,
        "best_players": "6",
        "playtime": 30,
        "min_age": 8,
        "complexity": "1.2",
        "location": "Шкаф в спальне",
        "notes": "",
        "categories": ["party"],
        "themes": ["fairytale"],
        "mechanics": ["associations", "voting"],
    },
    {
        "title": "7 чудес: Дуэль",
        "title_original": "7 Wonders Duel",
        "slug": "7-wonders-duel",
        "description": (
            "Драфт карт античных построек на двоих: три эпохи, три способа победить "
            "и постоянный соблазн отобрать у соперника нужную карту."
        ),
        "min_players": 2,
        "max_players": 2,
        "best_players": "2",
        "playtime": 30,
        "min_age": 10,
        "complexity": "2.2",
        "location": "Шкаф в спальне",
        "notes": "Лучшая дуэлька в коллекции.",
        "categories": ["duel"],
        "themes": ["antiquity"],
        "mechanics": ["drafting", "engine-building"],
    },
    {
        "title": "Сплендор",
        "title_original": "Splendor",
        "slug": "splendor",
        "description": (
            "Купцы эпохи Ренессанса копят самоцветы и скупают прииски, "
            "чтобы каждая следующая покупка обходилась дешевле предыдущей."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "3",
        "playtime": 30,
        "min_age": 10,
        "complexity": "1.8",
        "location": "Шкаф в спальне",
        "notes": "",
        "categories": ["family"],
        "themes": ["renaissance"],
        "mechanics": ["engine-building", "set-collection"],
    },
    {
        "title": "Имаджинариум",
        "title_original": "",
        "slug": "imaginarium",
        "description": (
            "Отечественный ответ «Дикситу» с более взрослыми и ироничными иллюстрациями."
        ),
        "min_players": 4,
        "max_players": 7,
        "best_players": "6",
        "playtime": 45,
        "min_age": 12,
        "complexity": "1.2",
        "location": "Шкаф в спальне",
        "notes": "",
        "categories": ["party"],
        "themes": ["fairytale"],
        "mechanics": ["associations", "voting"],
    },
    {
        "title": "Взрывные котята",
        "title_original": "Exploding Kittens",
        "slug": "exploding-kittens",
        "description": (
            "Карточная русская рулетка: тянешь карту и надеешься, что это не котёнок со взрывчаткой."
        ),
        "min_players": 2,
        "max_players": 5,
        "best_players": "4",
        "playtime": 15,
        "min_age": 7,
        "complexity": "1.1",
        "location": "Шкаф в спальне, коробка с филлерами",
        "notes": "",
        "categories": ["filler", "party"],
        "themes": ["humor"],
        "mechanics": ["hand-management", "bluffing"],
    },
    {
        "title": "Манчкин",
        "title_original": "Munchkin",
        "slug": "munchkin",
        "description": (
            "Пародия на подземелья и драконов, где подлость соседа — основная механика."
        ),
        "min_players": 3,
        "max_players": 6,
        "best_players": "4",
        "playtime": 90,
        "min_age": 10,
        "complexity": "1.8",
        "location": "Шкаф в спальне",
        "notes": "Заканчивать партию лучше по будильнику.",
        "categories": ["party"],
        "themes": ["fantasy", "humor"],
        "mechanics": ["bluffing", "hand-management"],
    },
    {
        "title": "Тайное послание",
        "title_original": "Love Letter",
        "slug": "love-letter",
        "description": (
            "Шестнадцать карт, одна в руке — и целая партия дедукции, "
            "которая помещается в карман."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "4",
        "playtime": 20,
        "min_age": 10,
        "complexity": "1.2",
        "location": "Шкаф в спальне, коробка с филлерами",
        "notes": "",
        "categories": ["filler"],
        "themes": ["medieval"],
        "mechanics": ["deduction", "bluffing"],
    },
    {
        "title": "Эволюция",
        "title_original": "",
        "slug": "evolution",
        "description": (
            "Создаём животных и навешиваем на них свойства, пока соседский хищник "
            "не решил, что наша водоплавающая — это обед."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "4",
        "playtime": 45,
        "min_age": 12,
        "complexity": "2.0",
        "location": "Полка в гостиной, нижний ряд",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["nature"],
        "mechanics": ["hand-management", "bluffing"],
    },
    {
        "title": "Бэнг!",
        "title_original": "Bang!",
        "slug": "bang",
        "description": (
            "Вестерн со скрытыми ролями: шериф ищет бандитов, бандиты ищут шерифа, "
            "отступник ждёт своего момента."
        ),
        "min_players": 4,
        "max_players": 7,
        "best_players": "6",
        "playtime": 30,
        "min_age": 8,
        "complexity": "1.8",
        "location": "Шкаф в спальне",
        "notes": "",
        "categories": ["party"],
        "themes": ["western"],
        "mechanics": ["hidden-roles", "deduction", "bluffing"],
    },
]

EXPANSIONS = [
    {
        "title": "Каркассон: Река",
        "title_original": "Carcassonne: The River",
        "slug": "carcassonne-the-river",
        "base_game": "carcassonne",
        "description": "Речные тайлы для старта партии — карта разрастается ровнее и плотнее.",
        "min_players": 2,
        "max_players": 5,
        "playtime": 45,
        "min_age": 7,
        "complexity": "1.9",
        "location": "В коробке с базой",
        "categories": ["family"],
        "themes": ["medieval"],
        "mechanics": ["tile-laying"],
    },
    {
        "title": "Крылья: Европа",
        "title_original": "Wingspan: European Expansion",
        "slug": "wingspan-european-expansion",
        "base_game": "wingspan",
        "description": "Птицы Европы с новыми способностями, работающими в ход соперника.",
        "min_players": 1,
        "max_players": 5,
        "playtime": 60,
        "min_age": 10,
        "complexity": "2.4",
        "has_solo_mode": True,
        "location": "В коробке с базой",
        "categories": ["strategy"],
        "themes": ["nature"],
        "mechanics": ["engine-building"],
    },
]
