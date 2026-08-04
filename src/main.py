"""
Main Live Ingestion Engine - Phase 2 Pipeline
Consumes Kafka events, parses payloads, persists to TimescaleDB, and streams OSC to Max.
"""

import os
import sys
import time
import json
import logging
from typing import Optional

from src.parser import parse_raw_message, flatten_darwin_update
from src.database import DatabaseManager
from src.osc_sender import OSCTransport

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("TrainSonification")


def run_pipeline(
    kafka_bootstrap: Optional[str] = None,
    topic: str = "darwin-train-events",
    group_id: str = "sonification-consumer-group",
):
    kafka_bootstrap = kafka_bootstrap or os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")

    db = DatabaseManager()
    osc = OSCTransport()

    logger.info("Initializing TimescaleDB connection...")
    try:
        db.connect()
        logger.info("TimescaleDB connected successfully.")
    except Exception as e:
        logger.warning(f"TimescaleDB connection deferred/failed: {e}")

    logger.info(f"Connecting to Kafka broker at {kafka_bootstrap} (Topic: {topic})...")

    try:
        from confluent_kafka import Consumer, KafkaError
        conf = {
            'bootstrap.servers': kafka_bootstrap,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True
        }
        consumer = Consumer(conf)
        consumer.subscribe([topic])
        logger.info(f"Subscribed to topic '{topic}'. Listening for events...")

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                    break

            raw_val = msg.value()
            payload = parse_raw_message(raw_val)
            if not payload:
                continue

            records = flatten_darwin_update(payload)
            if records:
                # 1. Stream to Max via OSC
                osc.send_batch(records)

                # 2. Persist to TimescaleDB
                try:
                    db.insert_records(records)
                except Exception as db_err:
                    logger.warning(f"Database insertion failed: {db_err}")

                for r in records:
                    logger.info(
                        f"Event: [{r.get('event_type')}] Station: {r.get('station_code')} | "
                        f"Status: {r.get('status')} | Delay: {r.get('delay_seconds')}s"
                    )

    except KeyboardInterrupt:
        logger.info("Pipeline stopped by user.")
    except Exception as err:
        logger.error(f"Fatal error in pipeline: {err}")
    finally:
        db.close()


if __name__ == "__main__":
    run_pipeline()
