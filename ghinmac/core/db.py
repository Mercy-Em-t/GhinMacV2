import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "cartridge" / "company.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_db():
    conn = get_db()
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        name TEXT,
        status TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        item TEXT,
        status TEXT,
        amount REAL
    )''')

    # Seed dummy data if empty
    c.execute("SELECT count(*) FROM customers")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO customers VALUES (?, ?, ?)", [
            ("CUST-1", "Alice", "active"),
            ("CUST-2", "Bob", "active")
        ])
        c.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", [
            ("ORD-1", "CUST-1", "Laptop", "pending", 1200.00),
            ("ORD-2", "CUST-2", "Mouse", "shipped", 25.00)
        ])
        conn.commit()
    
    conn.close()

# Run setup on import
setup_db()
