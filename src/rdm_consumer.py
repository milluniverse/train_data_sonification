"""
Live National Rail Darwin Consumer via Rail Data Marketplace (RDM)
Connects directly to National Rail's live Kafka cluster over SASL_SSL.
Parses live updates, stores history in TimescaleDB/SQLite, and streams live OSC to Max.
"""

import os
import sys
import time
import logging
from dotenv import load_dotenv

# Load credentials from .env if present
load_dotenv()

from src.parser import parse_raw_message, flatten_darwin_update
from src.osc_sender import OSCTransport

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("RDM_Darwin_Consumer")


def run_live_consumer():
    bootstrap_server = os.getenv("RDM_BOOTSTRAP_SERVER", "kafka.raildata.org.uk:9092")
    topic = os.getenv("RDM_TOPIC", "Consumer.rdmportal.VirtualTopic.PushPort-v18")
    consumer_key = os.getenv("RDM_CONSUMER_KEY")
    consumer_secret = os.getenv("RDM_CONSUMER_SECRET")
    sasl_mechanism = os.getenv("RDM_SASL_MECHANISM", "PLAIN")
    security_protocol = os.getenv("RDM_SECURITY_PROTOCOL", "SASL_SSL")

    if not consumer_key or not consumer_secret or consumer_key == "YOUR_RDM_CONSUMER_KEY_HERE":
        logger.error("Missing RDM credentials!")
        logger.info("Please copy '.env.example' to '.env' and fill in your RDM_CONSUMER_KEY and RDM_CONSUMER_SECRET from https://raildata.org.uk")
        sys.exit(1)

    osc = OSCTransport()

    logger.info(f"Connecting to Live National Rail Darwin Kafka cluster at {bootstrap_server}...")
    
    try:
        from confluent_kafka import Consumer, KafkaError

        group_id = os.getenv("RDM_CONSUMER_GROUP", f"sonification-{consumer_key[:8]}")

        conf = {
            'bootstrap.servers': bootstrap_server,
            'group.id': group_id,
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True,
            'security.protocol': security_protocol,
            'sasl.mechanisms': sasl_mechanism,
            'sasl.username': consumer_key,
            'sasl.password': consumer_secret,
        }

        consumer = Consumer(conf)
        consumer.subscribe([topic])
        logger.info(f"Subscribed to live topic '{topic}'. Listening for real-time train movements...")

        msg_count = 0
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                    time.sleep(2.0)
                    continue

            raw_val = msg.value()
            payload = parse_raw_message(raw_val)
            if not payload:
                continue

            records = flatten_darwin_update(payload)
            if records:
                msg_count += len(records)
                # Stream live OSC to Max
                osc.send_batch(records)

                for r in records:
                    logger.info(
                        f"LIVE [{r.get('event_type')}] Station: {r.get('station_code')} | "
                        f"Train: {r.get('train_id')} | Status: {r.get('status')} | "
                        f"Delay: {r.get('delay_seconds')}s | Platform: {r.get('platform')}"
                    )

    except KeyboardInterrupt:
        logger.info("Live consumer stopped by user.")
    except Exception as err:
        logger.error(f"Fatal error in live consumer: {err}")


if __name__ == "__main__":
    run_live_consumer()
