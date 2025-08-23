import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DB_PATH = Path("/workspace/data/leads.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                source TEXT,
                status TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                scheduled_url TEXT,
                next_nudge_at DATETIME,
                nudges_sent INTEGER DEFAULT 0
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                direction TEXT, -- inbound/outbound
                channel TEXT, -- sms/email
                content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(lead_id) REFERENCES leads(id)
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def create_lead(name: str, email: Optional[str], phone: Optional[str], source: Optional[str]) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO leads (name, email, phone, source, status, next_nudge_at, nudges_sent) VALUES (?, ?, ?, ?, ?, DATETIME('now'), 0)",
            (name, email, phone, source, "new"),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_lead(lead_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def record_message(lead_id: int, direction: str, channel: str, content: str) -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (lead_id, direction, channel, content) VALUES (?, ?, ?, ?)",
            (lead_id, direction, channel, content),
        )
        conn.commit()
    finally:
        conn.close()


def increment_nudges(lead_id: int) -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE leads SET nudges_sent = nudges_sent + 1 WHERE id = ?", (lead_id,))
        conn.commit()
    finally:
        conn.close()


def set_next_nudge(lead_id: int, minutes_from_now: int) -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE leads SET next_nudge_at = DATETIME('now', ?) WHERE id = ?",
            (f"+{minutes_from_now} minutes", lead_id),
        )
        conn.commit()
    finally:
        conn.close()


def set_status(lead_id: int, status: str) -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE leads SET status = ? WHERE id = ?", (status, lead_id))
        conn.commit()
    finally:
        conn.close()


def set_scheduled(lead_id: int, scheduled_url: str) -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE leads SET scheduled_url = ?, status = 'scheduled' WHERE id = ?", (scheduled_url, lead_id))
        conn.commit()
    finally:
        conn.close()


def due_nudges(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM leads
            WHERE status != 'scheduled' AND next_nudge_at IS NOT NULL AND next_nudge_at <= DATETIME('now')
            ORDER BY next_nudge_at ASC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()