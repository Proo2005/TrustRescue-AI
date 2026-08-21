import streamlit as st
import pandas as pd
import requests
import json
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# Page Configuration
st.set_page_config(
    page_title="TrustRescue AI Command Center",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern Glassmorphism Custom CSS Styling ---
st.markdown("""
<style>
    /* Main Background & Theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    /* Header Typography */
    h1, h2, h3 {
        color: #f1f5f9;
        font-weight: 700;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Main Title Header
st.markdown("""
    <div style='padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 25px;'>
        <h1 style='margin:0; font-size: 2.2rem;'>🚨 TrustRescue AI Command Center</h1>
        <p style='color: #94a3b8; margin: 5px 0 0 0; font-size: 1.1rem;'>Autonomous Disaster Reconnaissance & Emergency Response Optimization Engine</p>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar for Telemetry Input ---
st.sidebar.header("📡 Live Sensor & Drone Telemetry")

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

# --- New Feature: Live Environmental Threat Index Meter in Sidebar ---
st.sidebar.markdown("---")
st.sidebar.subheader("⚠️ Environmental Threat Index")
threat_score = min(100, int((input_data["water_level"] / 15.0 * 40) + 
                            (input_data["wind_speed"] / 120.0 * 30) + 
                            (input_data["air_quality"] / 500.0 * 30)))
st.sidebar.progress(threat_score / 100.0)
if threat_score > 60:
    st.sidebar.error(f"Threat Index: {threat_score}/100 (CRITICAL)")
elif threat_score > 30:
    st.sidebar.warning(f"Threat Index: {threat_score}/100 (MODERATE)")
else:
    st.sidebar.success(f"Threat Index: {threat_score}/100 (LOW)")

# Initialize Session State for Custom Waypoints / Clicked Points
if "custom_waypoints" not in st.session_state:
    st.session_state.custom_waypoints = [
        {"name": "Shelter A (Safe Zone)", "lat": 22.5726, "lon": 88.3639},
        {"name": "Victim Zone (Hazard)", "lat": 22.6000, "lon": 88.3900}
    ]

# Layout Columns
# Layout Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
   
    st.markdown('<h3 style="margin-top:0;">📋 Active Telemetry Payload</h3>', unsafe_allow_html=True)
    st.json(input_data)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top:0;">📍 Manual Waypoint Management</h3>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown('<h3 style="margin-top:0;">🗺️ Interactive Crisis Map</h3>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Click anywhere on the map to drop coordinates or inspect checkpoints.</p>", unsafe_allow_html=True)
    m = folium.Map(location=[22.5850, 88.3750], zoom_start=13, tiles="CartoDB dark_matter")
    
    for wp in st.session_state.custom_waypoints:
        folium.Marker(
            [wp["lat"], wp["lon"]], 
            popup=wp["name"], 
            tooltip=wp["name"],
            icon=folium.Icon(color="red" if "Hazard" in wp["name"] or "Zone" in wp["name"] else "green", icon="info-sign")
        ).add_to(m)

    if len(st.session_state.custom_waypoints) >= 2:
        route_coords = [[wp["lat"], wp["lon"]] for wp in st.session_state.custom_waypoints]
        folium.PolyLine(route_coords, color="#3b82f6", weight=4, opacity=0.8).add_to(m)

    map_data = st_folium(m, height=420, width=700)

    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lng = map_data["last_clicked"]["lng"]
        if "last_click_processed" not in st.session_state or st.session_state.last_click_processed != (clicked_lat, clicked_lng):
            st.session_state.last_click_processed = (clicked_lat, clicked_lng)
            st.session_state.custom_waypoints.append({
                "name": f"Node_{len(st.session_state.custom_waypoints)+1}",
                "lat": clicked_lat,
                "lon": clicked_lng
            })
            st.rerun()

    total_manual_distance = 0.0
    for i in range(len(st.session_state.custom_waypoints) - 1):
        pt1 = (st.session_state.custom_waypoints[i]["lat"], st.session_state.custom_waypoints[i]["lon"])
        pt2 = (st.session_state.custom_waypoints[i+1]["lat"], st.session_state.custom_waypoints[i+1]["lon"])
        total_manual_distance += geodesic(pt1, pt2).kilometers

    st.markdown(f"<div style='margin-top: 15px; background: rgba(59, 130, 246, 0.1); padding: 10px 15px; border-radius: 8px; border-left: 4px solid #3b82f6;'>📏 <b>Manual Route Distance:</b> {total_manual_distance:.2f} km across {len(st.session_state.custom_waypoints)} nodes</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AI Intelligence Dispatch Section
st.markdown("---")
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("⚡ AI Response & Tactical Resource Dispatch")

if st.button("Run AI Intelligence & Dispatch Units", type="primary"):
    try:
        payload = {
            "record": input_data,
            "waypoints": st.session_state.custom_waypoints
        }
        response = requests.post("http://127.0.0.1:8000/ingest-and-optimize/", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            severity = result.get("ai_predicted_severity_level", "Medium")
            
            # Store result in session state for export capability
            st.session_state.last_mission_report = {
                "telemetry": input_data,
                "threat_score": threat_score,
                "ai_severity": severity,
                "rescue_methods": result.get("rescue_methods", []),
                "allocated_units": result.get("allocated_units", []),
                "evacuation_route": result.get("evacuation_route", []),
                "total_distance_km": result.get("total_distance_km", 0.0)
            }
            
            st.markdown("<br>", unsafe_allow_html=True)
            if severity == "High":
                st.error(f"⚠️ AI Predicted Severity Level: **{severity}**")
            elif severity == "Medium":
                st.warning(f"⚠️ AI Predicted Severity Level: **{severity}**")
            else:
                st.info(f"✅ AI Predicted Severity Level: **{severity}**")

            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.markdown("#### 🛡️ Recommended Methods of Rescue")
                for method in result.get("rescue_methods", []):
                    st.markdown(f"- ✅ {method}")

                st.markdown("#### 🚑 Automated Emergency Unit Dispatch")
                for unit in result.get("allocated_units", []):
                    st.markdown(f"- {unit}")

            with col_res2:
                st.markdown("#### 🗺️ Evacuation Logistics & Routing")
                st.write(f"**Optimized Route:** `{' -> '.join(result.get('evacuation_route', []))}`")
                st.write(f"**Total Path Distance:** {result.get('total_distance_km')} km")
            
        else:
            st.error(f"Backend Error: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI backend. Ensure your backend server is running (`uvicorn model:app --reload`).")

# --- New Feature: Export Mission Report Button ---
if "last_mission_report" in st.session_state:
    st.markdown("---")
    report_json = json.dumps(st.session_state.last_mission_report, indent=4)
    st.download_button(
        label="📥 Download Official Mission Report (JSON)",
        data=report_json,
        file_name="trustrescue_mission_report.json",
        mime="application/json"
    )

st.markdown('</div>', unsafe_allow_html=True)