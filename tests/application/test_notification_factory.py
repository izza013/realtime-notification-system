import pytest

from app.application.notification_factory import NotificationFactory
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
from app.domain.exceptions import UnsupportedEventError


def test_player_leveled_up_creates_game_notification() -> None:
    factory = NotificationFactory()

    notification = factory.create(
        PlayerLeveledUp(
            user_id=1,
            level=15,
        )
    )

    assert notification.user_id == 1
    assert notification.category == Category.GAME
    assert notification.message == (
        "Congratulations! You've reached level 15!"
    )


def test_item_acquired_creates_game_notification() -> None:
    factory = NotificationFactory()

    notification = factory.create(
        ItemAcquired(
            user_id=2,
            item="SwordOfAzeroth",
        )
    )

    assert notification.user_id == 2
    assert notification.category == Category.GAME
    assert notification.message == (
        "You've acquired the legendary SwordOfAzeroth!"
    )


def test_challenge_completed_creates_game_notification() -> None:
    factory = NotificationFactory()

    notification = factory.create(
        ChallengeCompleted(
            user_id=3,
            challenge="Dragon Slayer",
        )
    )

    assert notification.user_id == 3
    assert notification.category == Category.GAME
    assert notification.message == (
        "Congratulations! You've completed "
        "the challenge 'Dragon Slayer'!"
    )
def test_player_attacked_creates_game_notification() -> None:
    factory = NotificationFactory()

    notification = factory.create(
        PlayerAttacked(
            attacker_id=5,
            defender_id=2,
        )
    )

    assert notification.user_id == 2
    assert notification.category == Category.GAME
    assert notification.message == "Player '5' attacked you."
def test_player_defeated_creates_game_notification() -> None:
    factory = NotificationFactory()

    notification = factory.create(
        PlayerDefeated(
            attacker_id=5,
            defeated_id=2,
        )
    )

    assert notification.user_id == 2
    assert notification.category == Category.GAME
    assert notification.message == "Player '5' defeated you."


def test_friend_request_sent_creates_social_notification() -> None:
    factory = NotificationFactory()

    notification = factory.create(
        FriendRequestSent(
            sender_id=3,
            recipient_id=1,
        )
    )

    assert notification.user_id == 1
    assert notification.category == Category.SOCIAL
    assert notification.message == (
        "Player '3' has sent you a friend request."
    )


def test_friend_request_accepted_creates_social_notification() -> None:
    factory = NotificationFactory()

    notification = factory.create(
        FriendRequestAccepted(
            accepter_id=1,
            requester_id=3,
        )
    )

    assert notification.user_id == 3
    assert notification.category == Category.SOCIAL
    assert notification.message == (
        "Player '1' has accepted your friend request."
    )


def test_new_follower_creates_social_notification() -> None:
    factory = NotificationFactory()

    notification = factory.create(
        NewFollower(
            follower_id=5,
            followed_id=2,
        )
    )

    assert notification.user_id == 2
    assert notification.category == Category.SOCIAL
    assert notification.message == (
        "Player '5' is now following you."
    )


def test_unsupported_event_raises_error() -> None:
    factory = NotificationFactory()

    with pytest.raises(UnsupportedEventError):
        factory.create(object())