from app.domain.notification import Notification


class MockNotificationSender:
    """Simulates delivering notifications to a user."""

    def __init__(self) -> None:
        self.sent_notifications: list[Notification] = []

    def send(self, notification: Notification) -> None:
        """Simulate sending a notification."""
        self.sent_notifications.append(notification)
        print(
            f"[Notification] User {notification.user_id}: "
            f"{notification.message}"
        )