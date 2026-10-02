from app.application.notification_factory import NotificationFactory
from app.application.notification_service import NotificationService
from app.application.preference_service import PreferenceService
from app.domain.enums import Category
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