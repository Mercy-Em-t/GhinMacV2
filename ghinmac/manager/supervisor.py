import asyncio
from datetime import datetime, timedelta
from typing import Dict
from ghinmac.core.events import company_log, Event
from ghinmac.core.config import company_config

class WorkerState:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.last_heartbeat = datetime.utcnow()
        self.status = "healthy"
        self.risk_score = 0
        self.department = None

class Supervisor:
    def __init__(self):
        self.workers: Dict[str, WorkerState] = {}
        self.running = False
        company_log.subscribe(self.on_event)

    async def start(self):
        self.running = True
        company_log.append("manager", "supervisor_started", {})
        asyncio.create_task(self._monitor_loop())

    async def on_event(self, event: Event):
        # We only care about events from workers
        if not event.source.startswith("worker-"):
            return
            
        worker_id = event.source
        if worker_id not in self.workers:
            self.workers[worker_id] = WorkerState(worker_id)
            
        state = self.workers[worker_id]
        
        if event.type == "worker_started":
            state.department = event.payload.get("department")
            state.status = "healthy"
            
        elif event.type == "heartbeat":
            state.last_heartbeat = datetime.utcnow()
            
        elif event.type == "lane_violation" or event.type == "budget_breach":
            await self.quarantine_worker(worker_id, event.type)

    async def quarantine_worker(self, worker_id: str, reason: str):
        if self.workers[worker_id].status == "quarantined":
            return
            
        self.workers[worker_id].status = "quarantined"
        company_log.append("manager", "quarantine_action", {"worker_id": worker_id, "reason": reason})
        # In a real system, we would kill the worker process/task here.
        # Since they run in the same asyncio loop for Phase 1, we simulate it by logging.

    async def _monitor_loop(self):
        while self.running:
            now = datetime.utcnow()
            for worker_id, state in self.workers.items():
                if state.status == "quarantined":
                    continue
                    
                # Check soft signals (unresponsive)
                elapsed = (now - state.last_heartbeat).total_seconds()
                if elapsed > company_config["manager"]["timeout_seconds"]:
                    company_log.append("manager", "worker_unresponsive", {"worker_id": worker_id, "elapsed": elapsed})
                    await self.quarantine_worker(worker_id, "unresponsive")
                    
            await asyncio.sleep(5)
