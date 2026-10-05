from app.application.notification_factory import NotificationFactory
from app.application.notification_service import NotificationService
from app.application.preference_service import PreferenceService
from app.domain.enums import Category, DeliveryStatus
from app.infrastructure.mock_notification_sender import (
    MockNotificationSender,
)
from app.simulation.game_engine import GameEngine
from app.simulation.social_system import SocialSystem


def create_system() -> tuple[
    GameEngine,
    SocialSystem,
    PreferenceService,
    MockNotificationSender,
]:
    factory = NotificationFactory()
    preferences = PreferenceService()
    sender = MockNotificationSender()

    notification_service = NotificationService(
        factory=factory,
        preference_service=preferences,
        sender=sender,
    )

    game_engine = GameEngine(notification_service)
    social_system = SocialSystem(notification_service)

    return (
        game_engine,
        social_system,
        preferences,
        sender,
    )


def test_game_event_reaches_notification_sender() -> None:
    game_engine, _, _, sender = create_system()

    game_engine.player_leveled_up(
        user_id=1,
        level=15,
    )

    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 1
    assert notification.category == Category.GAME
    assert notification.message == (
        "Congratulations! You've reached level 15!"
    )

def test_player_attacked_reaches_sender() -> None:
    game_engine, _, _, sender = create_system()

    game_engine.player_attacked(
        attacker_id=5,
        defender_id=2,
    )

    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 2
    assert notification.category == Category.GAME
    assert notification.message == "Player '5' attacked you."

def test_player_defeated_reaches_sender() -> None:
    game_engine, _, _, sender = create_system()

    game_engine.player_defeated(
        attacker_id=5,
        defeated_id=2,
    )

    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 2
    assert notification.category == Category.GAME
    assert notification.message == "Player '5' defeated you."

def test_pvp_event_is_suppressed_when_game_notifications_are_disabled() -> None:
    game_engine, _, preferences, sender = create_system()

    preferences.set_enabled(
        user_id=2,
        category=Category.GAME,
        enabled=False,
    )

    game_engine.player_attacked(
        attacker_id=5,
        defender_id=2,
    )

    assert sender.sent_notifications == []

def test_social_event_reaches_notification_sender() -> None:
    _, social_system, _, sender = create_system()

    social_system.friend_request_sent(
        sender_id=3,
        recipient_id=1,
    )

    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 1
    assert notification.category == Category.SOCIAL
    assert notification.message == (
        "Player '3' has sent you a friend request."
    )


def test_disabled_category_prevents_delivery() -> None:
    game_engine, _, preferences, sender = create_system()

    preferences.set_enabled(
        user_id=1,
        category=Category.GAME,
        enabled=False,
    )

    game_engine.player_leveled_up(
        user_id=1,
        level=15,
    )

    assert len(sender.sent_notifications) == 0


def test_item_acquired_reaches_sender() -> None:
    game_engine, _, _, sender = create_system()

    game_engine.item_acquired(user_id=2, item="SwordOfAzeroth")

    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 2
    assert notification.category == Category.GAME
    assert "SwordOfAzeroth" in notification.message


def test_challenge_completed_reaches_sender() -> None:
    game_engine, _, _, sender = create_system()

    game_engine.challenge_completed(user_id=1, challenge="Dragon Slayer")

    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 1
    assert notification.category == Category.GAME
    assert "Dragon Slayer" in notification.message


def test_friend_request_accepted_reaches_original_requester() -> None:
    _, social_system, _, sender = create_system()

    social_system.friend_request_accepted(accepter_id=1, requester_id=3)

    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 3
    assert notification.category == Category.SOCIAL
    assert notification.message == (
        "Player '1' has accepted your friend request."
    )


def test_new_follower_reaches_followed_player() -> None:
    _, social_system, _, sender = create_system()

    social_system.new_follower(follower_id=5, followed_id=1)

    assert len(sender.sent_notifications) == 1

    notification = sender.sent_notifications[0]

    assert notification.user_id == 1
    assert notification.category == Category.SOCIAL
    assert notification.message == "Player '5' is now following you."


def test_disabled_social_category_prevents_delivery() -> None:
    _, social_system, preferences, sender = create_system()

    preferences.set_enabled(
        user_id=1,
        category=Category.SOCIAL,
        enabled=False,
    )

    social_system.friend_request_sent(sender_id=3, recipient_id=1)
    social_system.new_follower(follower_id=5, followed_id=1)

    assert sender.sent_notifications == []


def test_disabling_social_does_not_block_game_notifications() -> None:
    game_engine, social_system, preferences, sender = create_system()

    preferences.set_enabled(
        user_id=1,
        category=Category.SOCIAL,
        enabled=False,
    )

    social_status = social_system.friend_request_sent(3, 1)
    game_status = game_engine.player_leveled_up(1, 15)

    assert social_status == DeliveryStatus.SUPPRESSED
    assert game_status == DeliveryStatus.DELIVERED
    assert len(sender.sent_notifications) == 1
    assert sender.sent_notifications[0].category == Category.GAME


def test_one_users_preferences_do_not_block_another_user() -> None:
    game_engine, _, preferences, sender = create_system()

    preferences.set_enabled(
        user_id=1,
        category=Category.GAME,
        enabled=False,
    )

    game_engine.player_leveled_up(user_id=1, level=15)
    game_engine.player_leveled_up(user_id=2, level=10)

    assert len(sender.sent_notifications) == 1
    assert sender.sent_notifications[0].user_id == 2


def test_multiple_events_for_same_user_are_all_delivered() -> None:
    game_engine, social_system, _, sender = create_system()

    game_engine.player_leveled_up(user_id=1, level=15)
    game_engine.item_acquired(user_id=1, item="SwordOfAzeroth")
    social_system.friend_request_sent(sender_id=3, recipient_id=1)

    assert [n.user_id for n in sender.sent_notifications] == [1, 1, 1]
    assert [n.category for n in sender.sent_notifications] == [
        Category.GAME,
        Category.GAME,
        Category.SOCIAL,
    ]


def test_status_is_returned_to_the_caller() -> None:
    _, social_system, preferences, _ = create_system()

    assert social_system.new_follower(5, 1) == DeliveryStatus.DELIVERED

    preferences.set_enabled(1, Category.SOCIAL, enabled=False)

    assert social_system.new_follower(5, 1) == DeliveryStatus.SUPPRESSED
