"""Business metrics for Prometheus monitoring."""

from prometheus_client import Counter, Histogram

# Booking metrics
booking_created_total = Counter(
    "booking_created_total",
    "Total number of bookings created",
    ["source", "customer_id", "resource_id"],
)

booking_cancelled_total = Counter(
    "booking_cancelled_total",
    "Total number of bookings cancelled",
    ["source", "customer_id", "resource_id"],
)

booking_duration_seconds = Histogram(
    "booking_duration_seconds",
    "Duration of bookings in seconds",
    ["customer_id", "resource_id"],
    buckets=[300, 600, 1800, 3600, 7200, 14400, 28800, 86400],  # 5min to 24h
)

# Bot metrics
bot_messages_total = Counter(
    "bot_messages_total",
    "Total number of messages processed by bot",
    ["bot_id", "chat_type", "handler"],
)

bot_message_processing_seconds = Histogram(
    "bot_message_processing_seconds",
    "Time spent processing bot messages",
    ["bot_id", "handler"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
)

# Business metrics registry
business_metrics = [
    booking_created_total,
    booking_cancelled_total,
    booking_duration_seconds,
    bot_messages_total,
    bot_message_processing_seconds,
]
