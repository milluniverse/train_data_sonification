# National Rail Darwin Train Data Sonification Engine

A real-time data ingestion, transformation, and musical sonification pipeline that consumes National Rail Darwin Pub/Sub updates via Kafka from the Rail Data Marketplace (RDM), normalizes train delays and status changes in memory, and streams Open Sound Control (OSC) packets over UDP to Cycling '74 Max for real-time audio synthesis.

Developed for **Creative Coding for Sound — Assignment 2 (Option 1: Musical Sonification)**.

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────┐
│              National Rail Darwin Pub/Sub (Confluent Cloud)             │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ SASL_SSL JSON Stream
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 Python Ingestion Engine (src/rdm_consumer.py)           │
│   • Decodes raw RDM JSON updates in memory                              │
│   • Normalizes delays, statuses, platforms, and train IDs               │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     │ Streams UDP OSC Packets
                                     │ 127.0.0.1:7400
                                     ▼
                      ┌─────────────────────────────┐
                      │ Cycling '74 Max Patcher     │
                      │ (train_data_sonification)   │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │ Station Nodes & Master Synth│
                      │ • Station Route (e.g. GLGC) │
                      │ • Status Route (0,1,2,3,4)  │
                      │ • Master Additive Engines   │
                      └─────────────────────────────┘
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
   cd "/Users/milludaltcasa/Desktop/YEAR 3 SEM 1/Creative Coding for Sound/Assignment 2/TRAIN_DATA_SONIFICATION"
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
2026-08-10 04:30:00 [INFO] Connecting to Live National Rail Darwin Kafka cluster at pkc-z3p1v0.europe-west2.gcp.confluent.cloud:9092...
2026-08-10 04:30:01 [INFO] Subscribed to live topic 'prod-1010-Darwin-Train-Information-Push-Port-IIII2_0-JSON'.
2026-08-10 04:30:05 [INFO] LIVE [TS_UPDATE] Station: EDINB | Train: 1A99 | Status: ON TIME | Delay: 0s | Platform: 14
2026-08-10 04:30:06 [INFO] LIVE [TS_UPDATE] Station: MNCRPIC | Train: 9X99 | Status: LATE | Delay: 540s | Platform: 12
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

1. Open `train_data_sonification.maxpat` in Cycling '74 Max.
2. Turn on the audio engine (`ezdac~`).
3. Max will receive live OSC packets on UDP `127.0.0.1:7400`.

---

## 🎛️ OSC Address & Parameter Protocol

| OSC Address | Data Payload | Description / Max Parameter Mapping |
| :--- | :--- | :--- |
| **`/train/event`** | `[station_code, schedule_id, train_id, status, delay_sec, platform]` | Full record packet for display and station routing. |
| **`/train/delay`** | `[delay_sec]` | Macro delay in seconds (modulates filter cutoff frequency, pitch shift, resonance). |
| **`/train/trigger`** | `[station_code, status_int, delay_sec]` | Discrete trigger (`0`=On Time, `1`=Early, `2`=Late, `3`=Cancelled, `4`=Activated) for envelope triggers & per-station subpatch routing. |

---

## 📂 Project Structure

```text
.
├── .env                       # Local RDM credentials (git-ignored)
├── .env.example               # Environment variable template
├── README.md                  # Project documentation & setup guide
├── requirements.txt           # Python dependency manifest
├── docker-compose.yml         # Container stack (KRaft Kafka, Kafka UI)
├── src/
│   ├── __init__.py
│   ├── main.py                # Local Kafka consumer entrypoint
│   ├── osc_sender.py          # UDP OSC transport module
│   ├── parser.py              # Darwin JSON/XML schema parser & record flattener
│   ├── producer_sim.py        # Synthetic Darwin event producer
│   └── rdm_consumer.py        # Live Rail Data Marketplace consumer
└── train_data_sonification.maxpat # Cycling '74 Max audio synthesis patch
```
