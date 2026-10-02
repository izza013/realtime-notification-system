from enum import StrEnum


class Category(StrEnum):
    GAME = "game"
    SOCIAL = "social"


class DeliveryStatus(StrEnum):
    DELIVERED = "delivered"
    SUPPRESSED = "suppressed"