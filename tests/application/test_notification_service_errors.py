import pytest

from app.application.notification_factory import NotificationFactory
from app.application.notification_service import NotificationService
from app.application.preference_service import PreferenceService
from app.domain.events import PlayerLeveledUp
from app.domain.exceptions import DeliveryError


class FailingNotificationSender:
    def send(self, notification: object) -> None:
        raise RuntimeError("Simulated delivery failure")


def test_sender_failure_raises_delivery_error() -> None:
    service = NotificationService(
        factory=NotificationFactory(),
        preference_service=PreferenceService(),
        sender=FailingNotificationSender(),
    )

    event = PlayerLeveledUp(
        user_id=1,
        level=15,
    )

    with pytest.raises(DeliveryError):
        service.handle(event)