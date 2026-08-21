import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

st.set_page_config(page_title="TrustRescue AI Command Center", layout="wide")

st.title("🚨 TrustRescue AI: Interactive Command & Routing Dashboard")
st.markdown("Select points manually on the interactive map, track live locations, and compute dynamic routing distances.")

# Sidebar for Telemetry Input
st.sidebar.header("📡 Live Drone / Sensor Telemetry")

def user_input_features():
    timestamp = str(pd.Timestamp.now())
    temperature = st.sidebar.slider("Temperature (°C)", 10.0, 50.0, 28.5)
    humidity = st.sidebar.slider("Humidity (%)", 10.0, 100.0, 75.0)
    wind_speed = st.sidebar.slider("Wind Speed (km/h)", 0.0, 120.0, 15.0)
    air_quality = st.sidebar.slider("Air Quality Index (AQI)", 0.0, 500.0, 120.0)
    water_level = st.sidebar.slider("Water Level (m)", 0.0, 15.0, 3.5)
    
    building_damage_level = st.sidebar.selectbox("Building Damage Level", ["Undamaged", "Minor", "Moderate", "Severe"])
    road_condition = st.sidebar.selectbox("Road Condition", ["Clear", "Obstructed", "Blocked"])
    infrastructure_status = st.sidebar.selectbox("Infrastructure Status", ["Intact", "Damaged", "Destroyed"])
    
    vegetation_cover = st.sidebar.slider("Vegetation Cover (%)", 0.0, 100.0, 50.0)
    people_detected = st.sidebar.number_input("People Detected", min_value=0, value=2)
    heat_signatures = st.sidebar.number_input("Heat Signatures", min_value=0, value=3)
    hazardous_material_detected = st.sidebar.selectbox("Hazardous Material Detected", [0, 1])
    
    affected_area_type = st.sidebar.selectbox("Affected Area Type", ["Flooded", "Unblocked", "Fire-Damaged"])
    immediate_action_required = st.sidebar.selectbox("Immediate Action Required", ["Yes", "No"])
    survivor_presence_likelihood = st.sidebar.selectbox("Survivor Presence Likelihood", ["High", "Medium", "Low"])

    data = {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "air_quality": air_quality,
        "water_level": water_level,
        "building_damage_level": building_damage_level,
        "road_condition": road_condition,
        "infrastructure_status": infrastructure_status,
        "vegetation_cover": vegetation_cover,
        "people_detected": float(people_detected),
        "heat_signatures": float(heat_signatures),
        "hazardous_material_detected": int(hazardous_material_detected),
        "disaster_severity_level": "Medium",
        "affected_area_type": affected_area_type,
        "immediate_action_required": immediate_action_required,
        "survivor_presence_likelihood": survivor_presence_likelihood
    }
    return data

input_data = user_input_features()

# Initialize Session State for Custom Waypoints / Clicked Points
if "custom_waypoints" not in st.session_state:
    st.session_state.custom_waypoints = [
        {"name": "Shelter A (Safe Zone)", "lat": 22.5726, "lon": 88.3639},
        {"name": "Victim Zone (Hazard)", "lat": 22.6000, "lon": 88.3900}
    ]

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Submitted Telemetry Payload")
    st.json(input_data)

    st.subheader("📍 Manual Waypoint Management")
    with st.form("add_waypoint_form"):
        wp_name = st.text_input("Waypoint Name", value=f"Node_{len(st.session_state.custom_waypoints)+1}")
        wp_lat = st.number_input("Latitude", value=22.5850, format="%.4f")
        wp_lon = st.number_input("Longitude", value=88.3750, format="%.4f")
        add_btn = st.form_submit_button("Add Custom Waypoint")
        if add_btn:
            st.session_state.custom_waypoints.append({"name": wp_name, "lat": wp_lat, "lon": wp_lon})
            st.success(f"Added waypoint: {wp_name}")

    if st.button("Reset Waypoints"):
        st.session_state.custom_waypoints = [
            {"name": "Shelter A (Safe Zone)", "lat": 22.5726, "lon": 88.3639},
            {"name": "Victim Zone (Hazard)", "lat": 22.6000, "lon": 88.3900}
        ]
        st.rerun()

with col2:
    st.subheader("🗺️ Interactive Map (Click to Inspect/Add)")
    st.markdown("*(Click anywhere on the map to capture coordinates or review node distribution)*")

    # Create Folium Map centered around Kolkata region
    m = folium.Map(location=[22.5850, 88.3750], zoom_start=13)
    
    # Render all current waypoints as markers
    for wp in st.session_state.custom_waypoints:
        folium.Marker(
            [wp["lat"], wp["lon"]], 
            popup=wp["name"], 
            tooltip=wp["name"],
            icon=folium.Icon(color="red" if "Hazard" in wp["name"] or "Zone" in wp["name"] else "green", icon="info-sign")
        ).add_to(m)

    # Draw polyline connecting sequential waypoints to calculate manual distance
    if len(st.session_state.custom_waypoints) >= 2:
        route_coords = [[wp["lat"], wp["lon"]] for wp in st.session_state.custom_waypoints]
        folium.PolyLine(route_coords, color="blue", weight=3, opacity=0.8).add_to(m)

    # Capture map clicks using streamlit-folium
    map_data = st_folium(m, height=400, width=700)

    # Check if user clicked on map to add a point
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lng = map_data["last_clicked"]["lng"]
        # Avoid duplicate rerun loops by checking storage
        if "last_click_processed" not in st.session_state or st.session_state.last_click_processed != (clicked_lat, clicked_lng):
            st.session_state.last_click_processed = (clicked_lat, clicked_lng)
            st.session_state.custom_waypoints.append({
                "name": f"Clicked_Node_{len(st.session_state.custom_waypoints)+1}",
                "lat": clicked_lat,
                "lon": clicked_lng
            })
            st.rerun()

    # Calculate Total Manual Route Distance using Geodesy
    total_manual_distance = 0.0
    for i in range(len(st.session_state.custom_waypoints) - 1):
        pt1 = (st.session_state.custom_waypoints[i]["lat"], st.session_state.custom_waypoints[i]["lon"])
        pt2 = (st.session_state.custom_waypoints[i+1]["lat"], st.session_state.custom_waypoints[i+1]["lon"])
        total_manual_distance += geodesic(pt1, pt2).kilometers

    st.info(f"📏 **Calculated Manual Route Distance:** {total_manual_distance:.2f} km across {len(st.session_state.custom_waypoints)} nodes.")

# AI Intelligence Dispatch Section
st.markdown("---")
st.subheader("⚡ AI Response & Resource Dispatch")
if st.button("Run AI Intelligence & Dispatch Units", type="primary"):
    try:
        # --- PLACE THE PAYLOAD AND POST REQUEST HERE ---
        payload = {
            "record": input_data,
            "waypoints": st.session_state.custom_waypoints
        }
        response = requests.post("http://127.0.0.1:8000/ingest-and-optimize/", json=payload)


        if response.status_code == 200:
            result = response.json()
            severity = result.get("ai_predicted_severity_level", "Medium")
            
            if severity == "High":
                st.error(f"⚠️ AI Predicted Severity Level: **{severity}**")
            elif severity == "Medium":
                st.warning(f"⚠️ AI Predicted Severity Level: **{severity}**")
            else:
                st.info(f"✅ AI Predicted Severity Level: **{severity}**")

            st.write(f"**Backend Optimized Route:** `{' -> '.join(result.get('evacuation_route', []))}`")
            st.write(f"**Backend Path Distance:** {result.get('total_distance_km')} km")
        else:
            st.error(f"Backend Error: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI backend. Ensure your backend server is running (`uvicorn model:app --reload`).")