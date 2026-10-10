import asyncio
from typing import Dict, Any
from .events import company_log
from .bus import company_bus, TaskMessage
from .config import company_config
from ghinmac.llm.mock import MockProvider
from ghinmac.llm.gemini import GeminiProvider

class Worker:
    def __init__(self, worker_id: str, department_name: str):
        self.worker_id = worker_id
        self.department_name = department_name
        
        dept_config = company_config["departments"].get(department_name, {})
        self.allowed_tools = dept_config.get("allowed_tools", [])
        self.max_budget = dept_config.get("max_budget_per_task", 100)
        
        provider_name = company_config.get("llm_provider", "mock")
        if provider_name == "gemini":
            self.llm = GeminiProvider()
        else:
            self.llm = MockProvider()
            
        self.running = False
        self._task = None
        self._heartbeat_task = None
        
    async def start(self):
        self.running = True
        company_log.append(self.worker_id, "worker_started", {"department": self.department_name})
        self._task = asyncio.create_task(self._run_loop())
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
    async def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        company_log.append(self.worker_id, "worker_stopped", {})

    async def _heartbeat_loop(self):
        while self.running:
            company_log.append(self.worker_id, "heartbeat", {})
            await asyncio.sleep(5)

    async def _run_loop(self):
        queue = company_bus.get_queue(self.department_name)
        while self.running:
            try:
                task_msg: TaskMessage = await queue.get()
                await self.process_task(task_msg)
                queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                company_log.append(self.worker_id, "worker_error", {"error": str(e)})
                await asyncio.sleep(1)

    async def process_task(self, task_msg: TaskMessage):
        company_log.append(self.worker_id, "task_started", {"task_id": task_msg.task_id})
        budget_used = 0
        prompt = f"Task: {task_msg.payload}\nYou are in {self.department_name}."
        
        while budget_used < self.max_budget:
            budget_used += 10 # simulated cost
            
            response = await self.llm.generate(prompt, self.allowed_tools)
            
            if response.get("action") == "tool_call":
                tool = response.get("tool")
                company_log.append(self.worker_id, "tool_call", {"task_id": task_msg.task_id, "tool": tool, "args": response.get("args")})
                
                # Check hard limits before executing (Supervisor will also catch this but worker should refuse)
                if tool not in self.allowed_tools:
                    company_log.append(self.worker_id, "lane_violation", {"task_id": task_msg.task_id, "tool": tool})
                    break # Stop processing this task
                
                # Tool execution
                tool_output = "Success"
                try:
                    import cartridge.tools
                    if hasattr(cartridge.tools, tool):
                        tool_func = getattr(cartridge.tools, tool)
                        tool_output = tool_func(response.get("args", {}))
                    else:
                        tool_output = f"Error: Tool {tool} not found in cartridge."
                except Exception as e:
                    tool_output = f"Error executing tool {tool}: {e}"

                prompt += f"\nTool {tool} output: {tool_output}"
                
            elif response.get("action") == "reply":
                company_log.append(self.worker_id, "task_completed", {"task_id": task_msg.task_id, "result": response.get("content")})
                break
            
            await asyncio.sleep(1) # simulate think time
            
        if budget_used >= self.max_budget:
            company_log.append(self.worker_id, "budget_breach", {"task_id": task_msg.task_id})
