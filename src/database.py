"""
TimescaleDB & SQLite Persistence Module for Train Data Sonification
Supports PostgreSQL/TimescaleDB with automatic SQLite fallback for zero-dependency local runs.
"""

from datetime import datetime, timezone
import os
import sqlite3
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("DatabaseManager")

try:
    import psycopg2
    from psycopg2.extras import execute_values
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


class DatabaseManager:

    def __init__(
        self,
        dbname: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        sqlite_path: str = "train_sonification.db"
    ):
        self.dbname = dbname or os.getenv("POSTGRES_DB", "train_sonification")
        self.user = user or os.getenv("POSTGRES_USER", "postgres")
        self.password = password or os.getenv("POSTGRES_PASSWORD", "postgrespassword")
        self.host = host or os.getenv("POSTGRES_HOST", "localhost")
        self.port = port or int(os.getenv("POSTGRES_PORT", "5432"))
        self.sqlite_path = sqlite_path
        self.conn = None
        self.is_sqlite = False

    def connect(self):
        """Establish connection to PostgreSQL/TimescaleDB or fallback to SQLite."""
        if self.conn is not None:
            return

        if HAS_PSYCOPG2:
            try:
                self.conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    connect_timeout=3
                )
                self.conn.autocommit = True
                self.is_sqlite = False
                logger.info("Connected to TimescaleDB / PostgreSQL.")
                return
            except Exception as e:
                logger.warning(f"PostgreSQL connection failed ({e}). Falling back to local SQLite database.")

        # Fallback to SQLite
        self.is_sqlite = True
        self.conn = sqlite3.connect(self.sqlite_path, check_same_thread=False)
        self._init_sqlite_schema()
        logger.info(f"Connected to local SQLite database at '{self.sqlite_path}'.")

    def _init_sqlite_schema(self):
        """Initialize local SQLite schema if using fallback."""
        query = """
        CREATE TABLE IF NOT EXISTS train_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            schedule_id TEXT NOT NULL,
            train_id TEXT,
            station_code TEXT,
            origin TEXT,
            destination TEXT,
            status TEXT,
            delay_seconds INTEGER DEFAULT 0,
            platform TEXT,
            scheduled_arrival TEXT,
            scheduled_departure TEXT,
            predicted_arrival TEXT,
            predicted_departure TEXT,
            event_type TEXT
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def insert_records(self, records: List[Dict[str, Any]]):
        """Batch insert normalized train event records."""
        if not records:
            return

        self.connect()

        values = []
        for r in records:
            ts_str = r.get("timestamp") or datetime.now(timezone.utc).isoformat()
            values.append((
                ts_str,
                r.get("schedule_id", ""),
                r.get("train_id", ""),
                r.get("station_code", ""),
                r.get("origin", ""),
                r.get("destination", ""),
                r.get("status", "UNKNOWN"),
                r.get("delay_seconds", 0),
                r.get("platform", ""),
                r.get("scheduled_arrival"),
                r.get("scheduled_departure"),
                r.get("predicted_arrival"),
                r.get("predicted_departure"),
                r.get("event_type", "TS_UPDATE")
            ))

        cursor = self.conn.cursor()

        if self.is_sqlite:
            query = """
                INSERT INTO train_events (
                    time, schedule_id, train_id, station_code, origin, destination,
                    status, delay_seconds, platform, scheduled_arrival, scheduled_departure,
                    predicted_arrival, predicted_departure, event_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.executemany(query, values)
            self.conn.commit()
        else:
            query = """
                INSERT INTO train_events (
                    time, schedule_id, train_id, station_code, origin, destination,
                    status, delay_seconds, platform, scheduled_arrival, scheduled_departure,
                    predicted_arrival, predicted_departure, event_type
                ) VALUES %s
            """
            execute_values(cursor, query, values)
