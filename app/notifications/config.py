from dataclasses import dataclass


@dataclass
class Config:
    # Интервалы проверки (в минутах)
    CHECK_INTERVAL: int = 5  # Проверка каждые 5 минут
    REMINDER_24H: int = 24 * 60  # 24 часа в минутах
    REMINDER_1H: int = 60  # 1 час в минутах


# Создаем экземпляр конфигурации
config = Config()
