from app.domain.enums import Category
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
from app.domain.notification import Notification


class PlayerLeveledUpBuilder:
    def build(self, event: PlayerLeveledUp) -> Notification:
        return Notification(
            user_id=event.user_id,
            category=Category.GAME,
            message=f"Congratulations! You've reached level {event.level}!",
        )


class ItemAcquiredBuilder:
    def build(self, event: ItemAcquired) -> Notification:
        return Notification(
            user_id=event.user_id,
            category=Category.GAME,
            message=f"You've acquired the legendary {event.item}!",
        )


class ChallengeCompletedBuilder:
    def build(self, event: ChallengeCompleted) -> Notification:
        return Notification(
            user_id=event.user_id,
            category=Category.GAME,
            message=(
                f"Congratulations! You've completed "
                f"the challenge '{event.challenge}'!"
            ),
        )


class PlayerAttackedBuilder:
    def build(self, event: PlayerAttacked) -> Notification:
        return Notification(
            user_id=event.defender_id,
            category=Category.GAME,
            message=f"Player '{event.attacker_id}' attacked you.",
        )


class PlayerDefeatedBuilder:
    def build(self, event: PlayerDefeated) -> Notification:
        return Notification(
            user_id=event.defeated_id,
            category=Category.GAME,
            message=f"Player '{event.attacker_id}' defeated you.",
        )


class FriendRequestSentBuilder:
    def build(self, event: FriendRequestSent) -> Notification:
        return Notification(
            user_id=event.recipient_id,
            category=Category.SOCIAL,
            message=f"Player '{event.sender_id}' has sent you a friend request.",
        )


class FriendRequestAcceptedBuilder:
    def build(self, event: FriendRequestAccepted) -> Notification:
        return Notification(
            user_id=event.requester_id,
            category=Category.SOCIAL,
            message=f"Player '{event.accepter_id}' has accepted your friend request.",
        )


class NewFollowerBuilder:
    def build(self, event: NewFollower) -> Notification:
        return Notification(
            user_id=event.followed_id,
            category=Category.SOCIAL,
            message=f"Player '{event.follower_id}' is now following you.",
        )