# The Cartridge Pattern

The GhInMac Engine is domain-agnostic. It becomes a specialized operating system through **The Cartridge Pattern**, which isolates 100% of the business logic within the `cartridge/` directory.

## Isolation of Business Logic

By placing business-specific details in this isolated folder, the engine can safely swap between an E-Commerce system (e.g., Craft Atelier) and a Healthcare clinic without changing the core engine code.

### 1. `company.yaml`
This declarative configuration file defines the organizational structure and constraints:
- **Departments**: Maps out AI departments (e.g., Finance, Dispatch, Support).
- **Tool Access**: Explicitly lists the `allowed_tools` each department can use (e.g., Finance can use `reconcile_mpesa`).
- **Budgets & Guardrails**: Defines timeout thresholds, error limits, and token budgets per task.

### 2. `repository.py`
To prevent the AI from writing raw SQL and hallucinating database structures, all database interactions must pass through the **Data Access Object (DAO) Repository**.
- It strictly defines the available CRUD operations.
- Enforces State Machine rules (e.g., ensuring an order can only move from `PENDING` to `APPROVED`).

### 3. `tools.py`
This file implements the execution logic of the AI's capabilities.
- Examples include `reconcile_mpesa()`, `assign_rider()`, and `alert_admin()`.
- The tools interface with `repository.py` for database persistence.
- Any unauthorized tool call by a worker (e.g., calling a tool not in their department's `allowed_tools`) immediately triggers a "Lane Violation" quarantined by the Supervisor.
