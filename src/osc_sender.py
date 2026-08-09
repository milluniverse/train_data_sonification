"""
OSC Transport Layer for Train Data Sonification
Streams normalized event packets over UDP socket to Max (127.0.0.1:7400)
"""

import os
from pythonosc import udp_client
from typing import Any, Dict, List, Optional


STATUS_CODE_MAP = {
    "ON TIME": 0,
    "EARLY": 1,
    "LATE": 2,
    "CANCELLED": 3,
    "ACTIVATED": 4,
    "NO REPORT": 5,
}


class OSCTransport:

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None):
        self.host = host or os.getenv("OSC_HOST", "127.0.0.1")
        self.port = port or int(os.getenv("OSC_PORT", "7400"))
        self.client = udp_client.SimpleUDPClient(self.host, self.port)

    def send_event(self, record: Dict[str, Any]):
        """
        Send a normalized event record as OSC packets.
        
        OSC Paths sent:
        1. /train/event -> [schedule_id, train_id, station_code, status, delay_seconds, platform]
        2. /train/delay -> [delay_seconds]
        3. /train/trigger -> [station_code, status_int, delay_seconds]
        """
        if not record:
            return

        station_code = (record.get("station_code", ""))
        train_id = str(record.get("train_id", ""))
        status = str(record.get("status", "NO REPORT"))
        status_int = STATUS_CODE_MAP.get(status, 5)
        delay_sec = int(record.get("delay_seconds", 0))
        platform = str(record.get("platform", ""))
        schedule_id = str(record.get("schedule_id", ""))

        # Main Event packet
        self.client.send_message(
            "/train/event",
            [station_code, train_id, status, status_int, delay_sec, platform, schedule_id,]
        )

        # Macro Delay packet
        self.client.send_message("/train/delay", [delay_sec])

        # Discrete Trigger packet
        self.client.send_message(
            "/train/trigger",
            [station_code, status_int, delay_sec]
        )

    def send_batch(self, records: List[Dict[str, Any]]):
        """Send a list of records sequentially."""
        for r in records:
            self.send_event(r)
