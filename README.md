# Домашняя библиотека настолок

Монорепозиторий из трёх частей: витрина коллекции, API и админка.

```
board-games/
├── backend/     Litestar + SQLAlchemy + Alembic — API и владелец схемы БД
├── admin/       Django — только админка, модели с managed = False
├── frontend/    Vite + React + TypeScript + Tailwind + Framer Motion
├── scripts/     сверка схемы между SQLAlchemy и Django
└── docker-compose.yml
```

## Запуск

```bash
cp .env.example .env     # уже сделано, при желании поправь пароли и порты
docker compose up --build
```

| Что | Где |
|---|---|
| Сайт | http://localhost:5173 |
| API | http://localhost:8000/api |
| Документация API | http://localhost:8000/api/docs |
| Админка | http://localhost:8001/admin (admin / admin) |
| База | только внутри сети docker (`db:5432`) |

При первом старте `backend` накатывает миграции Alembic и заливает демо-данные
(справочники + 15 игр и 2 дополнения). Сид идемпотентен: повторный запуск ничего
не перезаписывает и не дублирует. Когда заведёшь свои игры, поставь в `.env`
`SEED_ON_START=0`.

## Доступ к базе с хоста

По умолчанию порт базы наружу не публикуется — сервисам она видна внутри сети как `db:5432`,
и никаких конфликтов с локальным Postgres быть не может. Заглянуть в базу можно так:

```bash
docker compose exec db psql -U boardgames -d boardgames
```

Если нужен внешний клиент (DBeaver, TablePlus), подними с оверлеем:

```bash
docker compose -f docker-compose.yml -f docker-compose.db-port.yml up
```

Порт задаётся в `.env` переменной `POSTGRES_HOST_PORT` (по умолчанию 5433).

## Если порт занят

`Bind for 0.0.0.0:XXXX failed: port is already allocated` — на хосте этот порт уже кем-то
занят. Порты сервисов настраиваются в `.env`: `BACKEND_PORT`, `ADMIN_PORT`, `FRONTEND_PORT`,
`POSTGRES_HOST_PORT`. Посмотреть, кто держит порт:

```bash
lsof -nP -iTCP:5433 -sTCP:LISTEN
docker ps -a --filter "publish=5433"
```

## Как устроены данные

Схемой владеет **backend**: модели в `backend/app/models.py`, миграции в
`backend/alembic/versions`. Django-приложение описывает те же таблицы с
`managed = False` и используется исключительно как интерфейс наполнения.

Порядок при изменении схемы:

1. правишь `backend/app/models.py`;
2. `docker compose exec backend alembic revision --autogenerate -m "что изменилось"`;
3. правишь зеркальную модель в `admin/games/models.py`;
4. `python scripts/check_schema_sync.py` — проверяет, что ничего не забыто;
5. `docker compose restart backend admin`.

Служебные таблицы Django (`auth_user`, `django_session`, `django_admin_log`)
живут в той же базе и мигрируются самим Django — Alembic их не трогает.

### Таблицы

| Таблица | Назначение |
|---|---|
| `games` | настолки и дополнения (дополнение = ссылка на базовую игру) |
| `categories` | тип игры: пати, стратегия, семейная, дуэльная |
| `themes` | тематика: фэнтези, детектив, космос |
| `mechanics` | механика: кооператив, дедукция, драфт |
| `game_images` | галерея фотографий |
| `game_categories`, `game_themes`, `game_mechanics` | связи многие-ко-многим |

## API

| Метод | Назначение |
|---|---|
| `GET /api/games` | список с фильтрами, поиском, сортировкой и пагинацией |
| `GET /api/games/{slug}` | детальная карточка с галереей и дополнениями |
| `GET /api/filters` | справочники со счётчиками и границы диапазонов |

Параметры списка: `search`, `players`, `playtime_max`, `age`, `complexity_min`,
`complexity_max`, `categories`, `themes`, `mechanics` (можно повторять),
`solo`, `expansions` (`hide` / `show` / `only`), `sort`, `page`, `page_size`.

Внутри одной группы справочника условия объединяются по «или», между группами —
по «и»: `?categories=party&mechanics=bluffing` вернёт пати-игры с блефом.

## Фронтенд

Состояние фильтров живёт в URL — ссылку на подборку можно отправить как есть.
Локальная разработка без docker:

```bash
cd frontend
npm install
npm run dev
```

Адрес API берётся из `VITE_API_URL` (по умолчанию `http://localhost:8000`).

## Полезные команды

```bash
docker compose exec backend alembic upgrade head        # накатить миграции
docker compose exec backend python -m app.seed          # залить демо-данные
docker compose exec admin python manage.py createsuperuser
docker compose logs -f backend
python scripts/check_schema_sync.py                     # сверка схем
```

## Картинки

Обложки и галерея загружаются через админку и складываются в общий том `media`,
который раздаёт backend по `/media/...`. Файлы правил — туда же, в `rules/`.
