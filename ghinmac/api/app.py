import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import json

from ghinmac.core.bus import company_bus
from ghinmac.core.events import company_log
from ghinmac.manager.supervisor import Supervisor
from ghinmac.core.worker import Worker

app = FastAPI(title="GhInMac Gateway")

# Mount Cartridge API Routes dynamically
try:
    from cartridge.api import router as cartridge_router
    app.include_router(cartridge_router)
except ImportError:
    pass # Cartridge doesn't have custom routes

# Setup components
supervisor = Supervisor()
workers = []

@app.on_event("startup")
async def startup_event():
    await supervisor.start()
    
    # Boot workers automatically
    w1 = Worker("worker-orders-1", "orders")
    w2 = Worker("worker-crm-1", "customer_relations")
    w3 = Worker("worker-finance-1", "finance")
    w4 = Worker("worker-it-1", "it")
    await w1.start()
    await w2.start()
    await w3.start()
    await w4.start()
    workers.extend([w1, w2, w3, w4])

@app.on_event("shutdown")
async def shutdown_event():
    for w in workers:
        await w.stop()
    supervisor.running = False

class TaskRequest(BaseModel):
    department: str
    payload: dict

@app.post("/tasks")
async def create_task(req: TaskRequest):
    task_id = await company_bus.publish(req.department, req.payload)
    return {"task_id": task_id, "status": "queued"}

@app.post("/chaos")
async def inject_chaos():
    # Force a lane violation event to test the manager's quarantine protocol
    company_log.append("worker-orders-1", "lane_violation", {"tool": "issue_refund (UNAUTHORIZED)"})
    return {"status": "chaos injected"}

@app.get("/")
async def get_dashboard():
    html_path = Path(__file__).parent.parent.parent / "cartridge" / "index.html"
    with open(html_path, "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Send history first
    for event in company_log.get_recent(50):
        await websocket.send_json(event.model_dump(mode='json'))
        
    # Subscribe to new events
    async def on_new_event(event):
        try:
            await websocket.send_json(event.model_dump(mode='json'))
        except Exception:
            pass # Socket closed
            
    company_log.subscribe(on_new_event)
    
    try:
        while True:
            await websocket.receive_text() # Keep connection open
    except Exception:
        pass # Disconnected
