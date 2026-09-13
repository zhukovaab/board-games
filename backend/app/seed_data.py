"""Реальная домашняя коллекция настольных игр.

Факты (издатель, год, число игроков, время партии, возраст) проверены по
BoardGameGeek, официальным страницам издателей, Википедии и российским
магазинам (igroved.ru, lavkaigr.ru) — при расхождении между глобальным и
российским изданием приоритет отдан российскому (например, возраст для
Anno 1800). Категории/темы/механики тоже сверены по жанровым тегам
российских магазинов, а не придуманы. Поле complexity (1–5) — субъективная
оценка сложности, не с BGG. Personal-поля (location, notes, best_players,
has_solo_mode) дозаполняются пользователем — придумывать их нельзя.
"""
from __future__ import annotations

CATEGORIES = [
    ("Пати-игра", "party", "Шумные игры для компании"),
    ("Стратегия", "strategy", "Игры с глубоким планированием"),
    ("Семейная", "family", "Правила понятны всем, играется вместе с детьми"),
    ("Дуэльная", "duel", "Рассчитана ровно на двоих"),
    ("Детская", "kids", "Для самых маленьких"),
    ("Филлер", "filler", "Короткая игра между делом"),
    ("Экономическая", "economic", "Торговля, ресурсы, производственные цепочки"),
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
    ("Индустриализация", "industry", ""),
    ("Шпионы", "spies", ""),
    ("Юмор", "humor", ""),
]

MECHANICS = [
    ("Выкладывание тайлов", "tile-laying", ""),
    ("Контроль территории", "area-control", ""),
    ("Строительство маршрутов", "route-building", ""),
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
    ("Дек-билдинг", "deck-building", ""),
]

GAMES = [
    {
        "title": "7 чудес",
        "title_original": "7 Wonders",
        "slug": "7-wonders",
        "description": (
            "Драфт карт: за 3 эпохи каждый строит своё чудо света и развивает город — "
            "военные, науку, торговлю и золото. Автор — Antoine Bauza, издатель Repos "
            "Production, 2010 год."
        ),
        "min_players": 3,
        "max_players": 7,
        "best_players": "",
        "playtime": 30,
        "min_age": 10,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["antiquity"],
        "mechanics": ["drafting", "set-collection", "engine-building"],
    },
    {
        "title": "7 чудес: Дуэль",
        "title_original": "7 Wonders Duel",
        "slug": "7-wonders-duel",
        "description": (
            "Дуэльный спин-офф «7 чудес» на двоих: драфт карт по общей пирамиде, "
            "три пути к победе — военный, научный или по очкам. Bauza & Cathala, "
            "Repos Production, 2015 год."
        ),
        "min_players": 2,
        "max_players": 2,
        "best_players": "",
        "playtime": 30,
        "min_age": 10,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["duel"],
        "themes": ["antiquity"],
        "mechanics": ["drafting", "set-collection", "engine-building"],
    },
    {
        "title": "Эволюция",
        "title_original": "",
        "slug": "evolution",
        "description": (
            "Российская игра о выживании видов: игроки создают животных и наделяют их "
            "свойствами, конкурируя за еду и спасаясь от хищников. Автор — Дмитрий "
            "Кнорре, издатель «Правильные игры»/Cognitive Games, 2010 год."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "",
        "playtime": 45,
        "min_age": 12,
        "complexity": 3,
        "location": "",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["nature"],
        "mechanics": ["hand-management"],
    },
    {
        "title": "Колонизаторы",
        "title_original": "Catan",
        "slug": "catan",
        "description": (
            "Остров из шестиугольников: кубики решают урожай, а торговля с соперниками — "
            "почти всё остальное. Автор — Klaus Teuber, издатель Kosmos, 1995 год."
        ),
        "min_players": 3,
        "max_players": 4,
        "best_players": "",
        "playtime": 90,
        "min_age": 10,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["strategy", "economic"],
        "themes": ["civilization"],
        "mechanics": ["trading", "dice", "route-building"],
    },
    {
        "title": "Гарри Поттер: Битва за Хогвартс",
        "title_original": "Harry Potter: Hogwarts Battle",
        "slug": "harry-potter-hogwarts-battle",
        "description": (
            "Кооперативный дек-билдинг по семи книгам о Гарри Поттере: команда студентов "
            "отбивается от злодеев и усиливает свои колоды от игры к игре. Издатель — "
            "USAopoly, 2016 год."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "",
        "playtime": 45,
        "min_age": 11,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["fantasy"],
        "mechanics": ["deck-building", "cooperative"],
    },
    {
        "title": "Анно 1800",
        "title_original": "Anno 1800",
        "slug": "anno-1800",
        "description": (
            "Настольная адаптация видеоигры Ubisoft: развитие острова в эпоху "
            "индустриализации, торговля и снабжение растущего населения. Автор — "
            "Martin Wallace, издатель Kosmos, 2019 год."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "",
        "playtime": 130,
        "min_age": 14,
        "complexity": 3,
        "location": "",
        "notes": "",
        "categories": ["strategy", "economic"],
        "themes": ["industry"],
        "mechanics": ["drafting", "hand-management", "engine-building", "trading"],
    },
    {
        "title": "Плоский мир: Анк-Морпорк",
        "title_original": "Discworld: Ankh-Morpork",
        "slug": "discworld-ankh-morpork",
        "description": (
            "По мотивам Плоского мира Терри Пратчетта: у каждого игрока свой секретный "
            "персонаж и своё условие победы в городе, где лорд Ветинари пропал без вести. "
            "Автор — Martin Wallace, издатель Treefrog Games, 2011 год."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "",
        "playtime": 60,
        "min_age": 11,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["fantasy", "humor"],
        "mechanics": ["area-control", "hidden-roles", "hand-management"],
    },
    {
        "title": "Кодовые имена",
        "title_original": "Codenames",
        "slug": "codenames",
        "description": (
            "Два капитана дают ассоциации одним словом, команды угадывают своих агентов "
            "на поле из карточек со словами. Автор — Vlaada Chvátil, издатель Czech Games "
            "Edition, 2015 год (русская локализация — GaGa Games)."
        ),
        "min_players": 2,
        "max_players": 8,
        "best_players": "",
        "playtime": 15,
        "min_age": 10,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["party"],
        "themes": ["spies"],
        "mechanics": ["associations", "teams", "deduction"],
    },
    {
        "title": "Кодовые имена: Картинки",
        "title_original": "Codenames: Pictures",
        "slug": "codenames-pictures",
        "description": (
            "Версия «Кодовых имён», где агенты — не слова, а картинки с несколькими "
            "деталями, что даёт более гибкие ассоциации. Издатель — Czech Games "
            "Edition, 2016 год."
        ),
        "min_players": 2,
        "max_players": 8,
        "best_players": "",
        "playtime": 15,
        "min_age": 10,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["party"],
        "themes": ["spies"],
        "mechanics": ["associations", "teams", "deduction"],
    },
    {
        "title": "Детективные истории: Тигр и Дракон",
        "title_original": "",
        "slug": "detective-stories-tiger-and-dragon",
        "description": (
            "Кооперативная детективная игра из серии «Детективные истории»: команда "
            "расследует два переплетённых дела в средневековом Китае, используя "
            "приложение-компаньон. Издатель — Hobby World."
        ),
        "min_players": 1,
        "max_players": 5,
        "best_players": "",
        "playtime": 105,
        "min_age": 12,
        "complexity": 2,
        "location": "",
        "notes": "Для игры нужно интернет-соединение (приложение-компаньон).",
        "categories": ["family"],
        "themes": ["detective", "history"],
        "mechanics": ["cooperative", "deduction"],
    },
    {
        "title": "Каркассон: Big Box",
        "title_original": "Carcassonne: Big Box",
        "slug": "carcassonne-big-box",
        "description": (
            "Классика выкладывания тайлов (Klaus-Jürgen Wrede, Hans im Glück, 2000) "
            "в комплекте с дополнениями «Таверны и соборы», «Купцы и зодчие» и "
            "мини-дополнениями «Аббат», «Река», «Воздушные шары», «Гонцы», «Паромы», "
            "«Золотые прииски», «Маг и ведьма», «Разбойники» и «Круги на полях»."
        ),
        "min_players": 2,
        "max_players": 5,
        "best_players": "",
        "playtime": 45,
        "min_age": 7,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["family"],
        "themes": ["medieval"],
        "mechanics": ["tile-laying", "area-control"],
    },
    {
        "title": "Гномы-вредители",
        "title_original": "Saboteur",
        "slug": "saboteur",
        "description": (
            "Гномы копают тоннели к золоту, но часть игроков тайно саботирует "
            "раскопки. Автор — Frédéric Moyersoen, издатель AMIGO, 2004 год; "
            "в российской рознице издаётся под названием «Гномы-вредители»."
        ),
        "min_players": 3,
        "max_players": 10,
        "best_players": "",
        "playtime": 30,
        "min_age": 8,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["party", "family"],
        "themes": ["fantasy"],
        "mechanics": ["hidden-roles", "route-building", "bluffing", "deduction"],
    },
    {
        "title": "Гномы-вредители: Дуэль",
        "title_original": "Saboteur: The Duel",
        "slug": "saboteur-duel",
        "description": (
            "Самостоятельная версия «Гномов-вредителей» на одного или двух игроков: "
            "соло — собрать как можно больше золота, вдвоём — собрать больше "
            "соперника. Издатель — AMIGO, 2014 год."
        ),
        "min_players": 1,
        "max_players": 2,
        "best_players": "",
        "playtime": 30,
        "min_age": 8,
        "complexity": 1,
        "has_solo_mode": True,
        "location": "",
        "notes": "",
        "categories": ["duel"],
        "themes": ["fantasy"],
        "mechanics": ["route-building", "hand-management"],
    },
    {
        "title": "Дэни",
        "title_original": "",
        "slug": "deni",
        "description": "",
        "location": "",
        "notes": "Уточнить полное название и данные — не опознана.",
        "categories": [],
        "themes": [],
        "mechanics": [],
    },
    {
        "title": "Ещё не отчислен",
        "title_original": "",
        "slug": "esche-ne-otchislen",
        "description": "",
        "location": "",
        "notes": "Данные допишет владелица игры.",
        "categories": [],
        "themes": [],
        "mechanics": [],
    },
]

EXPANSIONS: list[dict] = []
