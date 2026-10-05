class NotificationError(Exception):
    """Base exception for notification system errors."""


class UnsupportedEventError(NotificationError):
    """Raised when the system does not support an event type."""


class DeliveryError(NotificationError):
    """Raised when a notification cannot be delivered."""