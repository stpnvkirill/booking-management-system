# BookingService - Сервис управления бронированиями

## Описание

`BookingService` — это бизнес-слой приложения, отвечающий за управление бронированиями ресурсов. Сервис обеспечивает:

- **Проверку доступности** ресурса на выбранный период времени
- **Создание бронирований** с валидацией владения ресурсом и отсутствия конфликтов
- **Получение бронирований** пользователя по его учетной записи и клиенту
- **Отмену бронирований** с проверкой принадлежности

## Основные компоненты

### DataClass `BookingParams`

Параметры для создания нового бронирования:

```python
@dataclass
class BookingParams:
    user_id: UUID              # ID пользователя, создающего бронирование
    customer_id: UUID          # ID клиента (владельца ресурса)
    resource_id: int           # ID ресурса для бронирования
    start_time: datetime       # Начало периода бронирования
    end_time: datetime         # Конец периода бронирования
```

### Методы BookingService

#### `check_availability(resource_id, start_time, end_time)`

Проверяет, доступен ли ресурс на указанный период времени.

**Параметры:**
- `resource_id` (int): ID ресурса
- `start_time` (datetime): Начало периода
- `end_time` (datetime): Конец периода

**Возвращает:** `True` если ресурс доступен (нет конфликтов), иначе `False`

**Логика:** Использует SQL запрос для поиска пересекающихся бронирований:
```sql
WHERE resource_id = X AND start_time < new_end AND end_time > new_start
```

#### `create_booking(params: BookingParams)`

Создает новое бронирование с полной валидацией.

**Параметры:**
- `params` (BookingParams): Параметры бронирования

**Возвращает:** Объект `Booking` или `None` если валидация не прошла

**Валидация:**
1. Проверка, что `end_time > start_time`
2. Проверка существования ресурса и принадлежности клиенту
3. Проверка доступности ресурса на выбранный период

#### `get_user_bookings(user_id, customer_id)`

Получает все бронирования пользователя для ресурсов определённого клиента.

**Параметры:**
- `user_id` (UUID): ID пользователя
- `customer_id` (UUID): ID клиента

**Возвращает:** Список объектов `Booking`

#### `cancel_booking(booking_id, user_id)`

Отменяет (удаляет) бронирование с проверкой прав.

**Параметры:**
- `booking_id` (int): ID бронирования для отмены
- `user_id` (UUID): ID пользователя, запрашивающего отмену

**Возвращает:** `True` при успехе, `False` если бронирование не найдено или не принадлежит пользователю

#### `get_booking_with_resource(booking_id)`

Получает бронирование со связанными данными ресурса (для форматирования ответов).

**Параметры:**
- `booking_id` (int): ID бронирования

**Возвращает:** Кортеж `(Booking, Resource)` или `None` если бронирование не найдено

## Использование

```python
from app.domain.services.bookings import BookingService, BookingParams
from datetime import datetime, timedelta
from uuid import UUID

service = BookingService()

# Создание бронирования
params = BookingParams(
    user_id=UUID("..."),
    customer_id=UUID("..."),
    resource_id=1,
    start_time=datetime.now(),
    end_time=datetime.now() + timedelta(hours=2)
)
booking = await service.create_booking(params, session=session)

# Проверка доступности
is_available = await service.check_availability(
    resource_id=1,
    start_time=datetime.now(),
    end_time=datetime.now() + timedelta(hours=2)
)

# Получение бронирований пользователя
bookings = await service.get_user_bookings(
    user_id=UUID("..."),
    customer_id=UUID("...")
)

# Отмена бронирования
success = await service.cancel_booking(
    booking_id=1,
    user_id=UUID("...")
)
```

## Архитектурные решения

### Инъекция зависимостей

Все методы используют декоратор `@provider.inject_session` для автоматического внедрения `AsyncSession`, обеспечивая:
- Единую точку управления сеансами БД
- Возможность тестирования с предоставленной сессией
- Асинхронную работу с PostgreSQL

### Проверка конфликтов

Алгоритм обнаружения пересечений использует условие:
```
start_time < новый_конец AND конец > новое_начало
```

Это позволяет корректно обрабатывать все случаи пересечений временных интервалов.

### Безопасность

- Всегда проверяется принадлежность ресурса клиенту перед созданием
- Бронирование может быть отменено только его создателем
- Удаление выполняется через `AsyncSession.execute()` для корректной работы с транзакциями

## Обработка ошибок

- Методы возвращают `None` или `False` в случае ошибок валидации
- При исключениях БД автоматически выполняется `rollback()`
- Клиент API получает понятные HTTP ошибки через проверку в маршрутизаторе
