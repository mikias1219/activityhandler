# LifeOS — Database Schema

## Phase 1 (MVP) Entity Relationship Diagram

```mermaid
erDiagram
    users ||--o{ task : "owns"
    users ||--o{ habit : "owns"
    users ||--o{ habit_check_in : "logs"
    users ||--o{ expense_category : "owns"
    users ||--o{ expense : "owns"
    users ||--o{ budget : "owns"
    users ||--o{ audit_log : "generates"

    habit ||--o{ habit_check_in : "has"

    expense_category ||--o{ expense : "categorizes"

    users {
        uuid id PK
        string email UK
        string password_hash
        string first_name
        string last_name
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    audit_log {
        uuid id PK
        uuid user_id FK
        string action
        string resource_type
        string resource_id
        string request_path
        string method
        datetime created_at
    }

    task {
        uuid id PK
        uuid user_id FK
        string title
        text notes
        date due_date
        string priority
        string status
        datetime created_at
        datetime updated_at
    }

    habit {
        uuid id PK
        uuid user_id FK
        string name
        string target_frequency
        int target_count
        datetime created_at
        datetime updated_at
    }

    habit_check_in {
        uuid id PK
        uuid habit_id FK
        uuid user_id FK
        date check_date
        boolean completed
        text notes
        datetime created_at
    }

    expense_category {
        uuid id PK
        uuid user_id FK
        string name
        string icon
        datetime created_at
    }

    expense {
        uuid id PK
        uuid user_id FK
        uuid category_id FK
        decimal amount
        string currency
        date expense_date
        text note
        datetime created_at
    }

    budget {
        uuid id PK
        uuid user_id FK
        uuid category_id FK "nullable"
        date month
        decimal amount
        string currency
        datetime created_at
    }
```

## Priority & Status Enums (Phase 1)

- **Task priority (Eisenhower)**: `urgent_important`, `urgent_not_important`, `not_urgent_important`, `not_urgent_not_important`
- **Task status**: `todo`, `in_progress`, `done`, `cancelled`
- **Habit target_frequency**: `daily`, `weekly`, `custom`

## Indexes (Recommendations)

- `task(user_id, due_date, status)` for today/planner queries
- `habit_check_in(habit_id, check_date)` unique per user
- `expense(user_id, expense_date)`, `expense(category_id, expense_date)`
- `audit_log(user_id, created_at)`
