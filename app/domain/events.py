from pydantic import BaseModel, ConfigDict


class PlayerLeveledUp(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    user_id: int
    level: int


class ItemAcquired(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    user_id: int
    item: str


class ChallengeCompleted(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    user_id: int
    challenge: str

class PlayerAttacked(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    attacker_id: int
    defender_id: int


class PlayerDefeated(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    attacker_id: int
    defeated_id: int

class FriendRequestSent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    sender_id: int
    recipient_id: int


class FriendRequestAccepted(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    accepter_id: int
    requester_id: int


class NewFollower(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    follower_id: int
    followed_id: int