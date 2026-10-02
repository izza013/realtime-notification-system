from typing import Protocol

from app.domain.notification import Notification


class NotificationSender(Protocol):
    """Interface for delivering notifications."""

    def send(self, notification: Notification) -> None:
        """Send a notification to the intended recipient."""
        ...