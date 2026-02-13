# LifeOS — Phase 1 MVP Scope

## 1. Goals

- Validate architecture with a working, deployable slice.
- Deliver core value: tasks, habits, expenses.
- Establish patterns for auth, audit, API, and DevOps.

---

## 2. User Stories (Phase 1)

### Auth & Users

- **US-A1**: As a user, I can register with email and password so that I have an account.
- **US-A2**: As a user, I can log in and receive a JWT so that I can call APIs.
- **US-A3**: As a user, I can refresh my token so that I stay logged in.
- **US-A4**: As a user, I can reset my password via email so that I can recover access.

### Productivity (Tasks & Planner)

- **US-P1**: As a user, I can create/edit/delete tasks with title, notes, due date, priority (Eisenhower), and status so that I manage my work.
- **US-P2**: As a user, I can list tasks filtered by date, status, priority so that I see my daily plan.
- **US-P3**: As a user, I can get a “today” view (daily planner) so that I see what’s due today.

### Habits

- **US-H1**: As a user, I can define habits (name, target frequency, e.g. daily) so that I track them.
- **US-H2**: As a user, I can log a habit check-in for a date so that I build streaks.
- **US-H3**: As a user, I can see my current streak and history per habit so that I stay motivated.

### Finance

- **US-F1**: As a user, I can create expense categories so that I organize spending.
- **US-F2**: As a user, I can log an expense (amount, category, date, note) so that I track spending.
- **US-F3**: As a user, I can set a simple monthly budget (category or total) so that I have a target.
- **US-F4**: As a user, I can get a basic report (e.g. by category for a month) so that I see where money goes.

---

## 3. Database Schema (Phase 1)

### Core

- **users**: Custom user model (email as identifier, optional profile fields). Prefer extending `AbstractUser` with `USERNAME_FIELD = 'email'`.
- **audit_log**: Request/action audit (user_id, action, resource, timestamp, IP, payload hash). Optional; can start with a simple table or middleware-logged model.

### Productivity

- **task**: id, user_id, title, notes, due_date, priority (urgent_important, urgent_not_important, not_urgent_important, not_urgent_not_important), status (todo, in_progress, done, cancelled), created_at, updated_at.
- **daily_planner**: Optional view/query over tasks for “today”; can be derived from tasks + date filter.

### Habits

- **habit**: id, user_id, name, target_frequency (daily, weekly, custom), target_count (e.g. 1 per day), created_at.
- **habit_check_in**: id, habit_id, user_id, date, completed (bool), notes, created_at. Unique constraint (habit_id, date) per user.

### Finance

- **expense_category**: id, user_id, name, icon/code (optional), created_at.
- **expense**: id, user_id, category_id, amount (Decimal), currency, date, note, created_at.
- **budget**: id, user_id, month (YYYY-MM or date), category_id (nullable for “total”), amount (Decimal), created_at.

---

## 4. API Endpoints (REST, v1)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /api/v1/auth/register/ | Register |
| POST   | /api/v1/auth/login/ | Login (JWT) |
| POST   | /api/v1/auth/refresh/ | Refresh token |
| POST   | /api/v1/auth/password-reset/ | Request reset |
| POST   | /api/v1/auth/password-reset/confirm/ | Confirm reset |
| GET    | /api/v1/me/ | Current user profile |
| GET/POST | /api/v1/tasks/ | List / create tasks |
| GET/PUT/PATCH/DELETE | /api/v1/tasks/:id/ | Task detail |
| GET    | /api/v1/tasks/today/ | Today’s tasks (planner) |
| GET/POST | /api/v1/habits/ | List / create habits |
| GET/PUT/PATCH/DELETE | /api/v1/habits/:id/ | Habit detail |
| GET/POST | /api/v1/habits/:id/check-ins/ | List / create check-ins |
| GET    | /api/v1/habits/:id/streak/ | Current streak |
| GET/POST | /api/v1/expense-categories/ | List / create categories |
| GET/POST | /api/v1/expenses/ | List / create expenses |
| GET    | /api/v1/expenses/report/ | Report (month, category) |
| GET/POST | /api/v1/budgets/ | List / create budgets |
| GET    | /api/health/ | Health check |

---

## 5. Phase 1 Deliverables Checklist

- [ ] Django project with apps: `core`, `users`, `productivity`, `habits`, `finance`.
- [ ] Custom user model + JWT auth (register, login, refresh, password reset).
- [ ] Audit logging (middleware or model).
- [ ] Task CRUD + today view; Eisenhower priority.
- [ ] Habit CRUD + check-ins + streak logic.
- [ ] Expense categories, expenses, budgets, basic report.
- [ ] OpenAPI schema (drf-spectacular or similar).
- [ ] Docker + docker-compose (app, PostgreSQL, Redis).
- [ ] GitHub Actions: lint (Ruff/Black), test (pytest), build image, push to ACR.
- [ ] README + ARCHITECTURE + run instructions.
- [ ] Tests targeting ~90% coverage for new code.

---

## 6. Out of Scope (Phase 1)

- GraphQL, MFA, calendar sync, Pomodoro, full dashboard, AI, automation, Azure IaC deployment, mobile app.

---

Confirm this MVP scope to proceed with implementation. After confirmation, implementation will follow the order in **ARCHITECTURE.md** (scaffold → auth → core → productivity → habits → finance → Docker → CI/CD → docs).
