import asyncio
import random
from ghinmac.core.bus import company_bus
from ghinmac.core.worker import Worker
from ghinmac.manager.supervisor import Supervisor

async def run_simulation():
    print("Starting GhInMac Simulator...")
    
    # 1. Start Supervisor
    supervisor = Supervisor()
    await supervisor.start()
    
    # 2. Start Workers
    w1 = Worker("worker-orders-1", "orders")
    w2 = Worker("worker-crm-1", "customer_relations")
    await w1.start()
    await w2.start()
    
    # 3. Inject some tasks
    await company_bus.publish("orders", {"order_id": "ORD-1234", "item": "Laptop", "action": "process"})
    await asyncio.sleep(2)
    await company_bus.publish("customer_relations", {"customer": "Alice", "query": "Where is my order?"})
    
    # Let it run a bit
    await asyncio.sleep(10)
    
    # 4. Inject Chaos (Simulate a rogue worker)
    # We'll artificially make a worker send a budget breach event
    from ghinmac.core.events import company_log
    company_log.append("worker-orders-1", "lane_violation", {"tool": "issue_refund"})
    
    await asyncio.sleep(5)
    
    # Clean up
    await w1.stop()
    await w2.stop()
    supervisor.running = False

if __name__ == "__main__":
    asyncio.run(run_simulation())
