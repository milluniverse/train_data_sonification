# National Rail Darwin Train Data Sonification Engine

A real-time data ingestion, transformation, and musical sonification pipeline that consumes National Rail Darwin Pub/Sub updates via Kafka from the Rail Data Marketplace (RDM), normalizes train delays and status changes, persists historical events to TimescaleDB (with local SQLite fallback), and streams Open Sound Control (OSC) packets over UDP to Cycling '74 Max for real-time audio synthesis.

Developed for **Creative Coding for Sound — Assignment 2 (Option 1: Musical Sonification)**.

---

## 🏗️ System Architecture

```text
               ┌─────────────────────────────────────────────────┐
               │ National Rail Darwin Pub/Sub (Confluent Cloud)  │
               └────────────────────────┬────────────────────────┘
                                        │ SASL_SSL JSON Stream
                                        ▼
               ┌─────────────────────────────────────────────────┐
               │    Live Consumer Pipeline (src/rdm_consumer.py) │
               │   • Decodes raw RDM JSON updates                │
               │   • Normalizes delays, statuses, platforms      │
               └───────────┬─────────────────────────┬───────────┘
                           │                         │
             Persists to   │                         │ Streams OSC (UDP)
          Timescale/SQLite │                         │ 127.0.0.1:7400
                           ▼                         ▼
            ┌─────────────────────┐   ┌─────────────────────────────┐
            │ Time-Series DB      │   │ Cycling '74 Max Patch       │
            │ (train_events table)│   │ (train_data_sonification)   │
            └─────────────────────┘   └─────────────────────────────┘
```

---

## ⚡ Quickstart Guide: Running the Live Darwin Stream from Terminal

### 1. Prerequisites
* **Python 3.9+**
* **Cycling '74 Max 8 or Max 9**
* **Rail Data Marketplace (RDM) Account** (Free subscription at [raildata.org.uk](https://raildata.org.uk))

---

### 2. Installation

1. Open your Mac Terminal and navigate to the project root:
   ```bash
   cd "/Users/etc.../TRAIN_DATA_SONIFICATION
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### 3. Configure RDM Credentials

1. Copy the environment template file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` using your preferred text editor (e.g. `nano .env` or `nvim .env`) and populate your RDM credentials:
   ```env
   RDM_BOOTSTRAP_SERVER=pkc-z3p1v0.europe-west2.gcp.confluent.cloud:9092
   RDM_TOPIC=prod-1010-Darwin-Train-Information-Push-Port-IIII2_0-JSON
   RDM_CONSUMER_KEY=YOUR_RDM_CONSUMER_KEY
   RDM_CONSUMER_SECRET=YOUR_RDM_CONSUMER_SECRET
   RDM_CONSUMER_GROUP=SC-41fc370b-16f7-4d70-a0b7-4674405a0ce6
   RDM_SASL_MECHANISM=PLAIN
   RDM_SECURITY_PROTOCOL=SASL_SSL

   OSC_HOST=127.0.0.1
   OSC_PORT=7400
   ```

---

### 4. Launch the Live Stream

To start consuming live National Rail train updates and streaming OSC to Max:

```bash
python3 -m src.rdm_consumer
```

**Expected Terminal Output**:
```text
2026-08-07 19:30:00 [INFO] Connected to local SQLite database at 'train_sonification.db'.
2026-08-07 19:30:00 [INFO] Connecting to Live National Rail Darwin Kafka cluster at pkc-z3p1v0.europe-west2.gcp.confluent.cloud:9092...
2026-08-07 19:30:01 [INFO] Subscribed to live topic 'prod-1010-Darwin-Train-Information-Push-Port-IIII2_0-JSON'.
2026-08-07 19:30:05 [INFO] LIVE [TS_UPDATE] Station: EDINB | Train: 1A99 | Status: ON TIME | Delay: 0s | Platform: 14
2026-08-07 19:30:06 [INFO] LIVE [TS_UPDATE] Station: MNCRPIC | Train: 9X99 | Status: LATE | Delay: 540s | Platform: 12
```

---

### 5. Alternative: Running the Synthetic Producer Simulator

If you are offline or testing specific sonification scenarios, launch the built-in simulator:

```bash
python3 -m src.producer_sim
```

To run a continuous loop (e.g. 1,000 events at 1.0s interval):
```bash
python3 -c "from src.producer_sim import run_simulator; run_simulator(interval_seconds=1.0, count=1000)"
```

---

### 6. Connect Cycling '74 Max

1. Open [`train_data_sonification.maxpat`](file:///Users/milludaltcasa/Desktop/YEAR%203%20SEM%201/Creative%20Coding%20for%20Sound/Assignment%202/TRAIN_DATA_SONIFICATION/train_data_sonification.maxpat) in Cycling '74 Max.
2. Turn on the audio engine (`ezdac~`).
3. Max will receive live OSC packets on UDP `127.0.0.1:7400`.

---

## OSC Address & Parameter Protocol

| OSC Address | Data Payload | Description / Max Parameter Mapping |
| :--- | :--- | :--- |
| **`/train/event`** | `[schedule_id, train_id, station_code, status, delay_sec, platform]` | Full record packet for display and parsing. |
| **`/train/delay`** | `[delay_sec]` | Macro delay in seconds (modulates filter cutoff frequency, pitch shift, resonance). |
| **`/train/trigger`** | `[station_code, status_int, delay_sec]` | Discrete trigger (`0`=On Time, `1`=Early, `2`=Late, `3`=Cancelled, `4`=Activated) for envelope triggers & per-station subpatch routing. |

---

## Running Unit Tests

Run the full automated unit test suite covering schema parsing, delay calculation edge cases, database persistence, and OSC packet generation:

```bash
python3 -m unittest discover -s tests
```

---

## Project Structure

```text
.
├── .env                       # Local RDM credentials (git-ignored)
├── .env.example               # Environment variable template
├── README.md                  # Project documentation & setup guide
├── requirements.txt           # Python dependency manifest
├── docker-compose.yml         # Container stack (KRaft Kafka, TimescaleDB, Kafka UI)
├── scripts/
│   └── init_db.sql            # TimescaleDB hypertable setup script
├── src/
│   ├── __init__.py
│   ├── database.py            # TimescaleDB & SQLite auto-fallback manager
│   ├── main.py                # Local Kafka consumer entrypoint
│   ├── osc_sender.py          # UDP OSC transport module
│   ├── parser.py              # Darwin JSON/XML schema parser & record flattener
│   ├── producer_sim.py        # Synthetic Darwin event producer
│   └── rdm_consumer.py        # Live Rail Data Marketplace consumer
├── tests/
│   ├── test_phase1.py         # Phase 1 unit tests (parsing, delays, fields)
│   └── test_phase2.py         # Phase 2 unit tests (database, OSC transport)
└── train_data_sonification.maxpat # Cycling '74 Max audio synthesis patch
```
