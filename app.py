import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="TrustRescue AI Command Center", layout="wide")

st.title("🚨 TrustRescue AI: Emergency Command & Resource Allocation Dashboard")
st.markdown("Real-time telemetry ingestion, machine learning severity scoring, dynamic routing, and automated resource dispatch.")

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

# Main Panel Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Submitted Telemetry Payload")
    st.json(input_data)

with col2:
    st.subheader("⚡ AI Response & Resource Dispatch")
    if st.button("Run AI Intelligence & Dispatch Units", type="primary"):
        try:
            response = requests.post("http://127.0.0.1:8000/ingest-and-optimize/", json=input_data)
            if response.status_code == 200:
                result = response.json()
                severity = result.get("ai_predicted_severity_level", "Medium")
                area_type = input_data["affected_area_type"]
                
                st.success("Analysis and Optimization Successful!")
                
                # Display Severity Metric with Color Badges
                if severity == "High":
                    st.error(f"⚠️ AI Predicted Severity Level: **{severity}**")
                elif severity == "Medium":
                    st.warning(f"⚠️ AI Predicted Severity Level: **{severity}**")
                else:
                    st.info(f"✅ AI Predicted Severity Level: **{severity}**")

                # Automated Resource Allocation Engine
                st.markdown("### 🚑 Automated Emergency Unit Dispatch")
                allocated_units = []
                if severity == "High":
                    allocated_units.append("🚨 2x Heavy Rescue Teams")
                    allocated_units.append("🚁 1x Medical Evacuation Chopper")
                else:
                    allocated_units.append("🚑 1x Standard Ambulance")
                
                if area_type == "Flooded":
                    allocated_units.append("🚤 1x Rescue Boat Unit")
                elif area_type == "Fire-Damaged":
                    allocated_units.append("🚒 2x Fire Suppression Units")
                
                if input_data["hazardous_material_detected"] == 1:
                    allocated_units.append("☢️ HazMat Specialist Team")

                for unit in allocated_units:
                    st.markdown(f"- {unit}")

                # Routing Details
                st.markdown("### 🗺️ Evacuation Logistics")
                st.write(f"**Optimized Route:** `{' -> '.join(result.get('evacuation_route', []))}`")
                st.write(f"**Total Distance:** {result.get('total_distance_km')} km")

                # Map Visualization Mock / Coordinates
                st.markdown("### 📍 Crisis Zone Map View")
                map_data = pd.DataFrame({
                    'lat': [22.6000, 22.5800, 22.5726],
                    'lon': [88.3900, 88.3700, 88.3639],
                    'name': ['Victim Zone (Hazard)', 'Junction Node 1', 'Shelter A (Safe Zone)']
                })
                st.map(map_data, zoom=12)

            else:
                st.error(f"Backend Error: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI backend. Ensure your backend server is running (`uvicorn model:app --reload`).")