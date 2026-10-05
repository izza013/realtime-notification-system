from app.application.preference_service import PreferenceService
from app.domain.enums import Category


def test_categories_are_enabled_by_default() -> None:
    preferences = PreferenceService()

    assert preferences.is_enabled(1, Category.GAME)
    assert preferences.is_enabled(1, Category.SOCIAL)


def test_disabling_one_category_leaves_the_other_enabled() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        1,
        Category.SOCIAL,
        enabled=False,
    )

    assert not preferences.is_enabled(1, Category.SOCIAL)
    assert preferences.is_enabled(1, Category.GAME)


def test_preferences_are_per_user() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        1,
        Category.SOCIAL,
        enabled=False,
    )

    assert not preferences.is_enabled(1, Category.SOCIAL)
    assert preferences.is_enabled(2, Category.SOCIAL)


def test_category_can_be_re_enabled() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        1,
        Category.GAME,
        enabled=False,
    )

    preferences.set_enabled(
        1,
        Category.GAME,
        enabled=True,
    )

    assert preferences.is_enabled(1, Category.GAME)


def test_multiple_categories_can_be_disabled() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        1,
        {Category.GAME, Category.SOCIAL},
        enabled=False,
    )

    assert not preferences.is_enabled(1, Category.GAME)
    assert not preferences.is_enabled(1, Category.SOCIAL)


def test_multiple_categories_can_be_re_enabled() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        1,
        {Category.GAME, Category.SOCIAL},
        enabled=False,
    )

    preferences.set_enabled(
        1,
        {Category.GAME, Category.SOCIAL},
        enabled=True,
    )

    assert preferences.is_enabled(1, Category.GAME)
    assert preferences.is_enabled(1, Category.SOCIAL)


def test_disabling_category_for_one_user_does_not_affect_another() -> None:
    preferences = PreferenceService()

    preferences.set_enabled(
        1,
        Category.GAME,
        enabled=False,
    )

    assert not preferences.is_enabled(1, Category.GAME)
    assert preferences.is_enabled(2, Category.GAME)