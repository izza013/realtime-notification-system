from app.application.event_handler import EventHandler
from app.domain.enums import DeliveryStatus
from app.domain.events import (
    ChallengeCompleted,
    ItemAcquired,
    PlayerAttacked,
    PlayerDefeated,
    PlayerLeveledUp,
)


class GameEngine:
    """Simulates game actions that produce domain events."""

    def __init__(self, event_handler: EventHandler) -> None:
        self._event_handler = event_handler

    def player_leveled_up(
        self,
        user_id: int,
        level: int,
    ) -> DeliveryStatus:
        """Simulate a player reaching a new level."""
        event = PlayerLeveledUp(
            user_id=user_id,
            level=level,
        )
        return self._event_handler.handle(event)

    def item_acquired(
        self,
        user_id: int,
        item: str,
    ) -> DeliveryStatus:
        """Simulate a player acquiring an item."""
        event = ItemAcquired(
            user_id=user_id,
            item=item,
        )
        return self._event_handler.handle(event)

    def challenge_completed(
        self,
        user_id: int,
        challenge: str,
    ) -> DeliveryStatus:
        """Simulate a player completing a challenge."""
        event = ChallengeCompleted(
            user_id=user_id,
            challenge=challenge,
        )
        return self._event_handler.handle(event)

    def player_attacked(
        self,
        attacker_id: int,
        defender_id: int,
    ) -> DeliveryStatus:
        """Simulate one player attacking another."""
        event = PlayerAttacked(
            attacker_id=attacker_id,
            defender_id=defender_id,
        )
        return self._event_handler.handle(event)

    def player_defeated(
        self,
        attacker_id: int,
        defeated_id: int,
    ) -> DeliveryStatus:
        """Simulate one player defeating another."""
        event = PlayerDefeated(
            attacker_id=attacker_id,
            defeated_id=defeated_id,
        )
        return self._event_handler.handle(event)