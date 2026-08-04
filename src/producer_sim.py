"""
Simulator / Producer for Darwin Train Events.
Publishes synthetic and recorded train updates to local Kafka topic 'darwin-train-events'
or streams OSC directly to Max when Kafka is offline.
"""

from datetime import datetime, timedelta, timezone
import json
import random
import socket
import time
import os
from typing import List, Dict, Any


SAMPLE_STATIONS = [
    ("MNCRPIC", "Manchester Piccadilly"),
    ("EUSTON", "London Euston"),
    ("BHM", "Birmingham New Street"),
    ("LIVST", "Liverpool Lime Street"),
    ("GLC", "Glasgow Central"),
    ("EDINB", "Edinburgh Waverley"),
    ("CREWE", "Crewe"),
    ("CHSTR", "Chester"),
]


def generate_sample_darwin_update() -> Dict[str, Any]:
    """Generate a valid Darwin TS update payload."""
    station_code, station_name = random.choice(SAMPLE_STATIONS)
    dest_code, dest_name = random.choice(SAMPLE_STATIONS)
    while dest_code == station_code:
        dest_code, dest_name = random.choice(SAMPLE_STATIONS)

    rid = f"20260804{random.randint(100000, 999999)}"
    train_id = f"{random.randint(1, 9)}{random.choice(['A','B','C','X'])}{random.randint(10, 99)}"

    rand_val = random.random()
    if rand_val < 0.5:
        delay_min = 0
        status_can = False
    elif rand_val < 0.8:
        delay_min = random.randint(2, 25)
        status_can = False
    elif rand_val < 0.9:
        delay_min = -random.randint(1, 3)
        status_can = False
    else:
        delay_min = 0
        status_can = True

    now = datetime.now(timezone.utc)
    sched_dt = now + timedelta(minutes=random.randint(0, 10))
    sched_str = sched_dt.strftime("%H:%M")

    if delay_min != 0:
        pred_dt = sched_dt + timedelta(minutes=delay_min)
        pred_str = pred_dt.strftime("%H:%M")
    else:
        pred_str = sched_str

    loc_data = {
        "tpl": station_code,
        "wtd": f"{sched_str}:00",
        "ptd": sched_str,
        "origin": "MNCRPIC",
        "destination": dest_code,
        "plat": {"content": str(random.randint(1, 14)), "platsrc": "A"}
    }

    if status_can:
        loc_data["can"] = "true"
    else:
        loc_data["dep"] = {"et": pred_str, "src": "TD"}

    return {
        "uR": {
            "updateOrigin": "TD",
            "TS": {
                "rid": rid,
                "uid": train_id,
                "trainId": train_id,
                "Location": [loc_data]
            }
        }
    }


def is_kafka_running(host: str = "127.0.0.1", port: int = 9092) -> bool:
    """Check if Kafka broker socket is open."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False


def run_simulator(interval_seconds: float = 0.5, count: int = 20):
    """Publish simulated updates to Kafka or OSC & DB directly."""
    print(f"Starting Darwin Producer Simulator (Interval: {interval_seconds}s, Count: {count})...")
    
    use_kafka = is_kafka_running()
    producer = None

    if use_kafka:
        try:
            from confluent_kafka import Producer
            conf = {'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")}
            producer = Producer(conf)
            print("Connected to local Kafka broker.")
        except Exception as e:
            use_kafka = False
            print(f"Kafka client init failed ({e}). Running in Direct OSC / DB mode.")
    else:
        print("Kafka broker offline. Running in Direct OSC / DB mode.")

    from src.parser import flatten_darwin_update
    from src.osc_sender import OSCTransport
    from src.database import DatabaseManager

    osc = OSCTransport()
    db = DatabaseManager()
    db.connect()

    for i in range(count):
        payload = generate_sample_darwin_update()
        payload_str = json.dumps(payload)

        if use_kafka and producer:
            producer.produce("darwin-train-events", value=payload_str.encode("utf-8"))
            producer.poll(0)
        
        # Parse & send direct OSC
        records = flatten_darwin_update(payload)
        osc.send_batch(records)
        db.insert_records(records)

        rec = records[0] if records else {}
        print(
            f"[{i+1}/{count}] Event: {rec.get('station_code')} | "
            f"Status: {rec.get('status')} | Delay: {rec.get('delay_seconds')}s | "
            f"Platform: {rec.get('platform')}"
        )
        time.sleep(interval_seconds)

    if use_kafka and producer:
        producer.flush()

    db.close()
    print("Simulation run completed successfully.")


if __name__ == "__main__":
    run_simulator(interval_seconds=0.1, count=10)
