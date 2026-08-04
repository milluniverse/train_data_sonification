"""
Darwin PubSub Message Parser and Record Flattener.
Phase 1: Ingestion, Schema Mapping, and Normalization.
"""

from datetime import datetime, timezone
import json
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union


def parse_raw_message(raw_data: Union[str, bytes, dict]) -> Optional[Dict[str, Any]]:
    """
    Parse a raw message received from Kafka/PubSub.
    Handles raw JSON strings, dictionary objects, or base64-encoded XML/JSON payloads.
    """
    if isinstance(raw_data, (bytes, bytearray)):
        raw_data = raw_data.decode("utf-8")

    if isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
        except json.JSONDecodeError:
            # Check if it's direct XML string
            if raw_data.strip().startswith("<"):
                return parse_xml_payload(raw_data)
            return None

    if not isinstance(raw_data, dict):
        return None

    # Handle RDM envelope wrapper
    # Check if 'bytes' field contains embedded JSON or base64-encoded payload
    if "bytes" in raw_data and raw_data["bytes"]:
        content = raw_data["bytes"]
        if isinstance(content, str):
            # Try plain JSON decoding
            try:
                decoded_json = json.loads(content)
                return decoded_json
            except json.JSONDecodeError:
                pass

            # Try base64 decoding
            try:
                b64_decoded = base64.b64decode(content).decode("utf-8")
                try:
                    return json.loads(b64_decoded)
                except json.JSONDecodeError:
                    if b64_decoded.strip().startswith("<"):
                        return parse_xml_payload(b64_decoded)
            except Exception:
                pass

    return raw_data


def parse_xml_payload(xml_str: str) -> Dict[str, Any]:
    """
    Fallback parser for XML Darwin messages into a dictionary representation.
    """
    try:
        root = ET.fromstring(xml_str)
        # Strip namespace tags
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        
        def elem_to_dict(node):
            d = dict(node.attrib)
            for child in node:
                child_data = elem_to_dict(child)
                if child.tag in d:
                    if not isinstance(d[child.tag], list):
                        d[child.tag] = [d[child.tag]]
                    d[child.tag].append(child_data)
                else:
                    d[child.tag] = child_data
            if node.text and node.text.strip():
                if d:
                    d['content'] = node.text.strip()
                else:
                    return node.text.strip()
            return d

        return {root.tag: elem_to_dict(root)}
    except Exception:
        return {}


def time_to_seconds(time_str: Optional[str]) -> Optional[int]:
    """
    Convert a 'HH:MM' or 'HH:MM:SS' time string to seconds since midnight.
    Returns None if time_str is invalid or None.
    """
    if not time_str:
        return None
    time_str = time_str.strip()
    parts = time_str.split(":")
    try:
        if len(parts) == 2:
            return int(parts[0]) * 3600 + int(parts[1]) * 60
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except ValueError:
        return None
    return None


def calculate_delay_seconds(
    scheduled_time: Optional[str],
    actual_or_forecast_time: Optional[str]
) -> int:
    """
    Calculate delay in seconds between scheduled time and actual/forecast time.
    Positive value = late running (seconds).
    Negative value = early running (seconds).
    Zero = exactly on time.
    Handles midnight boundary crossings (-6h to +18h rule).
    """
    sched_sec = time_to_seconds(scheduled_time)
    real_sec = time_to_seconds(actual_or_forecast_time)

    if sched_sec is None or real_sec is None:
        return 0

    diff = real_sec - sched_sec

    # Midnight crossing adjustments per Thales spec:
    # If diff < -6 hours (-21600 seconds), assume train crossed midnight (+24 hours)
    if diff < -21600:
        diff += 86400
    # If diff > +18 hours (+64800 seconds), assume train crossed midnight backwards (-24 hours)
    elif diff > 64800:
        diff -= 86400

    return diff


def flatten_darwin_update(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract and flatten raw Darwin updates into normalized key-value records.
    
    Fields extracted:
    - train_id
    - schedule_id
    - origin
    - destination
    - station_code
    - scheduled_arrival
    - scheduled_departure
    - predicted_arrival
    - predicted_departure
    - platform
    - status
    - delay_seconds
    - timestamp
    """
    records: List[Dict[str, Any]] = []
    if not payload:
        return records

    # Unwrap 'uR' (update response) or 'sR' (snapshot response)
    response_root = payload.get("uR") or payload.get("sR") or payload

    # Extract 'TS' (Train Status) movement and forecast updates
    ts_updates = response_root.get("TS")
    if ts_updates:
        if isinstance(ts_updates, dict):
            ts_updates = [ts_updates]

        for ts in ts_updates:
            rid = ts.get("rid", "")
            locations = ts.get("Location") or ts.get("location") or []
            if isinstance(locations, dict):
                locations = [locations]

            for loc in locations:
                tpl = loc.get("tpl", "")
                wta = loc.get("wta")
                pta = loc.get("pta")
                wtd = loc.get("wtd")
                ptd = loc.get("ptd")

                sched_arr = pta or wta
                sched_dep = ptd or wtd

                # Check arrival or departure reports
                arr = loc.get("arr") or {}
                dep = loc.get("dep") or {}

                act_arr = arr.get("at") if isinstance(arr, dict) else None
                fcst_arr = arr.get("et") if isinstance(arr, dict) else None
                act_dep = dep.get("at") if isinstance(dep, dict) else None
                fcst_dep = dep.get("et") if isinstance(dep, dict) else None

                pred_arr = act_arr or fcst_arr
                pred_dep = act_dep or fcst_dep

                # Compute delay using departure if available, else arrival
                if pred_dep and sched_dep:
                    delay_sec = calculate_delay_seconds(sched_dep, pred_dep)
                elif pred_arr and sched_arr:
                    delay_sec = calculate_delay_seconds(sched_arr, pred_arr)
                else:
                    delay_sec = 0

                # Platform extraction
                plat_info = loc.get("plat") or {}
                platform = ""
                if isinstance(plat_info, dict):
                    platform = plat_info.get("content") or plat_info.get("plat") or ""
                elif isinstance(plat_info, str):
                    platform = plat_info

                # Status & Delay
                is_cancelled = loc.get("can") == "true" or loc.get("can") is True

                if is_cancelled:
                    status = "CANCELLED"
                elif (pred_dep and sched_dep) or (pred_arr and sched_arr):
                    if delay_sec > 60:
                        status = "LATE"
                    elif delay_sec < -60:
                        status = "EARLY"
                    else:
                        status = "ON TIME"
                else:
                    status = "NO REPORT"

                records.append({
                    "event_type": "TS_UPDATE",
                    "schedule_id": rid,
                    "train_id": ts.get("uid") or ts.get("trainId") or rid,
                    "origin": loc.get("origin", ""),
                    "destination": loc.get("destination", ""),
                    "station_code": tpl,
                    "scheduled_arrival": sched_arr,
                    "scheduled_departure": sched_dep,
                    "predicted_arrival": pred_arr,
                    "predicted_departure": pred_dep,
                    "platform": platform,
                    "status": status,
                    "delay_seconds": delay_sec,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })

    # Extract 'schedule' updates
    schedule = response_root.get("schedule")
    if schedule:
        if isinstance(schedule, dict):
            schedules = [schedule]
        else:
            schedules = schedule

        for sch in schedules:
            rid = sch.get("rid", "")
            uid = sch.get("uid", "")
            train_id = sch.get("trainId") or uid or rid

            # Extract Origin (OR) and Destination (DT)
            origin_node = sch.get("OR") or {}
            dest_node = sch.get("DT") or {}

            origin_tpl = origin_node.get("tpl", "") if isinstance(origin_node, dict) else ""
            dest_tpl = dest_node.get("tpl", "") if isinstance(dest_node, dict) else ""

            records.append({
                "event_type": "SCHEDULE_ACTIVATION",
                "schedule_id": rid,
                "train_id": train_id,
                "origin": origin_tpl,
                "destination": dest_tpl,
                "station_code": origin_tpl,
                "scheduled_arrival": None,
                "scheduled_departure": origin_node.get("ptd") or origin_node.get("wtd") if isinstance(origin_node, dict) else None,
                "predicted_arrival": None,
                "predicted_departure": None,
                "platform": "",
                "status": "ACTIVATED",
                "delay_seconds": 0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

    return records

