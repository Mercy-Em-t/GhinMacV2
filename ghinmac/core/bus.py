import asyncio
import uuid
from typing import Dict, Any
from .events import company_log

class TaskMessage:
    def __init__(self, task_id: str, department: str, payload: Dict[str, Any]):
        self.task_id = task_id
        self.department = department
        self.payload = payload
        self.status = "pending"

class MessageBus:
    def __init__(self):
        # Queues per department
        self.queues: Dict[str, asyncio.Queue] = {}

    def get_queue(self, department: str) -> asyncio.Queue:
        if department not in self.queues:
            self.queues[department] = asyncio.Queue()
        return self.queues[department]

    async def publish(self, department: str, payload: Dict[str, Any]) -> str:
        task_id = str(uuid.uuid4())
        msg = TaskMessage(task_id, department, payload)
        
        company_log.append("system", "task_created", {"task_id": task_id, "department": department, "payload": payload})
        
        queue = self.get_queue(department)
        await queue.put(msg)
        return task_id

# Global bus
company_bus = MessageBus()
