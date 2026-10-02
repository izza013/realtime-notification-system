from app.application.preference_service import PreferenceService
from app.domain.enums import Category


def test_notifications_are_enabled_by_default() -> None:
    preferences = PreferenceService()

    assert preferences.is_enabled(
        user_id=1,
        category=Category.GAME,
    ) is True

    assert preferences.is_enabled(
        user_id=1,
        category=Category.SOCIAL,
    ) is True


def test_user_can_disable_game_notifications() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        user_id=1,
        category=Category.GAME,
        enabled=False,
    )

    assert preferences.is_enabled(
        user_id=1,
        category=Category.GAME,
    ) is False


def test_user_can_disable_social_notifications() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        user_id=1,
        category=Category.SOCIAL,
        enabled=False,
    )

    assert preferences.is_enabled(
        user_id=1,
        category=Category.SOCIAL,
    ) is False


def test_game_and_social_preferences_are_independent() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        user_id=1,
        category=Category.GAME,
        enabled=False,
    )

    preferences.set_enabled(
        user_id=1,
        category=Category.SOCIAL,
        enabled=True,
    )

    assert preferences.is_enabled(
        user_id=1,
        category=Category.GAME,
    ) is False

    assert preferences.is_enabled(
        user_id=1,
        category=Category.SOCIAL,
    ) is True


def test_preferences_are_isolated_between_users() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        user_id=1,
        category=Category.GAME,
        enabled=False,
    )

    assert preferences.is_enabled(
        user_id=1,
        category=Category.GAME,
    ) is False

    assert preferences.is_enabled(
        user_id=2,
        category=Category.GAME,
    ) is True