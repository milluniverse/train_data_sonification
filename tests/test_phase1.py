"""
Unit tests for Phase 1: Ingestion, Schema Mapping, and Normalization.
"""

import sys
import os
import unittest

# Ensure src is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser import (
    parse_raw_message,
    calculate_delay_seconds,
    flatten_darwin_update,
    time_to_seconds,
)


class TestPhase1Parser(unittest.TestCase):

    def test_time_to_seconds(self):
        self.assertEqual(time_to_seconds("00:00"), 0)
        self.assertEqual(time_to_seconds("01:00:00"), 3600)
        self.assertEqual(time_to_seconds("12:30:15"), 12 * 3600 + 30 * 60 + 15)
        self.assertIsNone(time_to_seconds(None))
        self.assertIsNone(time_to_seconds("invalid"))

    def test_calculate_delay_seconds(self):
        # On time
        self.assertEqual(calculate_delay_seconds("12:00", "12:00"), 0)
        # 5 minutes late (+300s)
        self.assertEqual(calculate_delay_seconds("12:00", "12:05"), 300)
        # 2 minutes early (-120s)
        self.assertEqual(calculate_delay_seconds("12:00", "11:58"), -120)
        # Midnight boundary crossing (scheduled 23:58, actual 00:03 -> 5 mins late = +300s)
        self.assertEqual(calculate_delay_seconds("23:58", "00:03"), 300)

    def test_flatten_ts_update(self):
        sample_json_payload = {
            "uR": {
                "updateOrigin": "CIS",
                "requestSource": "CIS1",
                "TS": {
                    "rid": "202406107149951",
                    "uid": "G49951",
                    "Location": [
                        {
                            "tpl": "MNCRPIC",
                            "wtd": "12:01:00",
                            "ptd": "12:00",
                            "dep": {"at": "12:05", "src": "TD"},
                            "plat": {"content": "11", "platsrc": "A"},
                        },
                        {
                            "tpl": "CREWE",
                            "wta": "12:30:00",
                            "pta": "12:30",
                            "wtd": "12:31:30",
                            "ptd": "12:31",
                            "arr": {"et": "12:30", "src": "Darwin"},
                            "plat": {"content": "4", "platsrc": "M"},
                        },
                        {
                            "tpl": "CHSTR",
                            "wta": "13:00:00",
                            "pta": "13:00",
                            "can": "true",
                        }
                    ],
                },
            }
        }

        records = flatten_darwin_update(sample_json_payload)
        self.assertEqual(len(records), 3)

        # Record 1: MNCRPIC (5 mins late)
        rec1 = records[0]
        self.assertEqual(rec1["schedule_id"], "202406107149951")
        self.assertEqual(rec1["train_id"], "G49951")
        self.assertEqual(rec1["station_code"], "MNCRPIC")
        self.assertEqual(rec1["scheduled_departure"], "12:00")
        self.assertEqual(rec1["predicted_departure"], "12:05")
        self.assertEqual(rec1["platform"], "11")
        self.assertEqual(rec1["status"], "LATE")
        self.assertEqual(rec1["delay_seconds"], 300)

        # Record 2: CREWE (On time)
        rec2 = records[1]
        self.assertEqual(rec2["station_code"], "CREWE")
        self.assertEqual(rec2["scheduled_arrival"], "12:30")
        self.assertEqual(rec2["predicted_arrival"], "12:30")
        self.assertEqual(rec2["platform"], "4")
        self.assertEqual(rec2["status"], "ON TIME")
        self.assertEqual(rec2["delay_seconds"], 0)

        # Record 3: CHSTR (Cancelled)
        rec3 = records[2]
        self.assertEqual(rec3["station_code"], "CHSTR")
        self.assertEqual(rec3["status"], "CANCELLED")

    def test_flatten_schedule_activation(self):
        sample_schedule = {
            "uR": {
                "schedule": {
                    "rid": "202406107149951",
                    "uid": "C09014",
                    "trainId": "9X99",
                    "toc": "NW",
                    "OR": {"tpl": "MNCRPIC", "ptd": "12:00"},
                    "DT": {"tpl": "CHSTR", "pta": "13:00"},
                }
            }
        }

        records = flatten_darwin_update(sample_schedule)
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertEqual(rec["event_type"], "SCHEDULE_ACTIVATION")
        self.assertEqual(rec["schedule_id"], "202406107149951")
        self.assertEqual(rec["train_id"], "9X99")
        self.assertEqual(rec["origin"], "MNCRPIC")
        self.assertEqual(rec["destination"], "CHSTR")
        self.assertEqual(rec["status"], "ACTIVATED")


if __name__ == "__main__":
    unittest.main()
