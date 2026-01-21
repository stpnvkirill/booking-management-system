from infrastructure.database.models.booking import Booking as Mdl  # noqa: INP001

from app.infrastructure.database.models.users import User


class MessageFormatter:
    """Форматирование сообщений для напоминаний"""

    @staticmethod
    def _get_user_name(user: User) -> str:
        return user.first_name or user.username or "Uvazhaemyj klient"

    @staticmethod
    def _format_duration(booking) -> str:
        if hasattr(booking, "end_time") and booking.end_time:
            duration = booking.end_time - booking.start_time
            hours = duration.total_seconds() // 3600
            minutes = (duration.total_seconds() % 3600) // 60

            if hours > 0:
                return f"{int(hours)} ch {int(minutes)} min"
            return f"{int(minutes)} min"
        return "1 chas"

    @classmethod
    def format_24h_message(cls, booking, user: User) -> str:
        start_time = booking.start_time.strftime("%d.%m.%Y v %H:%M")
        user_name = cls._get_user_name(user)
        duration_text = Mdl.duration(booking)

        return (
            f"🔔 <b>Napominanie o bronirovanii</b>\n\n"
            f"Zdravstvujte, {user_name}!\n\n"
            f"Cherez 24 chasa u vas zapolneno bronirovanie:\n"
            f"🕐 <b>Vremya nachala:</b> {start_time}\n"
            f"⏳ <b>Prodolzhitel'nost':</b> {duration_text}\n\n"
            f"Pozhalujsta, podtverdite vashe uchastie.\n"
        )

    @classmethod
    def format_1h_message(cls, booking, user: User) -> str:
        start_time = booking.start_time.strftime("%H:%M")
        user_name = cls._get_user_name(user)
        duration_text = Mdl.duration(booking)

        return (
            f"⏰ <b>Skoro nachinaem!</b>\n\n"
            f"{user_name}, napominaem, chto cherez 1 chas:\n"
            f"🕐 <b>Nachalo v:</b> {start_time}\n"
            f"⏳ <b>Prodolzhitel'nost':</b> {duration_text}\n\n"
            f"Rekomenduem pribyt' za 10-15 minut do nachala."
        )
