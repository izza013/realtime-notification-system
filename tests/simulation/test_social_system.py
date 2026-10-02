from unittest.mock import Mock

from app.application.event_handler import EventHandler
from app.domain.events import (
    FriendRequestAccepted,
    FriendRequestSent,
    NewFollower,
)
from app.simulation.social_system import SocialSystem


def test_friend_request_sent_creates_event() -> None:
    event_handler = Mock(spec=EventHandler)
    social_system = SocialSystem(event_handler)

    social_system.friend_request_sent(
        sender_id=3,
        recipient_id=1,
    )

    event_handler.handle.assert_called_once()

    event = event_handler.handle.call_args.args[0]

    assert isinstance(event, FriendRequestSent)
    assert event.sender_id == 3
    assert event.recipient_id == 1


def test_friend_request_accepted_creates_event() -> None:
    event_handler = Mock(spec=EventHandler)
    social_system = SocialSystem(event_handler)

    social_system.friend_request_accepted(
        accepter_id=1,
        requester_id=3,
    )

    event_handler.handle.assert_called_once()

    event = event_handler.handle.call_args.args[0]

    assert isinstance(event, FriendRequestAccepted)
    assert event.accepter_id == 1
    assert event.requester_id == 3


def test_new_follower_creates_event() -> None:
    event_handler = Mock(spec=EventHandler)
    social_system = SocialSystem(event_handler)

    social_system.new_follower(
        follower_id=5,
        followed_id=2,
    )

    event_handler.handle.assert_called_once()

    event = event_handler.handle.call_args.args[0]

    assert isinstance(event, NewFollower)
    assert event.follower_id == 5
    assert event.followed_id == 2