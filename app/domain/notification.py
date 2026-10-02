from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import Category


class Notification(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    user_id: int
    category: Category
    message: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )