from app.domain.events import (
    ChallengeCompleted,
    FriendRequestAccepted,
    FriendRequestSent,
    ItemAcquired,
    NewFollower,
    PlayerAttacked,
    PlayerDefeated,
    PlayerLeveledUp,
)
from app.domain.exceptions import UnsupportedEventError
from app.domain.notification import Notification
from app.application.notification_builders import (
    ChallengeCompletedBuilder,
    FriendRequestAcceptedBuilder,
    FriendRequestSentBuilder,
    ItemAcquiredBuilder,
    NewFollowerBuilder,
    PlayerAttackedBuilder,
    PlayerDefeatedBuilder,
    PlayerLeveledUpBuilder,
)


class NotificationFactory:
    """Creates notifications using event-specific builders."""

    def __init__(self):
        self._builders = {
            PlayerLeveledUp: PlayerLeveledUpBuilder(),
            ItemAcquired: ItemAcquiredBuilder(),
            ChallengeCompleted: ChallengeCompletedBuilder(),
            PlayerAttacked: PlayerAttackedBuilder(),
            PlayerDefeated: PlayerDefeatedBuilder(),
            FriendRequestSent: FriendRequestSentBuilder(),
            FriendRequestAccepted: FriendRequestAcceptedBuilder(),
            NewFollower: NewFollowerBuilder(),
        }

    def create(self, event: object) -> Notification:
        """Create a notification for the given event."""

        builder = self._builders.get(type(event))

        if builder is None:
            raise UnsupportedEventError(
                f"Unsupported event type: {type(event).__name__}"
            )

        return builder.build(event)