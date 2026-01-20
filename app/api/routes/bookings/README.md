# API Routes для бронирований

## Описание

Этот модуль предоставляет REST API для управления бронированиями ресурсов. Включает функциональность создания, получения и отмены бронирований с полной валидацией и проверками безопасности.

## Endpoints

### POST `/api/bookings/`

Создает новое бронирование ресурса.

**Требуется аутентификация:** Да

**Тело запроса:**
```json
{
  "customer_id": "uuid",
  "resource_id": 1,
  "start_time": "2026-01-19T14:00:00",
  "end_time": "2026-01-19T16:00:00"
}
```

**Параметры:**
- `customer_id` (UUID): ID клиента, владельца ресурса
- `resource_id` (int): ID ресурса для бронирования
- `start_time` (datetime): Начало периода бронирования (ISO 8601)
- `end_time` (datetime): Конец периода бронирования (ISO 8601)

**Успешный ответ (200):**
```json
{
  "id": 1,
  "user_id": "uuid",
  "resource_id": 1,
  "start_time": "2026-01-19T14:00:00",
  "end_time": "2026-01-19T16:00:00"
}
```

**Возможные ошибки:**

| Статус | Причина |
|--------|---------|
| 400 | Время окончания должно быть позже времени начала |
| 400 | Ресурс не найден или не принадлежит клиенту |
| 400 | Ресурс недоступен на выбранный период (есть конфликтующие бронирования) |
| 401 | Не авторизован |
| 403 | Нет доступа к этому клиенту |

---

### GET `/api/bookings/`

Получает все бронирования текущего пользователя для ресурсов клиента.

**Требуется аутентификация:** Да

**Параметры запроса:**
- `customer_id` (UUID, обязательный): ID клиента для фильтрации ресурсов

**Успешный ответ (200):**
```json
{
  "bookings": [
    {
      "id": 1,
      "user_id": "uuid",
      "resource_id": 1,
      "start_time": "2026-01-19T14:00:00",
      "end_time": "2026-01-19T16:00:00"
    }
  ]
}
```

**Возможные ошибки:**

| Статус | Причина |
|--------|---------|
| 401 | Не авторизован |
| 403 | Нет доступа к этому клиенту |

---

### DELETE `/api/bookings/{id}`

Отменяет (удаляет) бронирование.

**Требуется аутентификация:** Да

**Параметры пути:**
- `id` (int): ID бронирования для отмены

**Успешный ответ (204):**
Нет содержимого (бронирование успешно отменено)

**Возможные ошибки:**

| Статус | Причина |
|--------|---------|
| 403 | Бронирование не найдено или принадлежит другому пользователю |
| 401 | Не авторизован |

---

## Pydantic Schemas

### `BookingCreate`

Схема для создания бронирования:
```python
class BookingCreate(BaseModel):
    customer_id: UUID
    resource_id: int
    start_time: datetime
    end_time: datetime
```

### `BookingResponse`

Схема для ответа при создании/получении:
```python
class BookingResponse(BaseModel):
    id: int
    user_id: UUID
    resource_id: int
    start_time: datetime
    end_time: datetime
```

### `BookingListResponse`

Схема для списка бронирований:
```python
class BookingListResponse(BaseModel):
    bookings: list[BookingResponse]
```

---

## Примеры использования

### Создание бронирования

```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Authorization: Bearer <compressed_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "550e8400-e29b-41d4-a716-446655440000",
    "resource_id": 1,
    "start_time": "2026-01-19T14:00:00",
    "end_time": "2026-01-19T16:00:00"
  }'
```

### Получение всех бронирований

```bash
curl -X GET "http://localhost:8000/api/bookings/?customer_id=550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer <compressed_token>"
```

### Отмена бронирования

```bash
curl -X DELETE http://localhost:8000/api/bookings/1 \
  -H "Authorization: Bearer <compressed_token>"
```

---

## Аутентификация

Все endpoints требуют аутентификации через заголовок `Authorization` с _сжатым_ токеном:

```
Authorization: Bearer <compressed_token>
```

Сжатый токен получается путём кодирования UUID в base64 формате. Подробнее смотрите в документации `app/api/security.py`.

---

## Валидация и обработка ошибок

### Валидация входных данных
- Проверка что `end_time > start_time`
- Проверка существования ресурса и его владельца
- Проверка прав доступа (принадлежность клиенту)

### Проверка конфликтов
- Автоматическая проверка пересечений с существующими бронированиями
- Возвращение 400 ошибки если ресурс недоступен

### Безопасность
- Только создатель бронирования может его отменить
- Клиент проверяется на совпадение с владельцем ресурса
- Все операции в БД используют `AsyncSession` с корректной обработкой транзакций

---

## Интеграция с BookingService

Все операции делегируются `BookingService`:

```python
from app.domain.services.bookings import booking_service

# Создание
booking = await booking_service.create_booking(params)

# Проверка доступности
is_available = await booking_service.check_availability(...)

# Получение бронирований
bookings = await booking_service.get_user_bookings(...)

# Отмена
success = await booking_service.cancel_booking(...)
```

Это обеспечивает отделение бизнес-логики от HTTP слоя и упрощает тестирование.

---

## Заметки для разработчиков

- Все операции асинхронные и используют `AsyncSession`
- Используется `provider.inject_session` декоратор для инъекции сессии БД
- Пагинация не реализована (GET возвращает все бронирования пользователя)
- Дополнительные поля (описание, примечания) могут быть добавлены в будущем
