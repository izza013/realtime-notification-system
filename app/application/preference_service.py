"""Per-user notification preferences."""

from dataclasses import dataclass, field

from app.domain.enums import Category


@dataclass
class PreferenceService:
    """Tracks which notification categories each user has disabled."""

    _disabled: dict[int, set[Category]] = field(default_factory=dict)


    def set_enabled(
        self,
        user_id: int,
        category: Category | set[Category],
        *,
        enabled: bool,
    ) -> None:
        """Enable or disable one or multiple notification categories."""

        categories = (
            {category}
            if isinstance(category, Category)
            else category
        )

        disabled = self._disabled.setdefault(user_id, set())

        if enabled:
            disabled.difference_update(categories)
        else:
            disabled.update(categories)
        

    def is_enabled(
        self,
        user_id: int,
        category: Category,
    ) -> bool:
        """Return whether notifications are enabled for a user."""
        return category not in self._disabled.get(user_id, set())