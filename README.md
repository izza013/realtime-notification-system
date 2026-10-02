# Real-Time Notification System

A Python-based real-time notification system designed for an online gaming platform.

The system receives game and social events, converts them into user notifications, checks user preferences, and delivers enabled notifications through a mock notification sender.

## Features

- Game event notifications
  - Player Level Up
  - Item Acquired
  - Challenge Completed
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
- Unit and integration tests
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

The factory uses Python's `singledispatchmethod` to dispatch based on the event type.

This keeps event-specific notification creation separate from notification orchestration logic.

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

Preferences are stored per user and per category:

```text
User 1
├── GAME   → enabled
└── SOCIAL → disabled
```

Preferences are independent between users.

If no preference has been configured, notifications are enabled by default.

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
| FriendRequestSent | Social | Request recipient |
| FriendRequestAccepted | Social | Original requester |
| NewFollower | Social | Followed player |

## Running the Project

This project uses `uv`.

Install dependencies:

```bash
uv sync
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
- Game event generation
- Social event generation
- End-to-end notification flow
- Notification suppression
- Unsupported events
- Notification delivery failures

Current test suite:

```text
24 passed
```

## Example

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
