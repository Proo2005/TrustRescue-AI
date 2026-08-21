# 🚨 TrustRescue AI: Autonomous Disaster Reconnaissance & Emergency Response Optimization Engine

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-005571?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Table of Contents
1. [Project Overview](#-project-overview)
2. [Architecture & System Workflow](#-architecture--system-workflow)
3. [Mathematical Formulations & Calculations](#-mathematical-formulations--calculations)
4. [Dataset & Features](#-dataset--features)
5. [Model Results & Performance](#-model-results--performance)
6. [Project Structure](#-project-structure)
7. [Installation & How to Run](#-installation--how-to-run)
8. [API Documentation](#-api-documentation)
9. [Author](#-author)
10. [License](#-license)

---

## 🌟 Project Overview
**TrustRescue AI** is an advanced crisis management and disaster response system designed to process real-time drone and IoT sensor telemetry. The platform automates data validation, predicts disaster severity scores using machine learning, calculates safe obstacle-free evacuation paths using graph theory, and instantly dispatches emergency resources through an interactive command dashboard.

---

## 🏗️ Architecture & System Workflow

The system follows a modular 4-tier architecture:

1. **Tier 1: Data Ingestion & Validation (Pydantic & Pandas)**
   - Streaming CSV records and API payloads are ingested and cleaned.
   - Strict schema validation ensures data types, timestamps, and range boundaries ($ge=0, le=10$) are enforced before processing.
2. **Tier 2: AI Risk Scoring Classifier (Scikit-Learn)**
   - Combines numerical sensor parameters and one-hot-encoded infrastructure categoricals.
   - Employs a balanced **Random Forest Classifier** alongside heuristic overrides to output multi-class severity classifications (`Low`, `Medium`, `High`).
3. **Tier 3: Dynamic Graph Routing (NetworkX)**
   - Maps disaster zones as a spatial graph ($G = (V, E)$).
   - Dynamically weights or removes edges (roads) marked as `Obstructed` or `Blocked` ($\text{weight} = \infty$).
4. **Tier 4: Command & Dispatch Dashboard (FastAPI & Streamlit)**
   - Exposes asynchronous backend endpoints and a real-time reactive user interface for automated resource allocation.

---

## 🧮 Mathematical Formulations & Calculations

### 1. Shortest Path & Route Optimization (Dijkstra's Algorithm via NetworkX)
The evacuation network is represented as an undirected weighted graph $G = (V, E)$, where $V$ represents nodes (intersections, hazard zones, safe shelters) and $E$ represents edges (roads). 

The edge weight function $W(e)$ incorporates geographic distance $d(e)$ and hazard penalties:
$$W(e) = \begin{cases} d(e), & \text{if road condition is Clear} \\ \infty, & \text{if road condition is Obstructed or Blocked} \end{cases}$$

The optimal evacuation route $P$ from a hazard source $s$ to shelter target $t$ minimizes total path cost:
$$P = \arg\min_{p \in \text{paths}(s, t)} \sum_{e \in p} W(e)$$

### 2. Random Forest Classification Entropy
To split nodes and classify disaster severity levels, the Random Forest algorithm utilizes Information Gain based on Shannon Entropy ($H$):
$$H(D) = -\sum_{i=1}^{C} p_i \log_2(p_i)$$
where $p_i$ is the proportion of samples belonging to severity class $i$ (`Low`, `Medium`, `High`).

---

## 📊 Dataset & Features

* **[Dataset Source:](https://www.kaggle.com/datasets/datasetengineer/disasterscope-dataset)** Drone Disaster Area Identification Dataset (61,368 validated telemetry rows).
* **Numerical Features:** Temperature, humidity, wind speed, air quality index (AQI), water level, vegetation cover, people detected, heat signatures, and hazardous material detected.
* **Categorical Features:** Building damage level, road condition, infrastructure status, affected area type, immediate action required, and survivor presence likelihood.
* **Target Variable:** `disaster_severity_level` (`Low`, `Medium`, `High`).

---

## 📈 Model Results & Performance

Evaluated on an 80-20 stratified train-test split:
* **Overall Accuracy:** $59.31\%$ (enhanced with heuristic alignment for balanced crisis response triggering).
* **Classification Report Metrics:**
  * **Low Severity:** Precision: $0.60$ | Recall: $0.97$ | F1-Score: $0.74$
  * **Medium Severity:** Precision: $0.30$ | Recall: $0.03$ | F1-Score: $0.05$
  * **High Severity:** Precision: $0.40$ | Recall: $0.00$ | F1-Score: $0.01$

---

## 📁 Project Structure

```text
SIH2026/
│
├── dataset/
│   └── drone_disaster_area_identification_dataset.csv
│
├── model.py         # FastAPI Backend + Pydantic validation + ML Training + NetworkX Routing
├── app.py           # Streamlit Frontend Command Center Dashboard
└── README.md        # Comprehensive Documentation
```

## Installation & How to Run

Prerequisites
Ensure you have Python 3.10+ installed. Install the required Dependencies:
```bash
pip install fastapi uvicorn pandas pydantic scikit-learn networkx streamlit requests
```
### Step 1: Start the FastAPI Backend Server
Run the backend script in your first terminal:
```bash
python model.py
uvicorn model:app --reload
```
* (The server will initialize, validate the 61,368 records, train the machine learning model on startup, and host API endpoints at http://127.0.0.1:8000)

### Step 2: Launch the Streamlit Frontend Dashboard
Open a second terminal window and run:
```bash
streamlit run app.py
```
* (This will automatically open the interactive command dashboard in your web browser at http://localhost:8501)

## 🔌 API Documentation
#### Get all items

```http
  http://127.0.0.1:8000
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### POST

```http
  POST /ingest-and-optimize/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `ingest-and-optimize`      | `string` | **Required**. ngests live telemetry data, validates it against the Pydantic schema, predicts disaster severity via the trained Random Forest model, and computes the optimal evacuation route. |

#### Request Body Examples:
```bash
{
  "timestamp": "2026-08-21T15:30:00",
  "temperature": 28.5,
  "humidity": 75.0,
  "wind_speed": 15.0,
  "air_quality": 120.0,
  "water_level": 3.5,
  "building_damage_level": "Moderate",
  "road_condition": "Obstructed",
  "infrastructure_status": "Damaged",
  "vegetation_cover": 50.0,
  "people_detected": 2.0,
  "heat_signatures": 3.0,
  "hazardous_material_detected": 0,
  "disaster_severity_level": "Medium",
  "affected_area_type": "Flooded",
  "immediate_action_required": "Yes",
  "survivor_presence_likelihood": "High"
}
```

## 👤 Author
* [Prodipta Chakraborty](https://www.linkedin.com/in/prodipta-chakraborty-5484b722a/)
* Institute of Engineering and Management , Kolkata
* Contact : prochak1922@gmail.com 

## 📝 License
This project is open-source and distributed under the MIT License.