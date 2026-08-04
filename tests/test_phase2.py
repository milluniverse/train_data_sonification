"""
Unit tests for Phase 2: Local Event Engine, Database Persistence, and OSC Transport.
"""

import sys
import os
import unittest
import socket

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import DatabaseManager
from src.osc_sender import OSCTransport


class TestPhase2Engine(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_train_sonification.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.db = DatabaseManager(sqlite_path=self.db_path)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_database_sqlite_insertion(self):
        self.db.connect()
        records = [
            {
                "event_type": "TS_UPDATE",
                "schedule_id": "20260804001",
                "train_id": "1A99",
                "station_code": "MNCRPIC",
                "origin": "MNCRPIC",
                "destination": "EUSTON",
                "status": "LATE",
                "delay_seconds": 300,
                "platform": "11",
                "scheduled_arrival": "12:00",
                "scheduled_departure": "12:00",
                "predicted_arrival": "12:05",
                "predicted_departure": "12:05",
                "timestamp": "2026-08-04T19:00:00+00:00"
            }
        ]

        self.db.insert_records(records)

        cursor = self.db.conn.cursor()
        cursor.execute("SELECT station_code, status, delay_seconds FROM train_events WHERE schedule_id='20260804001'")
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "MNCRPIC")
        self.assertEqual(row[1], "LATE")
        self.assertEqual(row[2], 300)

    def test_osc_transport_packet(self):
        # Create a UDP socket receiver to test OSC transport
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_sock.bind(("127.0.0.1", 7401))
        recv_sock.settimeout(2.0)

        osc = OSCTransport(host="127.0.0.1", port=7401)
        record = {
            "schedule_id": "RID123",
            "train_id": "1B20",
            "station_code": "CREWE",
            "status": "ON TIME",
            "delay_seconds": 0,
            "platform": "3"
        }

        osc.send_event(record)

        data, addr = recv_sock.recvfrom(1024)
        self.assertTrue(len(data) > 0)
        self.assertIn(b"/train/event", data)
        recv_sock.close()


if __name__ == "__main__":
    unittest.main()
