from prometheus_client import Counter, Histogram

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
booking_status_changed_total = Counter(
    "booking_status_changed_total",
    "Total number of booking status changes",
    ["from_status", "to_status", "customer_id", "resource_id"],
)
booking_duration_seconds = Histogram(
    "booking_duration_seconds",
    "Duration of bookings in seconds",
    ["customer_id", "resource_id"],
    buckets=[300, 600, 1800, 3600, 7200, 14400, 28800, 86400],
)
booking_lead_time_seconds = Histogram(
    "booking_lead_time_seconds",
    "Time between booking creation and start time in seconds",
    ["customer_id", "resource_id"],
    buckets=[60, 300, 900, 1800, 3600, 7200, 14400, 28800, 86400, 172800, 604800],
)
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
business_metrics = [
    booking_created_total,
    booking_cancelled_total,
    booking_status_changed_total,
    booking_duration_seconds,
    booking_lead_time_seconds,
    bot_messages_total,
    bot_message_processing_seconds,
]
booking_created_total.labels(
    source="unknown",
    customer_id="unknown",
    resource_id="unknown",
)
booking_cancelled_total.labels(
    source="unknown",
    customer_id="unknown",
    resource_id="unknown",
)
booking_status_changed_total.labels(
    from_status="unknown",
    to_status="unknown",
    customer_id="unknown",
    resource_id="unknown",
)
booking_duration_seconds.labels(customer_id="unknown", resource_id="unknown")
booking_lead_time_seconds.labels(customer_id="unknown", resource_id="unknown")
bot_messages_total.labels(bot_id="unknown", chat_type="unknown", handler="unknown")
bot_message_processing_seconds.labels(bot_id="unknown", handler="unknown")
