from app.application.event_handler import EventHandler
from app.domain.enums import DeliveryStatus
from app.domain.events import (
    FriendRequestAccepted,
    FriendRequestSent,
    NewFollower,
)


class SocialSystem:
    """Simulates social actions that produce domain events."""

    def __init__(self, event_handler: EventHandler) -> None:
        self._event_handler = event_handler

    def friend_request_sent(
        self,
        sender_id: int,
        recipient_id: int,
    ) -> DeliveryStatus:
        """Simulate one player sending a friend request."""
        event = FriendRequestSent(
            sender_id=sender_id,
            recipient_id=recipient_id,
        )
        return self._event_handler.handle(event)

    def friend_request_accepted(
        self,
        accepter_id: int,
        requester_id: int,
    ) -> DeliveryStatus:
        """Simulate a player accepting a friend request."""
        event = FriendRequestAccepted(
            accepter_id=accepter_id,
            requester_id=requester_id,
        )
        return self._event_handler.handle(event)

    def new_follower(
        self,
        follower_id: int,
        followed_id: int,
    ) -> DeliveryStatus:
        """Simulate one player following another player."""
        event = NewFollower(
            follower_id=follower_id,
            followed_id=followed_id,
        )
        return self._event_handler.handle(event)