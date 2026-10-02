from functools import singledispatchmethod

from app.domain.enums import Category
from app.domain.events import (
    ChallengeCompleted,
    PlayerAttacked,
    PlayerDefeated,
    FriendRequestAccepted,
    FriendRequestSent,
    ItemAcquired,
    NewFollower,
    PlayerLeveledUp,
)
from app.domain.exceptions import UnsupportedEventError
from app.domain.notification import Notification


class NotificationFactory:
    """Creates notifications from supported domain events."""

    @singledispatchmethod
    def create(self, event: object) -> Notification:
        """Create a notification for the given event."""
        raise UnsupportedEventError(
            f"Unsupported event type: {type(event).__name__}"
        )

    @create.register
    def _(self, event: PlayerLeveledUp) -> Notification:
        return Notification(
            user_id=event.user_id,
            category=Category.GAME,
            message=f"Congratulations! You've reached level {event.level}!",
        )

    @create.register
    def _(self, event: ItemAcquired) -> Notification:
        return Notification(
            user_id=event.user_id,
            category=Category.GAME,
            message=f"You've acquired the legendary {event.item}!",
        )

    @create.register
    def _(self, event: ChallengeCompleted) -> Notification:
        return Notification(
            user_id=event.user_id,
            category=Category.GAME,
            message=(
                f"Congratulations! You've completed "
                f"the challenge '{event.challenge}'!"
            ),
        )
    @create.register
    def _(self, event: PlayerAttacked) -> Notification:
        return Notification(
            user_id=event.defender_id,
            category=Category.GAME,
            message=f"Player '{event.attacker_id}' attacked you.",
        )
    @create.register
    def _(self, event: PlayerDefeated) -> Notification:
        return Notification(
            user_id=event.defeated_id,
            category=Category.GAME,
            message=f"Player '{event.attacker_id}' defeated you.",
        )


    @create.register
    def _(self, event: FriendRequestSent) -> Notification:
        return Notification(
            user_id=event.recipient_id,
            category=Category.SOCIAL,
            message=(
                f"Player '{event.sender_id}' has sent you "
                f"a friend request."
            ),
        )

    @create.register
    def _(self, event: FriendRequestAccepted) -> Notification:
        return Notification(
            user_id=event.requester_id,
            category=Category.SOCIAL,
            message=(
                f"Player '{event.accepter_id}' has accepted "
                f"your friend request."
            ),
        )

    @create.register
    def _(self, event: NewFollower) -> Notification:
        return Notification(
            user_id=event.followed_id,
            category=Category.SOCIAL,
            message=(
                f"Player '{event.follower_id}' is now following you."
            ),
        )