# Real-Time Notification System

A Python-based real-time notification system designed for an online gaming platform.

The system receives game and social events, converts them into user notifications, checks user preferences, and delivers enabled notifications through a mock notification sender.

## Features

- Game event notifications
  - Player Level Up
  - Item Acquired
  - Challenge Completed
  - Player Attacked (PvP)
  - Player Defeated (PvP)
- Social event notifications
  - Friend Request Sent
  - Friend Request Accepted
  - New Follower
- Per-user notification preferences
- Independent Game and Social notification categories
- Notification suppression when a category is disabled
- Mock notification delivery
- Immutable domain models using Pydantic
- Dependency injection
- Protocol-based abstractions
- Explicit error handling
- Unit, simulation and integration tests (45 tests)
- Python 3.12 + uv

## Architecture

The system follows a simple layered architecture:

```text
┌─────────────────────┐
│   Simulation Layer  │
│                     │
│  GameEngine         │
│  SocialSystem       │
└──────────┬──────────┘
           │
           │ Domain Events
           ▼
┌─────────────────────┐
│  Application Layer  │
│                     │
│ NotificationService │
│ NotificationFactory │
│ PreferenceService   │
└──────────┬──────────┘
           │
           │ Notification
           ▼
┌─────────────────────┐
│ Infrastructure      │
│                     │
│ MockNotification    │
│ Sender              │
└─────────────────────┘
```

### Event Processing Flow

```text
Game/Social Event
       │
       ▼
NotificationService
       │
       ▼
NotificationFactory
       │
       ▼
Notification
       │
       ▼
PreferenceService
       │
       ├── Disabled ──► Suppressed
       │
       └── Enabled
              │
              ▼
      NotificationSender
              │
              ▼
          Delivered
```

## Project Structure

```text
realtime-notification/
│
├── app/
│   ├── application/
│   │   ├── event_handler.py
│   │   ├── notification_builders.py
│   │   ├── notification_factory.py
│   │   ├── notification_sender.py
│   │   ├── notification_service.py
│   │   └── preference_service.py
│   │
│   ├── domain/
│   │   ├── enums.py
│   │   ├── events.py
│   │   ├── exceptions.py
│   │   └── notification.py
│   │
│   ├── infrastructure/
│   │   └── mock_notification_sender.py
│   │
│   └── simulation/
│       ├── game_engine.py
│       └── social_system.py
│
├── tests/
│   ├── application/
│   ├── integration/
│   └── simulation/
│
├── main.py
├── requirements.txt
├── AI_USAGE.md
├── PLAN.md
├── README.md
├── pyproject.toml
├── uv.lock
└── .python-version
```

## Design Decisions

### Domain Events

Events represent things that happened in the gaming platform.

For example:

```python
PlayerLeveledUp(
    user_id=1,
    level=15,
)
```

The event itself does not know anything about notification delivery.

This keeps the domain model independent from infrastructure concerns.

### Notification Factory

`NotificationFactory` converts domain events into `Notification` objects.

It does not build messages itself. It holds a registry that maps each event type to an event-specific builder
(`PlayerLeveledUpBuilder`, `FriendRequestSentBuilder`, ...), looks up the builder by `type(event)`, and calls its
`build(event)` method. If no builder is registered, it raises `UnsupportedEventError`.

```python
self._builders = {
    PlayerLeveledUp: PlayerLeveledUpBuilder(),
    FriendRequestSent: FriendRequestSentBuilder(),
    ...
}
```

Each builder lives in `notification_builders.py` and is responsible for one thing: the recipient, category and
message text for one event type. This keeps message creation separate from the lookup logic and from notification
orchestration. Supporting a new event means adding an event, a builder and one registry entry; existing builders
are not touched.

### Notification Service

`NotificationService` coordinates the complete workflow:

```text
Event
 ↓
Create Notification
 ↓
Check Preference
 ↓
Send Notification
```

It does not know how notifications are physically delivered.

### Notification Sender

The sender is represented by a `Protocol`:

```python
class NotificationSender(Protocol):
    def send(self, notification: Notification) -> None:
        ...
```

The current implementation is a mock sender because actual notification display/delivery is outside the scope of the challenge.

A production implementation could later send notifications through another mechanism without changing the application service.

### User Preferences

`PreferenceService` stores only what each user has **disabled**, per category:

```text
_disabled = {
    1: {SOCIAL},          # user 1 turned Social off
    2: {GAME, SOCIAL},    # user 2 turned both off
}
```

- `set_enabled(user_id, category, *, enabled)` disables a category by adding it to the user's set, and re-enables it by
  removing it. `category` can be a single `Category` or a set of categories, and `enabled` must be passed by keyword.
- `is_enabled(user_id, category)` returns `True` unless the category is in that user's disabled set.

```python
preferences.set_enabled(1, Category.SOCIAL, enabled=False)
preferences.set_enabled(2, {Category.GAME, Category.SOCIAL}, enabled=False)
```

Because only disabled categories are stored:

- A user who has never configured anything receives every notification (enabled by default).
- Preferences are independent between users, and disabling one category does not affect the others.
- Reading a user's preferences never creates an entry for them.

`NotificationService` calls `is_enabled(notification.user_id, notification.category)` once per event, after the
notification is built. If the category is disabled it returns `SUPPRESSED` and the sender is never called. Otherwise the
notification is sent. How preferences are stored is hidden inside `PreferenceService`, so it could change (for example
to a database) without changing the service.

Example for a user with Social disabled:

| Event | Category | Result |
|---|---|---|
| Level up, item acquired, challenge completed, attacked, defeated | Game (enabled) | Delivered |
| Friend request, friend accepted, new follower | Social (disabled) | Suppressed |

### Dependency Injection

Components receive their dependencies through constructors.

For example:

```python
notification_service = NotificationService(
    factory=factory,
    preference_service=preferences,
    sender=sender,
)
```

This makes components easier to test and replace.

## Supported Events

| Event | Category | Notification Recipient |
|---|---|---|
| PlayerLeveledUp | Game | Player |
| ItemAcquired | Game | Player |
| ChallengeCompleted | Game | Player |
| PlayerAttacked | Game | Attacked player (defender) |
| PlayerDefeated | Game | Defeated player |
| FriendRequestSent | Social | Request recipient |
| FriendRequestAccepted | Social | Original requester |
| NewFollower | Social | Followed player |

## Running the Project

This project uses `uv`.

Install dependencies:

```bash
uv sync
```

Alternatively, with pip (Python 3.12+):

```bash
pip install -r requirements.txt
```

Run the simulation:

```bash
uv run python main.py
```

## Running Tests

Run all tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check app tests
```

Run type checking:

```bash
uv run mypy app
```

## Test Coverage

The test suite covers:

- Notification creation
- Event-to-notification mapping
- User preferences
- Preference isolation between users
- Game event generation (including PvP)
- Social event generation
- Simulation methods returning the delivery status
- End-to-end notification flow for every event type
- Notification suppression per category and per user
- Disabling one category not affecting the other
- Unsupported events
- Notification delivery failures

Current test suite:

```text
45 passed
```

## Example

Every `GameEngine` and `SocialSystem` method returns a `DeliveryStatus`
(`DELIVERED` or `SUPPRESSED`), so callers can see what happened.

Running:

```python
game_engine.player_leveled_up(
    user_id=1,
    level=15,
)
```

produces:

```text
[Notification] User 1: Congratulations! You've reached level 15!
```

If the user has disabled Game notifications:

```text
Game notification status: suppressed
```

No notification is delivered.

## Error Handling

Unsupported event types raise:

```text
UnsupportedEventError
```

Notification delivery failures are wrapped as:

```text
DeliveryError
```

This keeps infrastructure failures from leaking directly into the application layer.

PvP events notify the player on the receiving end:

```text
[Notification] User 2: Player '5' attacked you.
[Notification] User 2: Player '5' defeated you.
```

## Future Improvements

A production implementation could extend the system with:

- Persistent user preferences
- Real notification providers
- Event queues/message brokers
- Retry mechanisms
- Notification delivery tracking
- Rate limiting
- Notification history
- Additional event categories
- Push/email/SMS channels

These features are intentionally outside the scope of this challenge.

## Development Process

The implementation was developed incrementally:

1. Defined the domain events and notification model.
2. Added notification categories and delivery statuses.
3. Implemented notification creation.
4. Added user preferences.
5. Added notification orchestration.
6. Added a mock notification sender.
7. Added game and social event simulations.
8. Added unit tests.
9. Added integration tests.
10. Added the executable demonstration.
11. Cleaned the project structure and configured uv for the `app/` package.
