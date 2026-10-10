# API Reference

The GhInMac API Gateway is built on FastAPI, serving both REST endpoints for incoming webhooks and WebSocket endpoints for the real-time God's Eye Dashboard.

## REST Endpoints

### `POST /tasks`
Submits a new task to the Redis Event Bus.
- **Request Body**: 
  ```json
  {
    "department": "finance",
    "payload": { ... }
  }
  ```
- **Response**: `{"task_id": "<uuid>", "status": "queued"}`

### `POST /chaos`
Injects a simulated "Lane Violation" event. Used primarily for testing the Supervisor manager's quarantine protocol.
- **Response**: `{"status": "chaos injected"}`

### `GET /`
Serves the Vue 3 God's Eye Dashboard HTML file (`index.html`) located in the loaded cartridge folder.

## WebSockets

### `WS /ws/events`
Real-time event stream for the God's Eye Dashboard.
- **Connection**: On connection, the server immediately pushes the last 50 historical events from the `company_log`.
- **Live Stream**: The socket subscribes to new events and streams JSON payloads live to the frontend. Used to visualize glowing particle flows and trigger real-time `alert_admin` alarms.
