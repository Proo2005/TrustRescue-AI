import pandas as pd
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException
import networkx as nx
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Initialize FastAPI app
app = FastAPI(title="TrustRescue AI Engine", version="1.0")

# Global variables for trained model components
ml_model = None
label_encoder = None
model_feature_columns = None

# --- Step 1: Data Validation Schema ---
class DisasterRecordSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    air_quality_index: Optional[float] = Field(None, alias="air_quality")
    water_level: Optional[float] = None
    building_damage_level: Optional[str] = Field(None, alias="building_damage_level")
    road_condition: Optional[str] = Field(None, alias="road_condition")
    infrastructure_status: Optional[str] = Field(None, alias="infrastructure_status")
    vegetation_cover: Optional[float] = Field(None, alias="vegetation_cover")
    people_detected: Optional[float] = Field(None, alias="people_detected")
    heat_signatures: Optional[float] = Field(None, alias="heat_signatures")
    hazardous_material_detected: Optional[int] = Field(None, alias="hazardous_material_detected")
    disaster_severity_level: Optional[str] = Field(None, alias="disaster_severity_level")
    affected_area_type: Optional[str] = Field(None, alias="affected_area_type")
    immediate_action_required: Optional[str] = Field(None, alias="immediate_action_required")
    survivor_presence_likelihood: Optional[str] = Field(None, alias="survivor_presence_likelihood")

    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return pd.to_datetime(value)
        return value

class DynamicOptimizationRequest(BaseModel):
    record: DisasterRecordSchema
    waypoints: Optional[List[Dict[str, Any]]] = None

def validate_dataset_stream(csv_file_path: str):
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()
    
    valid_records = []
    errors = []

    for index, row in df.iterrows():
        try:
            record = DisasterRecordSchema.model_validate(row.to_dict())
            valid_records.append(record.model_dump(by_alias=True))
        except Exception as e:
            errors.append({"row": index, "error": str(e)})

    print(f"Successfully validated: {len(valid_records)} records.")
    print(f"Validation errors found: {len(errors)} records.")
    return valid_records, errors


# --- Step 2: Training the Risk Scoring Classifier ---
def train_enhanced_risk_classifier(csv_file_path: str):
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()

    numerical_features = [
        'temperature', 'humidity', 'wind_speed', 'air_quality_index', 
        'water_level', 'vegetation_cover', 'people_detected', 
        'heat_signatures', 'hazardous_material_detected'
    ]
    
    categorical_features = [
        'building_damage_level', 'road_condition', 'infrastructure_status', 'affected_area_type'
    ]
    
    target_col = 'disaster_severity_level'
    df = df.dropna(subset=numerical_features + categorical_features + [target_col])

    X_num = df[numerical_features]
    X_cat = pd.get_dummies(df[categorical_features], drop_first=True)
    X = pd.concat([X_num, X_cat], axis=1)

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(df[target_col])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"Enhanced Model Training Complete!")
    print(f"Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=encoder.classes_))

    return clf, encoder, X.columns.tolist()


# --- Step 3: Dynamic Routing & Evacuation Optimization ---
def build_default_evacuation_network():
    G = nx.Graph()
    G.add_node("Shelter_A", pos=(22.5726, 88.3639), type="safe_zone", capacity=500)
    G.add_node("Node_1", pos=(22.5800, 88.3700), type="junction", risk_level="Low")
    G.add_node("Node_2", pos=(22.5900, 88.3800), type="junction", risk_level="High")
    G.add_node("Victim_Zone", pos=(22.6000, 88.3900), type="hazard", risk_level="Critical")

    G.add_edge("Victim_Zone", "Node_2", distance=2.5, road_condition="Obstructed", weight=float('inf'))
    G.add_edge("Victim_Zone", "Node_1", distance=3.0, road_condition="Clear", weight=3.0)
    G.add_node("Node_1", pos=(22.5800, 88.3700))
    G.add_edge("Node_1", "Shelter_A", distance=1.5, road_condition="Clear", weight=1.5)
    G.add_edge("Node_2", "Shelter_A", distance=2.0, road_condition="Clear", weight=2.0)
    return G


# --- Startup Event to Train Model Once ---
@app.on_event("startup")
def startup_event():
    global ml_model, label_encoder, model_feature_columns
    csv_path = "dataset/drone_disaster_area_identification_dataset.csv"
    ml_model, label_encoder, model_feature_columns = train_enhanced_risk_classifier(csv_path)


# --- Step 4: FastAPI Integration Endpoint with Automated Rescue Methods Analysis ---
@app.post("/ingest-and-optimize/")
def process_disaster_telemetry(payload: DynamicOptimizationRequest):
    try:
        record = payload.record
        waypoints = payload.waypoints
        
        validated_data = record.model_dump(by_alias=True)
        
        if "air_quality" in validated_data and "air_quality_index" not in validated_data:
            validated_data["air_quality_index"] = validated_data["air_quality"]
        
        # Prepare input dataframe for model prediction
        input_df = pd.DataFrame([validated_data])
        numerical_features = [
            'temperature', 'humidity', 'wind_speed', 'air_quality_index', 
            'water_level', 'vegetation_cover', 'people_detected', 
            'heat_signatures', 'hazardous_material_detected'
        ]
        categorical_features = [
            'building_damage_level', 'road_condition', 'infrastructure_status', 'affected_area_type'
        ]
        
        X_num = input_df[numerical_features]
        X_cat = pd.get_dummies(input_df[categorical_features], drop_first=True)
        X_input = pd.concat([X_num, X_cat], axis=1)
        X_input = X_input.reindex(columns=model_feature_columns, fill_value=0)
        
        pred_encoded = ml_model.predict(X_input)[0]
        ml_severity = label_encoder.inverse_transform([pred_encoded])[0]

        water_lvl = validated_data.get("water_level", 0)
        road_cond = validated_data.get("road_condition", "Clear")
        damage = validated_data.get("building_damage_level", "Undamaged")
        hazards = validated_data.get("hazardous_material_detected", 0)
        area_type = validated_data.get("affected_area_type", "Unblocked")

        if water_lvl > 8.0 or road_cond == "Blocked" or hazards == 1 or damage == "Severe":
            predicted_severity = "High"
        elif water_lvl > 4.0 or road_cond == "Obstructed" or damage == "Moderate":
            predicted_severity = "Medium"
        else:
            predicted_severity = ml_severity

        # --- Automated Rescue Methods Analysis Engine ---
        rescue_methods = []
        allocated_units = []

        if predicted_severity == "High":
            rescue_methods.append("Aerial Reconnaissance & Medical Evacuation (Chopper/UAV)")
            allocated_units.extend(["🚨 2x Heavy Rescue Teams", "🚁 1x Medical Evacuation Chopper"])
        else:
            allocated_units.append("🚑 1x Standard Ambulance")

        if area_type == "Flooded" or water_lvl > 4.0:
            rescue_methods.append("Waterborne Surface Rescue (Aquatic Extraction)")
            allocated_units.append("🚤 1x Rescue Boat Unit")

        if area_type == "Fire-Damaged":
            rescue_methods.append("Fire Suppression & Thermal Mitigation")
            allocated_units.append("🚒 2x Fire Suppression Units")

        if damage in ["Severe", "Moderate"] or road_cond in ["Obstructed", "Blocked"]:
            rescue_methods.append("Heavy Ground Extraction & Debris Clearance")

        if hazards == 1:
            rescue_methods.append("Hazardous Materials Containment & Decontamination (HazMat)")
            allocated_units.append("☢️ HazMat Specialist Team")

        if not rescue_methods:
            rescue_methods.append("Standard Ground Evacuation & Monitoring")

        # Build Graph dynamically from user waypoints or fallback to default
        graph = nx.Graph()
        if waypoints and len(waypoints) >= 2:
            for wp in waypoints:
                graph.add_node(wp["name"], pos=(wp["lat"], wp["lon"]))
            
            for i in range(len(waypoints) - 1):
                p1 = (waypoints[i]["lat"], waypoints[i]["lon"])
                p2 = (waypoints[i+1]["lat"], waypoints[i+1]["lon"])
                dist = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5 * 111.0
                
                weight = float('inf') if road_cond in ["Obstructed", "Blocked"] and i == 0 else dist
                graph.add_edge(waypoints[i]["name"], waypoints[i+1]["name"], distance=dist, weight=weight)
            
            source = waypoints[0]["name"]
            target = waypoints[-1]["name"]
        else:
            graph = build_default_evacuation_network()
            if road_cond in ["Obstructed", "Blocked"]:
                if graph.has_edge("Victim_Zone", "Node_1"):
                    graph["Victim_Zone"]["Node_1"]["weight"] = float('inf')
            source = "Victim_Zone"
            target = "Shelter_A"

        path = nx.shortest_path(graph, source=source, target=target, weight='weight')
        total_distance = nx.path_weight(graph, path, weight='distance')

        return {
            "status": "success",
            "ai_predicted_severity_level": predicted_severity,
            "rescue_methods": rescue_methods,
            "allocated_units": list(set(allocated_units)),
            "evacuation_route": path,
            "total_distance_km": round(total_distance, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))