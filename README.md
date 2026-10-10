# 🧠 GhInMac Autonomous OS

**GhInMac** is a highly scalable, event-driven Multi-Agent Operating System. It is designed to autonomously run corporate and e-commerce workloads by delegating tasks to a swarm of AI workers, safely constrained by strict Domain-Driven Design (DDD) boundaries.

## 🌟 Core Architecture

GhInMac is not just a chatbot; it is a full-scale corporate engine:

*   **🔌 The Cartridge Pattern:** The business logic (Database Schema, AI Tools, Prompts, Models) is 100% isolated inside the `cartridge/` directory. You can swap the system from an E-Commerce Platform to a Healthcare Clinic by simply swapping the cartridge folder.
*   **🛡️ Strict DBMS Control:** The AI does not write raw SQL. It interacts exclusively with a strict Data Access Object (DAO) Repository, preventing hallucinations, enforcing State Machine rules, and protecting database integrity.
*   **🚌 Redis Event Bus:** Tasks are routed via Redis Streams, ensuring zero data loss. If a worker container crashes mid-thought, the unacknowledged task is safely re-routed to the next available worker.
*   **👁️ The God's Eye Dashboard:** A real-time Vue 3 + Tailwind frontend connected via WebSockets. Watch tasks physically move between AI departments as glowing particles, and monitor the live database state in real-time.
*   **🚨 Human-in-the-Loop Escalation:** Workers autonomously handle the "happy path" (e.g. M-Pesa reconciliation). If an unresolvable edge case occurs, the AI calls the `alert_admin` tool, triggering visual and audio alarms on the dashboard to summon a human manager.
*   **👮 Independent Supervisor:** An isolated Supervisor container watches the Redis Event Log. If an AI attempts to use an unauthorized tool (Lane Violation), the Supervisor instantly quarantines the task and kills the worker.

## 🚀 Quick Start

1.  **Clone the Repo & Set API Keys:**
    ```bash
    git clone https://github.com/Mercy-Em-t/GhInMac.git
    cd GhInMac
    # Set your LLM provider keys (e.g. GEMINI_API_KEY)
    ```

2.  **Define your Business (The Cartridge):**
    Modify `cartridge/company.yaml` to define your departments, models, and allowed tools. Write your Python tools in `cartridge/tools.py`.

3.  **Spin up the Swarm:**
    ```bash
    docker-compose up --build -d
    ```

4.  **Enter the Cockpit:**
    Open `http://localhost:8080` to access the God's Eye Dashboard. Send a task via the UI or a REST `POST /tasks` webhook to watch the AI go to work.

## ☁️ Cloud Ready
The `k8s/` directory contains production-ready Kubernetes manifests (Deployments, HPA, Services) to instantly deploy GhInMac to GKE or EKS for infinite horizontal scaling.
