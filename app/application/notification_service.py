from app.application.notification_factory import NotificationFactory
from app.application.notification_sender import NotificationSender
from app.application.preference_service import PreferenceService
from app.domain.enums import DeliveryStatus
from app.domain.exceptions import DeliveryError


class NotificationService:
    """Coordinates event processing and notification delivery."""

    def __init__(
        self,
        factory: NotificationFactory,
        preference_service: PreferenceService,
        sender: NotificationSender,
    ) -> None:
        self._factory = factory
        self._preference_service = preference_service
        self._sender = sender

    def handle(self, event: object) -> DeliveryStatus:
        """Process an event and deliver its notification if enabled."""
        notification = self._factory.create(event)

        if not self._preference_service.is_enabled(
            notification.user_id,
            notification.category,
        ):
            return DeliveryStatus.SUPPRESSED

        try:
            self._sender.send(notification)
        except Exception as exc:
            raise DeliveryError(
                f"Failed to deliver notification to user "
                f"{notification.user_id}"
            ) from exc

        return DeliveryStatus.DELIVERED