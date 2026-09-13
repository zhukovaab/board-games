# Деплой на сервер

Прод-раскладка: один Ubuntu 24.04 сервер (RUVDS), `docker-compose.prod.yml`,
единственный публичный порт — 80 (контейнер `frontend`, он же nginx и
reverse-proxy на backend/admin).

Образы **собираются в GitHub Actions**, а не на сервере: сервер маленький
(на практике — 436 МБ RAM), сборки `npm ci`/`vite build`/`pip install`
там либо падают по нехватке памяти, либо еле ползут. Поэтому CI
(`.github/workflows/ci-cd.yml`) при пуше в `main` собирает три образа
(backend, admin, frontend) и пушит их в GitHub Container Registry (GHCR),
а сервер только делает `docker compose pull` + `up -d` — без единой
компиляции на самом VPS.

## 1. Один раз настроить сервер

Подключись по SSH под пользователем с sudo.

```bash
sudo apt update && sudo apt upgrade -y

# Docker Engine + compose plugin
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker   # или перелогинься, чтобы группа применилась

# порт 80 наружу
sudo apt install ufw -y   # на некоторых образах не предустановлен
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw enable
sudo ufw status
```

У RUVDS (и у большинства облачных провайдеров) есть ещё файрвол на уровне
хостинга, отдельно от `ufw` внутри сервера — проверь в личном кабинете
раздел «Файрвол»: по умолчанию там пусто (значит всё разрешено), но если
там уже есть правила — добавь туда порт 80 тоже, иначе `ufw` снаружи не
поможет.

Полный репозиторий на сервере не нужен — образы собираются в CI, сервер
только их запускает. Нужны ровно два файла: `docker-compose.prod.yml` и
`.env.prod`. Заведи для них папку и подложи первый файл (дальше CI будет
сам обновлять его при каждом деплое):

```bash
sudo mkdir -p /opt/board-games
sudo chown $USER:$USER /opt/board-games
cd /opt/board-games
curl -O https://raw.githubusercontent.com/zhukovaab/board-games/main/docker-compose.prod.yml
curl -O https://raw.githubusercontent.com/zhukovaab/board-games/main/.env.prod.example
```

## 2. Завести `.env.prod`

```bash
cp .env.prod.example .env.prod
nano .env.prod
```

Обязательно поменять:

- `POSTGRES_PASSWORD` — `openssl rand -base64 24`
- `DJANGO_SECRET_KEY` — `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`
- `DJANGO_ALLOWED_HOSTS` — публичный IP сервера
- `DJANGO_CSRF_TRUSTED_ORIGINS` — `http://<тот же IP>`
- `DJANGO_SUPERUSER_PASSWORD`
- `ADMIN_API_TOKEN` — `openssl rand -hex 32`. Даёт доступ к записи через
  `POST/PATCH/DELETE /api/admin/games` (см. `backend/app/routes/admin_games.py`).
  Пусто — ручки записи выключены. Храни как обычный секрет: не коммить,
  не логируй, передавай себе не по открытым каналам.

Файл `.env.prod` в git не попадает (в `.gitignore`) — трогать его руками
на сервере и всё.

## 3. Получить образы в GHCR (один раз, до первого деплоя)

Пока в `main` не было ни одного пуша после появления
`.github/workflows/ci-cd.yml` — образов в GHCR ещё нет, `docker compose
pull` на сервере пока пулить нечего. Смёрджи/запушь текущие изменения в
`main` (или просто дождись, если уже запушено) и проверь в GitHub →
вкладка **Actions**, что прогон `build-and-push` позеленел.

После первого успешного пуша образы появятся на странице **Packages**
профиля/организации репозитория, но по умолчанию GHCR делает их
**приватными** — даже если сам репозиторий публичный. Сделай их публичными
один раз (иначе на сервере `docker pull` без логина не сработает):

1. github.com → твой профиль → **Packages**.
2. Открой каждый из трёх пакетов: `board-games-backend`, `board-games-admin`,
   `board-games-frontend`.
3. **Package settings** → **Change visibility** → **Public**.

Так на сервере не понадобится `docker login` и токены — просто анонимный
`pull`. Если предпочитаешь держать образы приватными — тогда придётся
один раз выполнить на сервере `docker login ghcr.io` с personal access
token (scope `read:packages`).

## 4. Первый ручной деплой

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod pull
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
docker compose -f docker-compose.prod.yml ps
```

Проверка:

```bash
curl http://localhost/
curl http://localhost/api/games
curl -I http://localhost/admin/
```

Дальше то же самое по публичному IP из браузера: `http://<IP>/`,
`http://<IP>/admin/` (логин — `DJANGO_SUPERUSER_USERNAME`/`DJANGO_SUPERUSER_PASSWORD`
из `.env.prod`).

## 5. Настроить автодеплой в GitHub

В репозитории → Settings → Secrets and variables → Actions → New repository
secret:

| Secret | Значение |
|---|---|
| `SSH_HOST` | публичный IP сервера |
| `SSH_USER` | пользователь для SSH (тот, кто в группе `docker` и владеет `/opt/board-games`) |
| `SSH_PRIVATE_KEY` | приватный ключ для входа на сервер (лучше отдельный deploy-ключ, не личный) |
| `SSH_PORT` | опционально, если SSH не на 22 |
| `DEPLOY_PATH` | опционально, если репозиторий не в `/opt/board-games` |

`GITHUB_TOKEN` для пуша образов в GHCR заводить не нужно — он у GitHub
Actions встроенный, работает сам по себе.

Приватный ключ для `SSH_PRIVATE_KEY` — заведи отдельную пару именно под
деплой (не переиспользуй личный `~/.ssh/id_ed25519`):

```bash
ssh-keygen -t ed25519 -f deploy_key -N "" -C "gh-actions-deploy"
# deploy_key.pub добавить на сервер в ~/.ssh/authorized_keys того пользователя,
# что указан в SSH_USER
cat deploy_key.pub >> ~/.ssh/authorized_keys   # выполнить на сервере
# содержимое deploy_key (приватный) целиком — в секрет SSH_PRIVATE_KEY
```

После этого пуш/мердж в `main` гоняет `build-and-test` → `build-and-push`
(собирает образы и пушит в GHCR) → `deploy`: копирует свежий
`docker-compose.prod.yml` на сервер по SCP и по SSH выполняет
`docker compose pull && up -d`. Сборка целиком происходит на раннерах
GitHub — сервер только скачивает готовый файл и готовые образы, никакой
нагрузки на его CPU/RAM. `.env.prod` при этом не трогается — CI его не
видит и не перезаписывает, это чисто серверный файл.

## 6. Откат

Каждый образ в GHCR пушится с двумя тегами: `latest` и SHA коммита. Чтобы
откатиться на конкретную версию — найди нужный коммит в истории на GitHub
(вкладка **Commits**) и укажи его SHA в `.env.prod`:

```bash
cd /opt/board-games
nano .env.prod                           # раскомментировать/добавить:
                                          #   IMAGE_TAG=<sha-коммита>
docker compose -f docker-compose.prod.yml --env-file .env.prod pull
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

Чтобы вернуться на актуальную версию — убрать `IMAGE_TAG` из `.env.prod`
(или поставить `IMAGE_TAG=latest`) и повторить `pull && up -d`.

## Дальше (по желанию, не сделано сейчас)

**Домен + HTTPS.** Когда появится домен: направить A-запись на IP сервера,
поставить [Caddy](https://caddyserver.com/) перед контейнером `frontend`
(или заменить nginx на Caddy в `frontend/Dockerfile.prod` — он сам получает
и продлевает сертификат Let's Encrypt) либо `certbot` + `nginx`. Не забыть
обновить `DJANGO_ALLOWED_HOSTS`/`DJANGO_CSRF_TRUSTED_ORIGINS` на `https://`.

**Бэкапы БД.** Простой вариант — cron на сервере:

```bash
# /etc/cron.d/board-games-backup
0 3 * * * root docker exec bg-db pg_dump -U boardgames boardgames | gzip > /opt/backups/boardgames-$(date +\%F).sql.gz
```

С ротацией старых файлов (`find /opt/backups -mtime +14 -delete`) и
опционально выгрузкой куда-то за пределы сервера (S3-совместимое хранилище,
rsync на другую машину).
