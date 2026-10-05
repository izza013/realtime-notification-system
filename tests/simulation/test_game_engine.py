from unittest.mock import Mock

from app.application.event_handler import EventHandler
from app.domain.enums import DeliveryStatus
from app.domain.events import (
    ChallengeCompleted,
    ItemAcquired,
    PlayerAttacked,
    PlayerDefeated,
    PlayerLeveledUp,
)
from app.simulation.game_engine import GameEngine


def test_player_leveled_up_creates_event() -> None:
    event_handler = Mock(spec=EventHandler)
    game_engine = GameEngine(event_handler)

    game_engine.player_leveled_up(
        user_id=1,
        level=15,
    )

    event_handler.handle.assert_called_once()

    event = event_handler.handle.call_args.args[0]

    assert isinstance(event, PlayerLeveledUp)
    assert event.user_id == 1
    assert event.level == 15


def test_item_acquired_creates_event() -> None:
    event_handler = Mock(spec=EventHandler)
    game_engine = GameEngine(event_handler)

    game_engine.item_acquired(
        user_id=2,
        item="SwordOfAzeroth",
    )

    event_handler.handle.assert_called_once()

    event = event_handler.handle.call_args.args[0]

    assert isinstance(event, ItemAcquired)
    assert event.user_id == 2
    assert event.item == "SwordOfAzeroth"


def test_challenge_completed_creates_event() -> None:
    event_handler = Mock(spec=EventHandler)
    game_engine = GameEngine(event_handler)

    game_engine.challenge_completed(
        user_id=3,
        challenge="Dragon Slayer",
    )

    event_handler.handle.assert_called_once()

    event = event_handler.handle.call_args.args[0]

    assert isinstance(event, ChallengeCompleted)
    assert event.user_id == 3
    assert event.challenge == "Dragon Slayer"

def test_player_attacked_creates_event(mocker) -> None:
    handler = mocker.Mock()
    game_engine = GameEngine(handler)

    game_engine.player_attacked(
        attacker_id=5,
        defender_id=2,
    )
    


    event = handler.handle.call_args.args[0]

    assert isinstance(event, PlayerAttacked)
    assert event.attacker_id == 5
    assert event.defender_id == 2

def test_player_defeated_creates_event() -> None:
    event_handler = Mock(spec=EventHandler)
    game_engine = GameEngine(event_handler)

    game_engine.player_defeated(
        attacker_id=5,
        defeated_id=2,
    )

    event_handler.handle.assert_called_once()

    event = event_handler.handle.call_args.args[0]

    assert isinstance(event, PlayerDefeated)
    assert event.attacker_id == 5
    assert event.defeated_id == 2


def test_game_engine_returns_handler_status() -> None:
    event_handler = Mock(spec=EventHandler)
    event_handler.handle.return_value = DeliveryStatus.SUPPRESSED
    game_engine = GameEngine(event_handler)

    assert game_engine.player_leveled_up(1, 15) == DeliveryStatus.SUPPRESSED
    assert game_engine.item_acquired(1, "Sword") == DeliveryStatus.SUPPRESSED
    assert (
        game_engine.challenge_completed(1, "Dragon Slayer")
        == DeliveryStatus.SUPPRESSED
    )
    assert game_engine.player_attacked(5, 2) == DeliveryStatus.SUPPRESSED
    assert game_engine.player_defeated(5, 2) == DeliveryStatus.SUPPRESSED


def test_item_acquired_hands_event_over_only_once() -> None:
    event_handler = Mock(spec=EventHandler)
    game_engine = GameEngine(event_handler)

    game_engine.item_acquired(user_id=1, item="SwordOfAzeroth")

    event_handler.handle.assert_called_once()
