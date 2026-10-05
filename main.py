from app.application.notification_factory import NotificationFactory
from app.application.notification_service import NotificationService
from app.application.preference_service import PreferenceService
from app.infrastructure.mock_notification_sender import (
    MockNotificationSender,
)
from app.simulation.game_engine import GameEngine
from app.simulation.social_system import SocialSystem
from app.domain.enums import Category


def main() -> None:
    """Build the notification system and run example scenarios."""

    sender = MockNotificationSender()
    factory = NotificationFactory()
    preferences = PreferenceService()

    notification_service = NotificationService(
        factory=factory,
        preference_service=preferences,
        sender=sender,
    )

    game_engine = GameEngine(notification_service)
    social_system = SocialSystem(notification_service)

    preferences.set_enabled(
    user_id=1,
    category={
        Category.GAME,
        Category.SOCIAL,
    },
    enabled=False,
)

    print("\n--- Game Events ---")

    game_engine.player_leveled_up(
        user_id=1,
        level=15,
    )

    game_engine.item_acquired(
        user_id=1,
        item="SwordOfAzeroth",
    )

    game_engine.challenge_completed(
        user_id=1,
        challenge="Dragon Slayer",
    )

    game_engine.player_attacked(
        attacker_id=5,
        defender_id=2,
    )

    game_engine.player_defeated(
        attacker_id=5,
        defeated_id=2,
    )

    print("\n--- Social Events ---")
    
    

    social_system.friend_request_sent(
        sender_id=3,
        recipient_id=1,
    )

    social_system.friend_request_accepted(
        accepter_id=1,
        requester_id=3,
    )

    social_system.new_follower(
        follower_id=5,
        followed_id=1,
    )

    print("\n--- Preference Test ---")

   
    status = social_system.new_follower(
        follower_id=5,
        followed_id=1,
    )

    print(f"Social notification status: {status}")

    print("\nNotification simulation completed.")


if __name__ == "__main__":
    main()