# System Architecture

GhInMac Autonomous OS utilizes a Split Deployment model, taking advantage of edge computing and dedicated backend resources for optimal performance, scalability, and security.

## Split Deployment

### 1. Vercel Frontend (God's Eye Dashboard)
The "God's Eye Dashboard" is built with Vue 3 and Tailwind CSS. It is deployed on Vercel to leverage their Global Edge Network. 
- **Features**: Real-time visualization of task pipelines, glowing particles representing data flows between AI departments, and administrative intervention alerts.
- **Connection**: It connects to the Fly.io backend via WebSockets (`/ws/events`) for low-latency live updates of the database state and worker actions.

### 2. Fly.io Backend (GhInMac Engine)
The core GhInMac Engine runs on Fly.io, positioned close to the database for minimal latency.
- **Components**:
  - **FastAPI Gateway**: Receives REST webhooks and serves the WebSocket connections to the Vercel frontend.
  - **AI Workers**: Isolated worker nodes (e.g., Orders, CRM, Finance, IT) that process tasks asynchronously from the Redis Event Bus.
  - **Supervisor**: Monitors worker execution and enforces Domain-Driven Design (DDD) rules to prevent lane violations.
- **State Management**: Task queuing and event routing rely on Redis Streams, ensuring zero data loss and absolute fault-tolerance across container restarts. Data persistence is handled via Supabase.
