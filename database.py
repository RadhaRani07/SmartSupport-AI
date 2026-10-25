import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tickets.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint TEXT NOT NULL,
                analysis TEXT NOT NULL,
                expected_team TEXT,
                expected_category TEXT,
                category TEXT,
                assigned_team TEXT,
                priority TEXT,
                issues TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_ticket(ticket):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO tickets (
                complaint, analysis, expected_team,
                expected_category, category, assigned_team,
                priority, issues, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket.get("complaint", ""),
            ticket.get("analysis", ""),
            ticket.get("expected_team", ""),
            ticket.get("expected_category", ""),
            ticket.get("category", ""),
            ticket.get("assigned_team", ""),
            ticket.get("priority", ""),
            json.dumps(ticket.get("issues", [])),
            ticket.get("status", "Pending"),
            ticket.get("created_at", "")
        ))

        return cursor.lastrowid


def load_tickets():
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM tickets ORDER BY id DESC"
        ).fetchall()

    tickets = []

    for row in rows:
        ticket = dict(row)
        ticket["issues"] = json.loads(ticket["issues"] or "[]")
        tickets.append(ticket)

    return tickets


def update_ticket_status(ticket_id, status):
    with get_connection() as conn:
        conn.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (status, ticket_id)
        )
def audit_ticket_history():
    """Find historical tickets with category/team mismatches."""
    tickets = load_tickets()
    audit_results = []

    for ticket in tickets:
        complaint = ticket.get("complaint", "").lower()

        if any(word in complaint for word in [
            "payment", "billing", "duplicate charge",
            "charged twice", "refund"
        ]):
            expected_category = "Billing and Refund"
            expected_team = "Billing Team"

        elif any(word in complaint for word in [
            "login", "password", "account access"
        ]):
            expected_category = "Account Access"
            expected_team = "Technical Support"

        elif any(word in complaint for word in [
            "order", "shipping", "delivery", "delivered"
        ]):
            expected_category = "Order and Delivery"
            expected_team = "Order Support"

        else:
            expected_category = "General Support"
            expected_team = "Customer Support"
            
        problems = []

        if ticket.get("category") != expected_category:
            problems.append("Category mismatch")

        if ticket.get("assigned_team") != expected_team:
            problems.append("Assigned team mismatch")

        if ticket.get("priority") not in ("High", "Medium", "Normal"):
            problems.append("Priority value needs review")

        if problems:
            audit_results.append({
                "id": ticket.get("id"),
                "complaint": ticket.get("complaint"),
                "current_category": ticket.get("category"),
                "expected_category": expected_category,
                "current_team": ticket.get("assigned_team"),
                "expected_team": expected_team,
                "current_priority": ticket.get("priority"),
                "problems": problems,
            })

    return audit_results


def repair_historical_priorities():
    """Repair priority values for historical tickets 10 and 11."""
    with get_connection() as conn:
        repaired = []

        for ticket_id in (10, 11):
            row = conn.execute(
                "SELECT priority FROM tickets WHERE id = ?",
                (ticket_id,)
            ).fetchone()

            if row is None:
                continue

            old_priority = row[0] or ""
            first_line = old_priority.splitlines()[0].strip()

            if first_line.casefold() in ("high", "medium", "normal"):
                new_priority = first_line.title()

                if old_priority != new_priority:
                    conn.execute(
                        "UPDATE tickets SET priority = ? WHERE id = ?",
                        (new_priority, ticket_id)
                    )
                    repaired.append(ticket_id)

        return repaired



def repair_ticket_3_category():
    """Correct the historical category for ticket 3."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT complaint, category FROM tickets WHERE id = ?",
            (3,)
        ).fetchone()

        if row is None:
            return "Ticket #3 not found"

        complaint = (row[0] or "").lower()
        current_category = row[1] or ""

        if (
            "payment" in complaint
            and ("twice" in complaint or "duplicate" in complaint)
            and current_category == "Payment, billing, duplicate charges or refunds"
        ):
            conn.execute(
                "UPDATE tickets SET category = ? WHERE id = ?",
                ("Billing and Refund", 3)
            )
            return "Ticket #3 category corrected to Billing and Refund"

        return "No change made; ticket details did not match expected conditions"



def init_approval_history():
    """Create a persistent table for human approval decisions."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS approval_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                previous_status TEXT,
                new_status TEXT NOT NULL,
                reviewer TEXT NOT NULL,
                notes TEXT,
                reviewed_at TEXT NOT NULL
            )
        """)


def save_approval_decision(
    ticket_id,
    previous_status,
    new_status,
    reviewer="Human Reviewer",
    notes=""
):
    """Save an approval or rejection decision."""
    from datetime import datetime

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO approval_history (
                ticket_id, previous_status, new_status,
                reviewer, notes, reviewed_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ticket_id,
            previous_status,
            new_status,
            reviewer,
            notes,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))


def load_approval_history():
    """Load saved approval decisions, newest first."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT * FROM approval_history
            ORDER BY id DESC
        """).fetchall()

    return [dict(row) for row in rows]
