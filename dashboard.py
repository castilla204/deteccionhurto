import os
import json
import cv2
import streamlit as st
from datetime import datetime
from collections import defaultdict
from PIL import Image


EVENTS_DIR = "events"


def load_events():
    events = []
    if not os.path.exists(EVENTS_DIR):
        return events

    for event_name in os.listdir(EVENTS_DIR):
        event_path = os.path.join(EVENTS_DIR, event_name)
        if not os.path.isdir(event_path):
            continue

        metadata_path = os.path.join(event_path, "metadata.json")
        video_path = os.path.join(event_path, "clip.mp4")

        if not os.path.exists(metadata_path) or not os.path.exists(video_path):
            continue

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        timestamp = datetime.strptime(metadata["time"], "%Y-%m-%d %H:%M:%S")
        events.append({
            "event_dir": event_path,
            "video": video_path,
            "metadata": metadata,
            "timestamp": timestamp,
        })

    events.sort(key=lambda x: x["timestamp"], reverse=True)
    return events


def extract_thumbnail(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame)


def group_events_by_date(events):
    grouped = defaultdict(list)
    for event in events:
        date_key = event["timestamp"].strftime("%d/%m/%Y")
        grouped[date_key].append(event)
    return grouped


st.set_page_config(
    page_title="Deteccion Hurto - Historial",
    layout="wide",
)

st.title("Historial de incidentes")
st.caption("Diego Castilla · deteccionhurto")

events = load_events()
grouped_events = group_events_by_date(events)

if not events:
    st.info("Todavia no hay incidentes guardados.")
    st.stop()

for date, day_events in grouped_events.items():
    st.subheader(date)

    for event in day_events:
        col1, col2 = st.columns([1, 5])
        thumbnail = extract_thumbnail(event["video"])

        with col1:
            if thumbnail:
                st.image(thumbnail, width=120)

        with col2:
            meta = event["metadata"]
            time_str = event["timestamp"].strftime("%H:%M")

            st.markdown("**Posible hurto**")
            st.caption(f"{time_str} · Camara {meta['camera_id']} · Riesgo {meta['risk_score']}")

            with st.expander("Ver clip y metadatos"):
                st.video(event["video"])
                st.json(meta)

        st.divider()
