# Деплой на сервер

Прод-раскладка: один Ubuntu 24.04 сервер, `docker-compose.prod.yml`,
единственный публичный порт — 80 (контейнер `frontend`, он же nginx и
reverse-proxy на backend/admin). Автодеплой — GitHub Actions при пуше в
`main` (`.github/workflows/ci-cd.yml`).

## 1. Один раз настроить сервер

Подключись по SSH под пользователем с sudo.

```bash
sudo apt update && sudo apt upgrade -y

# Docker Engine + compose plugin
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker   # или перелогинься, чтобы группа применилась

# порт 80 наружу (порт свободен — ничего больше на нём не висит)
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw enable   # если ufw ещё не включён
sudo ufw status
```

Клонируй репозиторий:

```bash
sudo mkdir -p /opt/board-games
sudo chown $USER:$USER /opt/board-games
git clone https://github.com/zhukovaab/board-games.git /opt/board-games
cd /opt/board-games
```

Если репозиторий приватный — либо клонируй по SSH с deploy-ключом
(`git clone git@github.com:zhukovaab/board-games.git`), либо через HTTPS с
personal access token.

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

Файл `.env.prod` в git не попадает (в `.gitignore`) — трогать его руками
на сервере и всё.

## 3. Первый ручной деплой

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
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

## 4. Настроить автодеплой в GitHub

В репозитории → Settings → Secrets and variables → Actions → New repository
secret:

| Secret | Значение |
|---|---|
| `SSH_HOST` | публичный IP сервера |
| `SSH_USER` | пользователь для SSH (тот, под кем клонировали репозиторий и кто в группе `docker`) |
| `SSH_PRIVATE_KEY` | приватный ключ для входа на сервер (лучше отдельный deploy-ключ, не личный) |
| `SSH_PORT` | опционально, если SSH не на 22 |
| `DEPLOY_PATH` | опционально, если репозиторий не в `/opt/board-games` |

Приватный ключ для `SSH_PRIVATE_KEY` — заведи отдельную пару именно под
деплой (не переиспользуй личный `~/.ssh/id_ed25519`):

```bash
ssh-keygen -t ed25519 -f deploy_key -N "" -C "gh-actions-deploy"
# deploy_key.pub добавить на сервер в ~/.ssh/authorized_keys того пользователя,
# что указан в SSH_USER
cat deploy_key.pub >> ~/.ssh/authorized_keys   # выполнить на сервере
# содержимое deploy_key (приватный) целиком — в секрет SSH_PRIVATE_KEY
```

После этого пуш/мердж в `main` гоняет `build-and-test`, и если всё зелёное —
job `deploy` заходит по SSH и выполняет `git reset --hard origin/main` +
`docker compose ... up -d --build`.

## 5. Откат

Если новый деплой сломался:

```bash
cd /opt/board-games
git log --oneline -5          # найти рабочий коммит
git reset --hard <commit-sha>
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

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
