from typing import Protocol

from app.domain.enums import DeliveryStatus


class EventHandler(Protocol):
    """Interface for components that process domain events."""

    def handle(self, event: object) -> DeliveryStatus:
        """Process an event and return its delivery status."""
        ...