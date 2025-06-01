import sqlite3
import uuid
from datetime import datetime

class Database:
    def __init__(self, db_name="orders.db"):
        self.db_name = db_name
        self.create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    total_amount REAL,
                    status TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id TEXT PRIMARY KEY,
                    order_id TEXT,
                    product_name TEXT,
                    quantity INTEGER,
                    price REAL,
                    FOREIGN KEY (order_id) REFERENCES orders (id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS status_updates (
                    order_id TEXT,
                    status TEXT,
                    timestamp INTEGER,
                    FOREIGN KEY (order_id) REFERENCES orders (id)
                )
            """)

    def create_order(self, items, total_amount):
        order_id = str(uuid.uuid4())
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO orders (id, total_amount, status) VALUES (?, ?, ?)",
                (order_id, total_amount, "PENDING")
            )
            for item in items:
                item_id = str(uuid.uuid4())
                conn.execute(
                    "INSERT INTO order_items (id, order_id, product_name, quantity, price) VALUES (?, ?, ?, ?, ?)",
                    (item_id, order_id, item.product_name, item.quantity, item.price)
                )
            conn.commit()
        return order_id

    def get_order(self, order_id):
        with self._connect() as conn:
            order = conn.execute(
                "SELECT id, total_amount, status FROM orders WHERE id = ?", (order_id,)
            ).fetchone()
            if not order:
                return None
            items = conn.execute(
                "SELECT id, product_name, quantity, price FROM order_items WHERE order_id = ?", (order_id,)
            ).fetchall()
        return order, items

    def update_order_status(self, order_id, status):
        with self._connect() as conn:
            conn.execute(
                "UPDATE orders SET status = ? WHERE id = ?", (status, order_id)
            )
            timestamp = int(datetime.now().timestamp())
            conn.execute(
                "INSERT INTO status_updates (order_id, status, timestamp) VALUES (?, ?, ?)",
                (order_id, status, timestamp)
            )
            conn.commit()
            order = conn.execute(
                "SELECT id, total_amount, status FROM orders WHERE id = ?", (order_id,)
            ).fetchone()
            if not order:
                return None
            items = conn.execute(
                "SELECT id, product_name, quantity, price FROM order_items WHERE order_id = ?", (order_id,)
            ).fetchall()
        return order, items

    def cancel_order(self, order_id):
        return self.update_order_status(order_id, "CANCELLED")

    def list_orders(self):
        with self._connect() as conn:
            orders = conn.execute(
                "SELECT id, total_amount, status FROM orders"
            ).fetchall()
            result = []
            for order in orders:
                order_id = order[0]
                items = conn.execute(
                    "SELECT id, product_name, quantity, price FROM order_items WHERE order_id = ?", (order_id,)
                ).fetchall()
                result.append((order, items))
        return result

    def get_status_updates(self):
        with self._connect() as conn:
            return conn.execute(
                "SELECT order_id, status, timestamp FROM status_updates ORDER BY timestamp"
            ).fetchall()