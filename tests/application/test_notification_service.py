from app.application.notification_factory import NotificationFactory
from app.application.notification_service import NotificationService
from app.application.preference_service import PreferenceService
from app.domain.enums import Category, DeliveryStatus
from app.domain.events import PlayerLeveledUp
from app.infrastructure.mock_notification_sender import (
    MockNotificationSender,
)


def create_service() -> tuple[
    NotificationService,
    PreferenceService,
    MockNotificationSender,
]:
    factory = NotificationFactory()
    preferences = PreferenceService()
    sender = MockNotificationSender()

    service = NotificationService(
        factory=factory,
        preference_service=preferences,
        sender=sender,
    )

    return service, preferences, sender


def test_enabled_notification_is_delivered() -> None:
    service, _, sender = create_service()

    event = PlayerLeveledUp(
        user_id=1,
        level=15,
    )

    result = service.handle(event)

    assert result == DeliveryStatus.DELIVERED
    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 1
    assert notification.category == Category.GAME
    assert notification.message == (
        "Congratulations! You've reached level 15!"
    )


def test_disabled_category_suppresses_notification() -> None:
    service, preferences, sender = create_service()

    preferences.set_enabled(
        user_id=1,
        category=Category.GAME,
        enabled=False,
    )

    event = PlayerLeveledUp(
        user_id=1,
        level=15,
    )

    result = service.handle(event)

    assert result == DeliveryStatus.SUPPRESSED
    assert len(sender.sent_notifications) == 0