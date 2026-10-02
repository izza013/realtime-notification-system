class NotificationError(Exception):
    """Base exception for notification system errors."""


class InvalidEventError(NotificationError):
    """Raised when an event contains invalid data."""


class UnsupportedEventError(NotificationError):
    """Raised when the system does not support an event type."""


class DeliveryError(NotificationError):
    """Raised when a notification cannot be delivered."""