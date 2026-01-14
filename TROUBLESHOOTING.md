# Решение проблемы конфликта Telegram бота

## Проблема
Ошибка: `TelegramConflictError: Conflict: terminated by other getUpdates request`

Эта ошибка возникает, когда несколько экземпляров бота пытаются получать обновления одновременно.

## Решения

### 1. Проверка запущенных процессов Python

**Автоматическая проверка:**
```powershell
.\scripts\check_processes.ps1
```

**Или вручную:**
```powershell
Get-Process python,pythonw | Select-Object Id,ProcessName,Path,StartTime
```

Если найдете процессы, связанные с вашим проектом, завершите их:
```powershell
Stop-Process -Id <PID> -Force
```

**Или завершите все процессы Python:**
```powershell
Get-Process python,pythonw | Stop-Process -Force
```

### 2. Удаление webhook вручную

**Простой способ (без базы данных, только токен):**
```powershell
uv run python scripts/remove_webhook_simple.py YOUR_BOT_TOKEN
```

**Через базу данных:**
```powershell
uv run python scripts/remove_webhook.py
```

Или для конкретного бота (используйте bot_id из базы данных, например 8381146317):
```powershell
uv run python scripts/remove_webhook.py 8381146317
```

**Примечание:** Простой способ не требует подключения к базе данных - просто используйте токен бота из BotFather.

### 3. Проверка через Telegram Bot API

Вы можете проверить и удалить webhook напрямую через API:

1. Получить информацию о webhook:
```powershell
$token = "YOUR_BOT_TOKEN"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getWebhookInfo"
```

2. Удалить webhook:
```powershell
Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/deleteWebhook?drop_pending_updates=true"
```

### 4. Проверка Docker контейнеров

Если используете Docker, проверьте запущенные контейнеры:
```powershell
docker ps
```

Остановите контейнеры, если они запущены:
```powershell
docker stop <container_id>
```

### 5. Проверка других терминалов/сессий

Убедитесь, что вы не запустили бота в другом окне терминала или IDE.

## Автоматическое решение

Код теперь автоматически удаляет webhook перед запуском polling. Если проблема сохраняется:

1. Убедитесь, что нет других запущенных процессов
2. Запустите скрипт удаления webhook
3. Перезапустите приложение

