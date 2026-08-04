-- TimescaleDB Initialization Script for Train Data Sonification

CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE IF NOT EXISTS train_events (
    time TIMESTAMPTZ NOT NULL,
    schedule_id TEXT NOT NULL,
    train_id TEXT,
    station_code TEXT,
    origin TEXT,
    destination TEXT,
    status TEXT,
    delay_seconds INT DEFAULT 0,
    platform TEXT,
    scheduled_arrival TEXT,
    scheduled_departure TEXT,
    predicted_arrival TEXT,
    predicted_departure TEXT,
    event_type TEXT
);

-- Convert train_events into a TimescaleDB hypertable partitioned by 'time'
SELECT create_hypertable('train_events', 'time', if_not_exists => TRUE);

-- Create index on station_code, train_id, and schedule_id for rapid querying
CREATE INDEX IF NOT EXISTS idx_train_events_station ON train_events (station_code, time DESC);
CREATE INDEX IF NOT EXISTS idx_train_events_schedule ON train_events (schedule_id, time DESC);
