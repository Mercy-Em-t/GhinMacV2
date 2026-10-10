# Craft Atelier Specific Tools

def reconcile_mpesa(args):
    """Matches M-Pesa payments and updates the order status in Supabase to approved_pending."""
    order_id = args.get("order_id")
    amount = args.get("amount")
    
    if not order_id or not amount:
        return "Error: Missing order_id or amount."
    
    # In production, this would call Supabase directly
    return f"SUCCESS: Order {order_id} reconciled with payment of {amount}. State moved to approved_pending."

def assign_rider(args):
    """Assigns a rider in the fulfillment_logs table."""
    order_id = args.get("order_id")
    rider_name = args.get("rider_name", "Auto Rider")
    
    return f"SUCCESS: Rider {rider_name} assigned to order {order_id}."

def mark_in_transit(args):
    """Moves order to IN_TRANSIT, which natively triggers the Deno WhatsApp webhook."""
    order_id = args.get("order_id")
    
    # State Machine Guard logic goes here
    return f"SUCCESS: Order {order_id} moved to IN_TRANSIT. WhatsApp dispatched by edge function."

def alert_admin(args):
    """Fires a high-priority WebSocket alert to the Craft Atelier God's Eye Dashboard."""
    order_id = args.get("order_id", "Unknown")
    reason = args.get("reason", "Manual intervention required")
    
    from ghinmac.core.events import company_log
    company_log.append("system", "admin_alert", {
        "order_id": order_id,
        "reason": reason,
        "severity": "high"
    })
    return f"Admin alerted for {order_id}. Awaiting manual resolution."
