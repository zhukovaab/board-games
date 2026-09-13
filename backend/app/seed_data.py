"""Реальная домашняя коллекция настольных игр.

Факты (число игроков, время партии, возраст) проверены по BoardGameGeek,
официальным страницам издателей, Википедии и российским магазинам
(igroved.ru, lavkaigr.ru, hobbyworld.ru) — при расхождении между глобальным
и российским изданием или между сайтом и коробкой приоритет отдан тому,
что написано на самой коробке. Категории/темы/механики сверены по жанровым
тегам этих же магазинов, а не придуманы; каждая позиция в справочниках
использована хотя бы одной игрой.

Описания — про геймплей (что в коробке и как играть), без упоминания
автора/издателя/года — это в БД не нужно.

Поле complexity (1–5) — субъективная оценка сложности, не с BGG.
Personal-поля (location, notes, best_players, has_solo_mode) дозаполняются
пользователем — придумывать их нельзя.
"""
from __future__ import annotations

CATEGORIES = [
    ("Пати-игра", "party", "Шумные игры для компании"),
    ("Стратегия", "strategy", "Игры с глубоким планированием"),
    ("Семейная", "family", "Правила понятны всем, играется вместе с детьми"),
    ("Дуэльная", "duel", "Рассчитана ровно на двоих"),
    ("Экономическая", "economic", "Торговля, ресурсы, производственные цепочки"),
    ("Филлер", "filler", "Короткая игра между делом"),
]

THEMES = [
    ("Фэнтези", "fantasy", ""),
    ("Детектив", "detective", ""),
    ("История", "history", ""),
    ("Животные и природа", "nature", ""),
    ("Средневековье", "medieval", ""),
    ("Античность", "antiquity", ""),
    ("Цивилизация", "civilization", ""),
    ("Индустриализация", "industry", ""),
    ("Шпионы", "spies", ""),
    ("Юмор", "humor", ""),
    ("Фантастика", "sci-fi", ""),
    ("Космос", "space", ""),
    ("Сказка", "fairytale", ""),
    ("Абстрактная", "abstract", ""),
    ("Военная", "war", ""),
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
    ("Сторителлинг", "storytelling", ""),
    ("Аукцион", "auction", ""),
    ("Объяснение слов", "word-explaining", ""),
    ("Реальное время", "real-time", ""),
    ("Хронология", "timeline", ""),
    ("Движение по сетке", "grid-movement", ""),
]

GAMES = [
    {
        "title": "7 чудес",
        "title_original": "7 Wonders",
        "slug": "7-wonders",
        "cover": "https://www.igroved.ru/db/games/avatars/11/3211/box.jpg",
        "description": (
            "За три эпохи каждый игрок развивает свою античную цивилизацию: на "
            "каждом ходу из веера карт выбираешь одну, а остальные передаёшь "
            "соседу — так все действуют одновременно, без ожидания своей "
            "очереди. Карты дают ресурсы, здания, войска, деньги или очки "
            "науки; в конце партии победу определяет сумма очков за войска, "
            "чудо света, монеты, гильдии и научные символы."
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
        "cover": "https://www.igroved.ru/db/games/avatars/55/2355/box.jpg",
        "description": (
            "Дуэльная версия «7 чудес»: карты выкладываются общей пирамидой, "
            "и заранее видно, какие из них откроются позже. Как и в оригинале, "
            "строишь здания и чудеса по путям военной силы, науки или очков, "
            "но здесь есть и мгновенная победа — через военное давление на "
            "соперника или сбор полного набора одинаковых научных символов."
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
        "cover": "https://www.igroved.ru/db/games/avatars/21/621/box.jpg",
        "description": (
            "Каждый игрок выращивает популяцию животных на общем столе с "
            "ограниченным количеством еды. В свой ход разыгрываешь карты — "
            "заводишь новых животных или добавляешь им свойства (хищник, "
            "панцирь, плавание, симбиоз и другие), а на фазе питания решается, "
            "кто наестся, а кто вымрет от голода или зубов соседа."
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
        "cover": "https://www.igroved.ru/db/games/avatars/4/4/box.jpg",
        "description": (
            "На острове из шестиугольных участков строишь дороги, посёлки и "
            "города; какие ресурсы ты получишь в свой ход, решает бросок "
            "кубика и то, что стоит рядом с твоими постройками. Ресурсами "
            "торгуешь с другими игроками и портами, а очки победы дают "
            "застройка острова, самая длинная дорога, самое большое войско и "
            "карты развития."
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
        "cover": "https://www.igroved.ru/db/games/avatars/98/3298/box.jpg",
        "description": (
            "Кооперативный дек-билдинг на четверых: в начале у каждого слабая "
            "стартовая колода, а за партию она усиливается заклинаниями, "
            "союзниками и предметами, которые покупаются на общем рынке. Семь "
            "последовательных партий-«книг» повышают сложность и добавляют "
            "новых злодеев, с которыми предстоит справиться командой."
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
        "cover": "https://www.igroved.ru/db/games/avatars/17/3417/box.jpg",
        "description": (
            "Развиваешь остров эпохи промышленной революции: тянешь карты из "
            "общего ряда (можно забрать даже карту из чужого сброса, вынуждая "
            "соперника подстраиваться), строишь здания, повышаешь уровень "
            "населения и обеспечиваешь его растущие потребности. Победу "
            "определяет сочетание застройки, выполненных контрактов и "
            "технологического развития острова."
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
        "cover": "https://www.igroved.ru/games/ankh-morpork/small/igroved_ankh-morpork_09.jpg",
        "description": (
            "Каждый игрок тайно получает персонажа со своим уникальным "
            "условием победы — и до самого конца никто не знает, кто и как "
            "может выиграть. На карте города игроки двигают агентов, строят и "
            "разрушают здания, устраивают беспорядки и разыгрывают карты "
            "событий, приближаясь к своей скрытой цели."
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
        "cover": "https://www.igroved.ru/db/games/avatars/8/2308/box.jpg",
        "description": (
            "Игроки делятся на две команды, у каждой — капитан, который "
            "знает, какие из 25 карт на столе принадлежат его агентам, какие "
            "— агентам соперника, а какая одна — смертельному убийце. Капитан "
            "даёт одно слово-подсказку и число, а команда должна угадать "
            "нужные карты, не наткнувшись на карту соперника или на убийцу."
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
        "cover": "https://www.igroved.ru/db/games/avatars/68/2468/box.jpg",
        "description": (
            "Та же игра, что и «Кодовые имена», но вместо слов на карточках "
            "— картинки с несколькими деталями и смыслами сразу. Это делает "
            "подсказки капитанов более гибкими и открывает игру тем, кто пока "
            "не бегло читает."
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
        "cover": "https://media.lavkaigr.ru/cache/78/7a/787a398ca8eff4baf774a8d41d8d414b.png",
        "description": (
            "Кооперативное расследование двух переплетённых дел в "
            "средневековом Китае: команда вместе изучает улики, опрашивает "
            "персонажей через карты и приложение-компаньон, действуя "
            "ограниченным числом ходов. В конце каждый отвечает на вопросы о "
            "произошедшем и получает очки за точность своей версии."
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
        "cover": "https://www.igroved.ru/db/games/avatars/9/3309/box.jpg",
        "description": (
            "По очереди достраиваешь карту средневековой Франции, выкладывая "
            "тайлы с дорогами, городами, монастырями и полями, и ставишь на "
            "них своих подданных, чтобы застолбить территорию. В комплекте — "
            "дополнения «Таверны и соборы», «Купцы и зодчие» и девять "
            "мини-модулей (Аббат, Река, Воздушные шары, Гонцы, Паромы, "
            "Золотые прииски, Маг и ведьма, Разбойники, Круги на полях), "
            "которые можно свободно комбинировать с базовыми правилами."
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
        "cover": "https://www.igroved.ru/db/games/avatars/53/1053/box.jpg",
        "description": (
            "Часть игроков тайно назначена вредителями и должна незаметно "
            "мешать остальным. Игроки по очереди выкладывают карты-тоннели, "
            "прокладывая путь от старта к одной из скрытых карт с золотом (или "
            "с пустой породой), а карты действий позволяют ломать инструменты "
            "соперников, чинить свои или обрушивать уже построенные тоннели."
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
        "cover": "https://www.igroved.ru/db/games/avatars/37/2637/box.jpg",
        "description": (
            "Самостоятельная версия «Гномов-вредителей» для одного или двух "
            "игроков без скрытых ролей: соло — как можно быстрее и "
            "эффективнее прокопать путь к золоту, вдвоём — прокопать больше "
            "золотых жил, чем соперник, попутно мешая ему обвалами и "
            "ловушками."
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
        "title": "Судный день",
        "title_original": "Human Punishment: Social Deduction 2.0",
        "slug": "sudnyj-den",
        "cover": "https://22games.net/wp-content/uploads/2022/04/Human-Punishment-Social-Deduction-1.jpg",
        "description": (
            "Большая социально-дедуктивная игра для компании: каждый тайно "
            "получает роль человека, машины или изгоя со своими целями. За "
            "несколько раундов обсуждений и голосований игроки казнят "
            "подозреваемых, пытаясь понять, кто на чьей стороне, прежде чем "
            "время выйдет."
        ),
        "min_players": 4,
        "max_players": 16,
        "best_players": "",
        "playtime": 30,
        "min_age": 14,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["party"],
        "themes": ["sci-fi"],
        "mechanics": ["hidden-roles", "voting", "bluffing"],
    },
    {
        "title": "Мачи Коро",
        "title_original": "Machi Koro",
        "slug": "machi-koro",
        "cover": "https://www.igroved.ru/db/games/avatars/19/1819/box.jpg",
        "description": (
            "Строишь свой город, бросая кубики: выпавшее число решает, какие "
            "из твоих и чужих предприятий приносят доход в этот ход. На "
            "заработанные монеты покупаешь новые предприятия и "
            "достопримечательности — тот, кто первым построит все четыре "
            "знаковые постройки, побеждает."
        ),
        "min_players": 2,
        "max_players": 5,
        "best_players": "",
        "playtime": 30,
        "min_age": 7,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["strategy", "economic"],
        "themes": [],
        "mechanics": ["dice", "engine-building", "set-collection"],
    },
    {
        "title": "Да, Тёмный Властелин!",
        "title_original": "Aye, Dark Overlord!",
        "slug": "da-tyomnyy-vlastelin",
        "cover": "https://www.igroved.ru/db/games/avatars/81/181/box.jpg",
        "description": (
            "Каждый игрок — незадачливый слуга Тёмного Властелина, который "
            "должен на ходу придумать оправдание провалу задания, используя "
            "случайно выпавшие слова-подсказки. Остальные голосуют, чья байка "
            "правдоподобнее, — и чем нелепее история, тем чаще она побеждает."
        ),
        "min_players": 4,
        "max_players": 9,
        "best_players": "",
        "playtime": 30,
        "min_age": 12,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["party"],
        "themes": ["fantasy", "humor"],
        "mechanics": ["storytelling", "bluffing"],
    },
    {
        "title": "Нефариус",
        "title_original": "Nefarious",
        "slug": "nefarious",
        "cover": "https://gaga.ru/gaga/files/images/fullsize/2387/1.jpg",
        "description": (
            "Каждый раунд на столе появляются новые изобретения, а игроки "
            "участвуют в закрытом аукционе за право заполучить их первыми. "
            "Собранные изобретения и патенты приносят деньги и очки "
            "признания, а случайные карты «мировых законов» каждую партию "
            "меняют правила игры."
        ),
        "min_players": 2,
        "max_players": 6,
        "best_players": "",
        "playtime": 30,
        "min_age": 12,
        "complexity": 3,
        "location": "",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["sci-fi"],
        "mechanics": ["auction", "hand-management", "set-collection"],
    },
    {
        "title": "Диксит Одиссея",
        "title_original": "Dixit Odyssey",
        "slug": "dixit-odyssey",
        "cover": "https://www.boardgamebliss.com/cdn/shop/products/pic918568_lg.jpg?v=1578608899&width=1726",
        "description": (
            "Рассказчик выбирает карту с сюрреалистичной иллюстрацией и "
            "придумывает к ней фразу или ассоциацию — не слишком очевидную и "
            "не слишком туманную. Остальные подкладывают свои карты, которые "
            "тоже подходят под подсказку, а затем все голосуют, пытаясь "
            "угадать карту рассказчика, не выдав при этом своей."
        ),
        "min_players": 3,
        "max_players": 12,
        "best_players": "",
        "playtime": 30,
        "min_age": 8,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["party", "family"],
        "themes": ["fairytale"],
        "mechanics": ["storytelling", "voting", "associations"],
    },
    {
        "title": "Star Wars: Карточная игра",
        "title_original": "Star Wars: The Card Game",
        "slug": "star-wars-card-game",
        "cover": "https://media.lavkaigr.ru/catalog/2017/04/star-wars-kartochnaia-igra.jpg",
        "description": (
            "Дуэльная карточная игра по вселенной Star Wars: каждый строит "
            "колоду персонажей, кораблей и событий одной из сторон Силы и "
            "борется за контроль над локациями, нанося урон базе соперника. "
            "Победа достигается разгромом вражеской базы или выполнением "
            "условий на картах-целях."
        ),
        "min_players": 2,
        "max_players": 2,
        "best_players": "",
        "playtime": 45,
        "min_age": 10,
        "complexity": 3,
        "location": "",
        "notes": "",
        "categories": ["duel"],
        "themes": ["space"],
        "mechanics": ["hand-management", "area-control"],
    },
    {
        "title": "Кодекс Природы",
        "title_original": "Codex Naturalis",
        "slug": "codex-naturalis",
        "cover": "https://www.igroved.ru/db/games/avatars/17/3517/box.jpg",
        "description": (
            "Выкладываешь карты друг на друга, как страницы манускрипта, "
            "совмещая изображённые ресурсы (грибы, растения, животных, "
            "насекомых) так, чтобы новые карты давали как можно больше очков. "
            "Часть карт при выкладке закрывают друг друга лишь частично, "
            "поэтому нужно заранее просчитывать, какие углы останутся "
            "доступными для следующих ходов."
        ),
        "min_players": 1,
        "max_players": 4,
        "best_players": "",
        "playtime": 25,
        "min_age": 7,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["family", "strategy"],
        "themes": ["nature"],
        "mechanics": ["tile-laying", "set-collection"],
    },
    {
        "title": "Экивоки: Мама запретила",
        "title_original": "",
        "slug": "ekivoki-mama-zapretila",
        "cover": "https://catalog-cdn.detmir.st/media/-OlVysRwMRJQjKtbdlNTDkYsuoSuAREIjHw_wXXVsLM=.webp?preset=site_product_gallery_r450",
        "description": (
            "Командная игра на объяснение слов для взрослых компаний: "
            "доставшееся тебе слово нужно передать своей команде одним из "
            "выпавших способов — синонимами, антонимами, жестами, рисунком, "
            "звуками или пластилином. Карточки в этом выпуске — на темы "
            "вечеринок, странностей и всего того, что «мама запретила бы» "
            "объяснять при детях."
        ),
        "min_players": 2,
        "max_players": 16,
        "best_players": "",
        "playtime": 50,
        "min_age": 16,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["party"],
        "themes": ["humor"],
        "mechanics": ["word-explaining", "teams"],
    },
    {
        "title": "Робин Гуд",
        "title_original": "",
        "slug": "robin-gud-zvezda",
        "cover": "https://zvezda.org.ru/upload/iblock/c56/8952.jpg",
        "description": (
            "Игроки — разбойники из отряда Робин Гуда: грабят на дорогах "
            "купцов, разносят вести, помогают в лагере и собирают сведения о "
            "соседях. Каждое выполненное задание даёт карту одного из типов, "
            "и первый, кто наберёт семь карт одного типа, становится правой "
            "рукой Робин Гуда."
        ),
        "min_players": 2,
        "max_players": 6,
        "best_players": "",
        "playtime": 30,
        "min_age": 8,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["family"],
        "themes": ["medieval"],
        "mechanics": ["set-collection", "hand-management"],
    },
    {
        "title": "Cluedo",
        "title_original": "Cluedo",
        "slug": "cluedo",
        "cover": "https://www.igroved.ru/db/games/avatars/16/16/box.jpg",
        "description": (
            "Классический детектив: игроки перемещаются по особняку, "
            "посещают комнаты и делают предположения о том, кто убийца, каким "
            "оружием и в какой комнате было совершено преступление. Через "
            "процесс исключения — по своим и чужим подсказкам — нужно первым "
            "назвать точную комбинацию."
        ),
        "min_players": 2,
        "max_players": 6,
        "best_players": "",
        "playtime": 90,
        "min_age": 8,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["family", "strategy"],
        "themes": ["detective"],
        "mechanics": ["deduction", "dice"],
    },
    {
        "title": "Кубики историй",
        "title_original": "Rory's Story Cubes",
        "slug": "rorys-story-cubes",
        "cover": "https://catalog-cdn.detmir.st/media/T2ncZeBIA7DQ5Y8i5_gLtrc_obIjFTf-R2P8fGCBx9w=.webp?preset=site_product_gallery_r450",
        "description": (
            "Девять кубиков с картинками вместо цифр: бросаешь все разом и "
            "придумываешь историю, которая связывает выпавшие изображения "
            "одно за другим. Играть можно одному для разминки воображения или "
            "по кругу компанией, продолжая рассказ друг друга."
        ),
        "min_players": 1,
        "max_players": 12,
        "best_players": "",
        "playtime": 10,
        "min_age": 6,
        "complexity": 1,
        "has_solo_mode": True,
        "location": "",
        "notes": "",
        "categories": ["filler"],
        "themes": [],
        "mechanics": ["storytelling"],
    },
    {
        "title": "Исторический детектив: Смерть на балу",
        "title_original": "",
        "slug": "istoricheskiy-detektiv-smert-na-balu",
        "cover": "https://veselosidim.ru/images/detailed/26/%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D0%B4%D0%B5%D1%82%D0%B5%D0%BA%D1%82%D0%B8%D0%B2_%D0%A1%D0%BC%D0%B5%D1%80%D1%82%D1%8C_%D0%BD%D0%B0_%D0%B1%D0%B0%D0%BB%D1%83.jpg",
        "description": (
            "На балу при загадочных обстоятельствах умирает знатный человек, "
            "и каждый игрок ведёт собственное расследование: изучает улики, "
            "опрашивает персонажей и делает пометки, действуя ограниченным "
            "числом ходов. В конце нужно ответить на вопросы о произошедшем — "
            "чем точнее версия, тем больше очков."
        ),
        "min_players": 2,
        "max_players": 6,
        "best_players": "",
        "playtime": 45,
        "min_age": 8,
        "complexity": 2,
        "location": "",
        "notes": "Для проверки версии в конце нужен телефон с камерой (QR-коды).",
        "categories": ["family"],
        "themes": ["detective", "history"],
        "mechanics": ["cooperative", "deduction"],
    },
    {
        "title": "LEGO: Звёздные войны. Битва за Хот",
        "title_original": "LEGO Star Wars: The Battle of Hoth",
        "slug": "lego-3866-battle-of-hoth",
        "description": (
            "Настольная игра на основе конструктора: одна сторона играет за "
            "Империю с AT-AT и штурмовиками, другая — за Альянс, обороняющий "
            "базу на заснеженном Хоте. Бросок кубика решает, какие фигурки "
            "двигаются и атакуют, а собранное из деталей LEGO поле боя "
            "определяет, кто до кого дотянется."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "",
        "playtime": 20,
        "min_age": 8,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["family", "duel"],
        "themes": ["space"],
        "mechanics": ["dice", "area-control"],
    },
    {
        "title": "UNO",
        "title_original": "",
        "slug": "uno",
        "cover": "https://www.igroved.ru/db/games/avatars/1/1/box.jpg",
        "description": (
            "Игроки по очереди избавляются от карт на руке, подкладывая карту "
            "того же цвета, номера или символа, что и верхняя карта стопки "
            "сброса. Карты действия меняют направление хода, заставляют "
            "соседа брать карты или пропускать ход, а когда остаётся одна "
            "карта, нужно успеть выкрикнуть «Уно!» — иначе штраф."
        ),
        "min_players": 2,
        "max_players": 10,
        "best_players": "",
        "playtime": 30,
        "min_age": 7,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["family"],
        "themes": [],
        "mechanics": ["hand-management"],
    },
    {
        "title": "UNO No Mercy",
        "title_original": "UNO Show 'em No Mercy",
        "slug": "uno-no-mercy",
        "cover": "https://cdn11.bigcommerce.com/s-9im8f1/products/14446/images/22203/UNO-Show-em-No-Mercy-Card-Game-for-Kids-Adults-Family-Night-Parties-and-Travel_4b6b2f16-5de9-45bf-8806-b4987073d637.75a39bf7478f025258ca16b41f460d2c__13571.1695135688.500.750.jpg?c=2",
        "description": (
            "Более злая версия UNO: карты «возьми +2/+4/+6/+10» можно "
            "перекидывать друг на друга по цепочке, пока кто-то не заберёт "
            "всё сразу, а карты «7» и «0» заставляют меняться картами на "
            "руках с другим игроком. Победить можно и избавившись от всех "
            "карт, и выбив из игры всех соперников."
        ),
        "min_players": 2,
        "max_players": 10,
        "best_players": "",
        "playtime": 20,
        "min_age": 12,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["party"],
        "themes": [],
        "mechanics": ["hand-management"],
    },
    {
        "title": "Лабиринт",
        "title_original": "Labyrinth",
        "slug": "labyrinth",
        "cover": "https://www.igroved.ru/db/games/avatars/48/48/box.jpg",
        "description": (
            "Лабиринт на игровом поле постоянно меняется: перед своим ходом "
            "игрок задвигает свободный тайл коридора с одного края поля, "
            "сдвигая всю линию тайлов и открывая новые проходы. Затем нужно "
            "провести свою фишку как можно дальше по получившимся коридорам "
            "к очередному сокровищу — собравший больше всех побеждает."
        ),
        "min_players": 2,
        "max_players": 4,
        "best_players": "",
        "playtime": 30,
        "min_age": 7,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["family"],
        "themes": [],
        "mechanics": ["tile-laying", "set-collection"],
    },
    {
        "title": "Воины Одина",
        "title_original": "",
        "slug": "voiny-odina",
        "cover": "https://www.igroved.ru/db/games/avatars/85/4485/box.jpg",
        "description": (
            "Игроки по очереди выкладывают карты на стол: каждая следующая "
            "выкладка должна быть больше предыдущей по номиналу и состоять из "
            "равного или большего числа карт одного ранга или цвета. Кто "
            "выложил карты, забирает одну из уже лежащих на столе себе в руку "
            "и сбрасывает остальные; игрок, первым избавившийся от всех карт, "
            "заканчивает раунд, а оставшиеся на руках карты у других — штраф."
        ),
        "min_players": 2,
        "max_players": 6,
        "best_players": "",
        "playtime": 15,
        "min_age": 7,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["filler"],
        "themes": [],
        "mechanics": ["hand-management"],
    },
    {
        "title": "Пара",
        "title_original": "The Pair",
        "slug": "para",
        "description": (
            "Двое одновременно выкладывают карты со значками и буквами. Как "
            "только у обоих на столе оказываются карты с одинаковым значком, "
            "начинается дуэль: нужно первым составить слово из открытых на "
            "столе букв и выкрикнуть его — победитель забирает верхнюю карту "
            "соперника. Побеждает тот, кто соберёт больше карт к концу игры."
        ),
        "min_players": 2,
        "max_players": 2,
        "best_players": "",
        "playtime": 15,
        "min_age": 8,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["duel"],
        "themes": [],
        "mechanics": ["real-time"],
    },
    {
        "title": "Боманка",
        "title_original": "",
        "slug": "bomanka",
        "description": (
            "Карточная игра про студенческую жизнь с юмором и мемами: "
            "партии короткие и быстро объясняются, в комплекте карты с "
            "заданиями и карты персонажей-студентов."
        ),
        "min_players": 2,
        "max_players": 5,
        "best_players": "4",
        "playtime": 20,
        "min_age": 16,
        "complexity": 1,
        "location": "",
        "notes": "Точные правила и механику стоит перепроверить по коробке.",
        "categories": ["party"],
        "themes": ["humor"],
        "mechanics": [],
    },
    {
        "title": "А ты шаришь: Древний мир",
        "title_original": "",
        "slug": "a-ty-sharish-drevniy-mir",
        "description": (
            "Каждый собирает перед собой линию из пяти карт-«изобретений», "
            "располагая их в хронологическом порядке — от самых древних до "
            "более поздних, ориентируясь только на знания и подсказки, "
            "потому что даты на обороте карт открывать нельзя раньше "
            "времени. Особые карты позволяют улучшить свою линию или "
            "сломать чужую."
        ),
        "min_players": 2,
        "max_players": 5,
        "best_players": "",
        "playtime": 15,
        "min_age": None,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["family"],
        "themes": ["antiquity"],
        "mechanics": ["timeline"],
    },
    {
        "title": "Берсерк: Русы против Ящеров",
        "title_original": "",
        "slug": "berserk-rusy-protiv-yashcherov",
        "cover": "https://hobbyworld.cdnvideo.ru/image/cache/hobbyworld/data/-new/hobby-world/berserk/rusi-protiv-jashherov/berserk-rusi-protiv-yascherov-00-320x320.jpg",
        "description": (
            "Самостоятельный дуэльный набор карточной battle-игры: у каждого "
            "игрока своя колода бойцов, которых нужно выводить на поле и "
            "атаковать бойцов соперника, снижая им очки здоровья до нуля. "
            "Бросок кубика и карты эффектов добавляют непредсказуемости в "
            "исход каждого столкновения."
        ),
        "min_players": 2,
        "max_players": 2,
        "best_players": "",
        "playtime": 50,
        "min_age": 18,
        "complexity": 3,
        "location": "",
        "notes": "",
        "categories": ["duel"],
        "themes": ["fantasy"],
        "mechanics": ["hand-management", "dice"],
    },
    {
        "title": "Шахматы",
        "title_original": "Chess",
        "slug": "chess",
        "cover": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Chess_board_and_pieces.jpg",
        "description": (
            "Классическая абстрактная стратегия на клетчатой доске 8×8: у "
            "каждого по 16 фигур шести видов, каждая ходит по-своему, и цель "
            "— поставить мат королю соперника, лишив его любого безопасного "
            "хода. Никакой случайности — только просчёт вариантов на "
            "несколько ходов вперёд."
        ),
        "min_players": 2,
        "max_players": 2,
        "best_players": "",
        "playtime": None,
        "min_age": None,
        "complexity": 4,
        "location": "",
        "notes": "",
        "categories": ["strategy", "duel"],
        "themes": ["abstract"],
        "mechanics": ["grid-movement"],
    },
    {
        "title": "Манчкин",
        "title_original": "Munchkin",
        "slug": "munchkin",
        "cover": "https://www.igroved.ru/db/games/avatars/20/20/box.jpg",
        "description": (
            "Пародия на подземелья и драконов: спускаешься в подземелье, "
            "пинаешь дверь и сражаешься с монстром — в одиночку или прося "
            "помощи у соседа за долю добычи, а можно и подставить союзника, "
            "подсунув ему монстра посильнее. За победу над монстрами и "
            "находки растёт уровень персонажа — первый, кто доберётся до "
            "нужного уровня, побеждает."
        ),
        "min_players": 3,
        "max_players": 6,
        "best_players": "",
        "playtime": 60,
        "min_age": 12,
        "complexity": 2,
        "location": "",
        "notes": "",
        "categories": ["party"],
        "themes": ["fantasy", "humor"],
        "mechanics": ["hand-management", "bluffing"],
    },
    {
        "title": "Риск: Игра в завоевание мира",
        "title_original": "Risk",
        "slug": "risk",
        "cover": "https://tesera.ru/images/items/3202,3/200x200xpa/photo1.jpg",
        "description": (
            "Каждый игрок командует армиями на карте мира, разделённой на "
            "территории и континенты. В свой ход перебрасываешь войска, "
            "атакуешь соседние территории (исход боя решают кубики) и "
            "получаешь подкрепления за захваченные земли и континенты; цель "
            "— вытеснить всех соперников с карты или выполнить тайную "
            "карту-задание."
        ),
        "min_players": 2,
        "max_players": 6,
        "best_players": "",
        "playtime": 60,
        "min_age": 10,
        "complexity": 3,
        "location": "",
        "notes": "",
        "categories": ["strategy"],
        "themes": ["war"],
        "mechanics": ["dice", "area-control"],
    },
    {
        "title": "Сундук приключений",
        "title_original": "Dungeon Roll",
        "slug": "dungeon-roll",
        "cover": "https://www.igroved.ru/db/games/avatars/3/2503/box.jpg",
        "description": (
            "Собираешь отряд, бросая белые кубики-искателей, а затем кубиками "
            "тёмного цвета определяешь, какие монстры ждут в подземелье. "
            "Каждый боец хорошо справляется со своим типом врагов, поэтому "
            "нужно решать, кого на кого бросить, а когда выпадет три дракона "
            "— готовиться к финальной битве. За три спуска в подземелье "
            "побеждает тот, кто набрал больше опыта."
        ),
        "min_players": 1,
        "max_players": 4,
        "best_players": "",
        "playtime": 20,
        "min_age": 8,
        "complexity": 1,
        "has_solo_mode": True,
        "location": "",
        "notes": "",
        "categories": ["filler"],
        "themes": ["fantasy"],
        "mechanics": ["dice", "set-collection"],
    },
    {
        "title": "Игральные карты, 54 листа",
        "title_original": "",
        "slug": "playing-cards-54",
        "cover": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Set_of_playing_cards_52.JPG",
        "description": (
            "Стандартная колода из 52 карт четырёх мастей плюс 2 джокера — "
            "универсальный набор для десятков карточных игр (дурак, "
            "покер, преферанс, пасьянсы и другие), а не отдельная игра со "
            "своими правилами."
        ),
        "location": "",
        "notes": "",
        "categories": [],
        "themes": [],
        "mechanics": [],
    },
    {
        "title": "Доббль",
        "title_original": "Dobble",
        "slug": "dobble",
        "cover": "https://www.igroved.ru/db/games/avatars/72/3072/box.jpg",
        "description": (
            "На каждой из 55 круглых карточек — восемь картинок, и у любых "
            "двух карточек всегда совпадает ровно одна. Правила предлагают "
            "несколько мини-игр: где-то нужно первым найти совпадение и "
            "избавиться от своей карточки, где-то — наоборот, собрать их "
            "как можно больше. Побеждает тот, кто быстрее замечает "
            "совпадающий рисунок."
        ),
        "min_players": 2,
        "max_players": 8,
        "best_players": "",
        "playtime": 20,
        "min_age": 6,
        "complexity": 1,
        "location": "",
        "notes": "",
        "categories": ["filler"],
        "themes": [],
        "mechanics": ["real-time"],
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

EXPANSIONS = [
    {
        "title": "Судный день: Проект «Чистилище»",
        "title_original": "Human Punishment: Project Hell Gate",
        "slug": "sudnyj-den-proekt-chistilische",
        "cover": "https://gaga.ru/gaga/files/images/fullsize/6055/1.jpg",
        "base_game": "sudnyj-den",
        "description": (
            "Дополнение к «Судному дню»: добавляет новые роли, врата ада и "
            "особые карты-автоматы, которые меняют состав ролей и вносят "
            "непредсказуемость в стандартные партии."
        ),
        "min_players": 4,
        "max_players": 16,
        "playtime": 30,
        "min_age": 14,
        "complexity": 2,
        "location": "",
        "categories": ["party"],
        "themes": ["sci-fi"],
        "mechanics": ["hidden-roles", "voting", "bluffing"],
    },
]
