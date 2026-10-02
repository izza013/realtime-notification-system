# AI Usage

## 1. AI Tools Used

The following AI tools were used during the development of this coding challenge:

- **ChatGPT** — used as the primary development assistant for understanding requirements, system design, implementation guidance, debugging, testing, documentation, and step-by-step development.
- **GitHub Copilot** — used as a coding assistant during development for code suggestions and implementation support.
- **Claude** — used primarily for research and learning, including finding relevant articles and resources about production patterns for generic agent/notification-style systems and understanding how similar concepts are handled in real-world systems.

AI was used as an assistant throughout the process, not as a replacement for understanding, implementation, testing, or review.

---

## 2. Overall AI-Assisted Development Process

The development process followed this sequence:

```text
Read the challenge myself
        ↓
Understand requirements and deliverables
        ↓
Ask ChatGPT to break down the challenge
        ↓
Research related production concepts using Claude
        ↓
Divide the challenge into smaller requirements
        ↓
Design the architecture
        ↓
Implement one component at a time
        ↓
Write and run tests
        ↓
Debug and refine
        ↓
Run quality checks
        ↓
Document the solution and AI-assisted workflow
```

The goal was to use AI to accelerate learning and implementation while keeping the development process understandable and reviewable.

---

## 3. Step 1 — Read and Understand the Challenge Myself

Before using AI, I read the coding challenge document myself.

The first goal was to understand:

- What the system is expected to do.
- What types of events need to be supported.
- How notifications should be generated.
- How user preferences should affect delivery.
- What parts of the system are in scope.
- What parts are explicitly out of scope.
- What deliverables are expected.
- What optional requirements exist.
- What needs to be demonstrated through the final implementation.

This was important because I wanted the AI assistance to be based on my understanding of the actual requirements rather than simply asking AI to build the entire project from the document.

---

## 4. Step 2 — Requirements Breakdown with ChatGPT

After reading the document, I asked ChatGPT to break the challenge down into smaller parts.

The main purpose of this step was to clarify:

- Functional requirements.
- Domain concepts.
- Event types.
- Notification types.
- User preference behavior.
- Event-to-notification flow.
- Required components.
- Testing requirements.
- Suggested project structure.
- What should and should not be implemented.

Instead of immediately writing code, I used the discussion to build a mental model of the system.

### Example prompt pattern

> "Explain this coding challenge to me and break down exactly what is required, what the deliverables are, and what is in and out of scope."

I then asked follow-up questions whenever something was unclear.

This helped turn the original challenge document into a list of smaller engineering tasks.

---

## 5. Step 3 — Research with Claude

After understanding the requirements, I used Claude for additional research and learning.

I asked Claude to provide articles and resources related to the use case so I could understand how similar concepts are handled in production.

The research focused on topics such as:

- Generic notification systems.
- Event-driven architecture.
- Event handling and dispatching.
- Notification preferences.
- Separation of domain and infrastructure concerns.
- Production patterns for agent/event-based systems.
- Designing systems that can be extended with additional event types.

The purpose was not to copy an existing implementation. It was to understand common production approaches and use that knowledge when designing the solution.

---

## 6. Step 4 — Divide the Requirements into Small Parts

Once the requirements and related concepts were clearer, I divided the implementation into smaller pieces.

The project was approached incrementally rather than building everything at once.

The major pieces were:

1. Project setup.
2. Domain categories and statuses.
3. Domain events.
4. Notification model.
5. Domain exceptions.
6. Notification factory.
7. User preference service.
8. Notification sender abstraction.
9. Notification service.
10. Mock notification sender.
11. Game simulation.
12. Social simulation.
13. Unit tests.
14. Integration tests.
15. Error-handling tests.
16. Application entry point.
17. Code quality checks.
18. Documentation.

This made it easier to understand the responsibility of each component and verify each step before moving forward.

---

## 7. Step 5 — Step-by-Step Development with ChatGPT

The implementation was developed interactively with ChatGPT.

Rather than asking for one large final implementation, I used a workflow where each component was discussed, implemented, tested, and then reviewed before moving to the next one.

### Project setup

I decided to use:

- Python 3.12
- `uv` for project and dependency management
- `pytest` for testing
- `ruff` for linting
- `mypy` for static type checking
- Pydantic for domain models

ChatGPT helped explain the setup commands, project structure, dependency configuration, and the reasoning behind the tools.

### Architecture

The project was separated into:

```text
app/
├── domain/
├── application/
├── infrastructure/
└── simulation/
```

The purpose of this separation was to keep business concepts independent from infrastructure and simulation code.

The dependency direction was kept simple:

```text
domain
   ↑
application
   ↑
infrastructure / simulation
```

The architecture was discussed before implementation so that individual classes had clear responsibilities.

---

## 8. Step 6 — Implementing the Domain

The first implementation stage focused on the domain.

This included:

- Notification categories.
- Delivery status.
- Game events.
- Social events.
- Notification model.
- Domain exceptions.

The events were modeled explicitly instead of passing arbitrary dictionaries around.

For example, the system has separate event types for:

- Player level up.
- Item acquired.
- Challenge completed.
- Friend request sent.
- Friend request accepted.
- New follower.

Pydantic models were used to validate and represent these events.

---

## 9. Step 7 — Notification Creation

The next step was deciding how events should become notifications.

Different approaches were discussed, including:

- A large `if/elif` chain.
- A builder-style approach.
- Type-based dispatch.

The final implementation uses Python's `singledispatchmethod`.

The reasoning was that each event type can have its own notification creation logic while keeping the factory extensible and avoiding a large conditional block.

This was an example of AI-assisted design discussion rather than simply accepting generated code.

---

## 10. Step 8 — Preferences and Delivery Flow

The next pieces were:

- `PreferenceService`
- `NotificationSender`
- `NotificationService`

The main processing flow became:

```text
Game/Social Event
       ↓
NotificationService
       ↓
NotificationFactory
       ↓
Notification
       ↓
PreferenceService
       ↓
Enabled?
   ↙       ↘
 No         Yes
 ↓           ↓
Suppress    Sender
             ↓
          Delivered
```

The preference system stores settings per user and per category.

For example:

```text
User 1
 ├── Game: enabled/disabled
 └── Social: enabled/disabled
```

One important behavior that was verified during development was that changing one user's preferences must not affect another user's preferences.

---

## 11. Step 9 — Mock Infrastructure

Because the challenge explicitly states that the actual notification UI/display is outside the scope, a mock notification sender was implemented.

The mock sender:

- Receives a `Notification`.
- Stores sent notifications in memory.
- Prints the notification to the console.

This provides a simple way to demonstrate that the notification reached the delivery layer without implementing an actual mobile/web notification system.

---

## 12. Step 10 — Simulation Layer

The simulation layer represents parts of a gaming platform that generate events.

Two simulation components were implemented:

- `GameEngine`
- `SocialSystem`

For example:

```text
GameEngine
    ↓
PlayerLeveledUp event
    ↓
NotificationService
```

and:

```text
SocialSystem
    ↓
FriendRequestSent event
    ↓
NotificationService
```

The simulation layer therefore demonstrates how different parts of a larger application could feed events into the notification system.

---

## 13. Step 11 — Testing with AI Assistance

Tests were developed alongside the implementation rather than only at the end.

The test suite covers:

### Notification service

- Notification is delivered when enabled.
- Notification is suppressed when disabled.
- Sender failures are converted into the domain-level `DeliveryError`.

### Notification factory

Each supported event type was tested to verify:

- Correct recipient.
- Correct category.
- Correct notification message.

Unsupported event types were also tested.

### Preference service

Tests verify:

- Notifications are enabled by default.
- Game preferences can be disabled.
- Social preferences can be disabled.
- Categories are independent.
- Users have isolated preferences.

### Simulation layer

Game and social simulation methods were tested to ensure they create and forward the correct domain events.

### Integration

End-to-end flows were tested to verify:

```text
Simulation
   ↓
Event
   ↓
Notification Service
   ↓
Preference Check
   ↓
Mock Sender
```

---

## 14. AI-Assisted Debugging and Refinement

AI was also used during debugging.

Examples of issues discussed and resolved included:

- Python import/path configuration.
- `uv` project structure.
- The generated `src/` layout from `uv`.
- Configuring the project to use the `app` package.
- Test discovery.
- Understanding why preferences were suppressing some notifications.
- Verifying recipient logic for social events.
- Improving the demonstration in `main.py`.
- Reviewing architecture and responsibilities between layers.

The important part of the workflow was that suggested fixes were actually run and verified locally.

---

## 15. Example Prompt Patterns Used

The AI-assisted development used iterative prompts rather than one large prompt.

Examples of the types of prompts used were:

### Requirement understanding

> "Break this coding challenge down for me and explain exactly what is required and what the deliverables are."

### Architecture

> "Let's start with the project structure. Explain why we should separate domain, application, infrastructure, and simulation."

### Incremental implementation

> "Let's do this step by step. Explain it first and then we'll implement it."

### Design discussion

> "Can't we create a builder of these notifications and call it in the notification factory?"

This led to a comparison of approaches before settling on the chosen design.

### Debugging

> "It works now, what's next?"

and follow-up questions were used after running commands locally.

### Testing

> "Let's add tests for this behavior."

### Documentation

> "Let's generate README.md."

The process was conversational and iterative: understand → implement → run → inspect → fix → test → continue.

---

## 16. Human Decisions and AI Contributions

AI contributed significantly to the development process, but the final implementation was reviewed and validated manually.

### AI was used for

- Requirement breakdown.
- Architecture suggestions.
- Explaining design patterns.
- Code scaffolding.
- Test suggestions.
- Debugging guidance.
- Explaining errors.
- Documentation drafting.
- Reviewing implementation decisions.

### I was responsible for

- Reading the original challenge.
- Understanding and confirming requirements.
- Choosing the final architecture.
- Asking follow-up questions.
- Choosing between alternative implementation approaches.
- Writing/running commands locally.
- Reviewing generated code.
- Modifying code when required.
- Running tests and quality checks.
- Verifying actual application behavior.
- Deciding what was ultimately included in the submission.

For example, different approaches to the notification factory were discussed before `singledispatchmethod` was selected.

---

## 17. AI Was Not Treated as the Source of Truth

The AI-generated suggestions were treated as development assistance rather than automatically correct answers.

The workflow was:

```text
AI suggestion
    ↓
Understand the suggestion
    ↓
Implement or modify it
    ↓
Run it locally
    ↓
Run tests
    ↓
Inspect the result
    ↓
Accept, modify, or reject
```

This was especially important during debugging because an AI suggestion can be technically plausible but still incorrect for the actual project structure or requirements.

One example during development was an incorrect test-count assumption. The final verified test suite contains **24 passing tests**, and this was confirmed by running `uv run pytest`.

---

## 18. Development and Validation Tools

The final development workflow used:

| Tool | Purpose |
|---|---|
| ChatGPT | Requirements, architecture, implementation guidance, debugging, testing, documentation |
| GitHub Copilot | Coding assistance and code suggestions |
| Claude | Research and production-pattern learning |
| Python 3.12 | Programming language/runtime |
| uv | Project, dependency, and environment management |
| Pydantic | Domain model validation |
| pytest | Automated testing |
| pytest-mock | Test support |
| Ruff | Linting/code quality |
| mypy | Static type checking |
| Git/GitHub | Version control and submission |

---

## 19. Final Validation

Before considering the implementation complete, the project was validated locally.

The final checks included:

```bash
uv run pytest
uv run ruff check app tests
uv run mypy app
uv run python main.py
```

The test suite completed with:

```text
24 passed
```

Ruff and mypy checks were also run successfully, and the application simulation was executed through `main.py`.

---

## 20. Summary of the AI Workflow

The overall approach was:

1. **Read the challenge independently.**
2. **Use ChatGPT to clarify and break down the requirements.**
3. **Use Claude to research related production concepts and articles.**
4. **Divide the requirements into small engineering tasks.**
5. **Discuss architecture before implementation.**
6. **Implement one component at a time.**
7. **Use ChatGPT/Copilot for implementation assistance.**
8. **Run the code locally after each meaningful change.**
9. **Use AI to help investigate errors and design questions.**
10. **Write unit and integration tests.**
11. **Run linting and static type checking.**
12. **Review and validate the final behavior manually.**
13. **Document both the solution and the AI-assisted development process.**

The main principle throughout the project was to use AI as an engineering partner for learning, reasoning, implementation assistance, and iteration while maintaining human review and verification of the final solution.
