import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder

def run_model_evaluation():
    csv_path = "dataset/drone_disaster_area_identification_dataset.csv"
    
    print("Loading dataset for evaluation...")
    df = pd.read_csv(csv_path)
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

    print("Training Random Forest Classifier for evaluation...")
    clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Evaluation Complete!")
    print(f"Overall Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=encoder.classes_))

    # --- 1. Plot & Save Confusion Matrix ---
    cm = confusion_matrix(y_test, y_pred)
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
                xticklabels=encoder.classes_, 
                yticklabels=encoder.classes_, ax=ax)
    
    ax.set_title('TrustRescue AI - Severity Classification Confusion Matrix', fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel('Predicted Severity Level', fontsize=10, labelpad=10)
    ax.set_ylabel('Actual Severity Level', fontsize=10, labelpad=10)
    
    plt.tight_layout()
    
    # Save the figure to disk
    plt.savefig('confusion_matrix_result.png', dpi=300, facecolor='#0f172a', edgecolor='none')
    print("Saved evaluation plot as: confusion_matrix_result.png")
    
    # Render and display the plot window on screen
    plt.show()

if __name__ == "__main__":
    run_model_evaluation()