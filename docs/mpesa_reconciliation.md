# M-Pesa Reconciliation Workflow

The M-Pesa reconciliation process allows the AI (specifically the Finance department worker) to autonomously match incoming payments to orders.

## Workflow 
1. **Safaricom Webhook**: Safaricom posts payment details via webhook to the GhInMac API.
2. **Task Queuing**: The API enqueues a reconciliation task onto the Redis Event Bus directed at the `finance` department.
3. **AI Execution**: A finance worker picks up the task and uses the `reconcile_mpesa` tool. 
4. **Matching & Database Update**: The `reconcile_mpesa` tool takes the `order_id` and `amount`. It queries Supabase via the Repository to match the exact amounts. Upon success, it updates the order status in Supabase to `approved_pending`.
5. **Human Escalation (Edge Cases)**: If the payment does not match (e.g., partial payment, unknown order ID), the AI calls the `alert_admin` tool. This fires a high-priority WebSocket alert to the God's Eye Dashboard, prompting human intervention.
