from collections import defaultdict

from app.domain.enums import Category


class PreferenceService:
    """Manages user notification preferences."""

    def __init__(self) -> None:
        self._preferences: dict[int, dict[Category, bool]] = defaultdict(dict)

    def set_enabled(
        self,
        user_id: int,
        category: Category,
        enabled: bool,
    ) -> None:
        """Enable or disable a notification category for a user."""
        self._preferences[user_id][category] = enabled

    def is_enabled(
        self,
        user_id: int,
        category: Category,
    ) -> bool:
        """Return whether a notification category is enabled for a user."""
        return self._preferences[user_id].get(category, True)