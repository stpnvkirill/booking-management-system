# Docker Setup & Build Instructions

## Профили

Проект использует два профиля:
- **default** (разработка): БД + Redis (без backend и frontend)
- **prod** (production): Все сервисы (backend, frontend, БД, Redis)

---

## 🚀 Production сборка и запуск

### 1. Выключить все контейнеры

```bash
docker compose --profile prod down
```

### 2. Пересобрать и запустить в режиме production

```bash
docker compose --profile prod up -d --build
```

### 3. Проверить статус всех контейнеров

```bash
docker compose --profile prod ps
```

Должны быть запущены:
- `bms-backend` (порт 80)
- `bms-frontend` (порт 4173)
- `bms-db` (порт 6432)
- `bms-redis` (порт 6379)

### 4. Просмотреть логи

Все логи:
```bash
docker compose --profile prod logs -f
```

Логи конкретного сервиса:
```bash
docker compose --profile prod logs -f backend
docker compose --profile prod logs -f frontend
```

## ⚡ Быстрая команда (один шаг)

Выключить, пересобрать и запустить в production:

```bash
docker compose --profile prod down && docker compose --profile prod up -d --build && docker compose --profile prod logs -f
```

---

## 💻 Development режим (БД + Redis, без backend/frontend)

Если нужны только БД и Redis:

```bash
docker compose up -d --build
docker compose ps
```

---

## 🌐 Доступ к приложению

После запуска с профилем `prod`:
- **Frontend**: http://localhost:4173
- **Backend API**: http://localhost:80
- **PostgreSQL**: localhost:6432
- **Redis**: localhost:6379

---

## 🗑️ Полная очистка

### Без потери данных (сохранить БД и Redis)

```bash
docker compose --profile prod down
docker system prune -a
docker compose --profile prod up -d --build
```

### С потерей данных (полная очистка)

```bash
docker compose --profile prod down -v
docker system prune -a --volumes
docker compose --profile prod up -d --build
```

---

## 🔧 Решение проблем

### Контейнер не поднимается

```bash
docker compose --profile prod logs backend
docker compose --profile prod logs frontend
```

### Ошибка при сборке frontend (TypeScript ошибки)

Проверьте, что нет неиспользуемых переменных:
```bash
cd frontend
npm run lint
```

### Долгая первая сборка

Первый запуск может занять 30-60 секунд. Последующие будут быстрее благодаря кэшу.

### Порты уже заняты

```bash
docker compose --profile prod down -v
docker compose --profile prod up -d --build
```
