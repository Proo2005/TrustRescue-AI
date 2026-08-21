import pandas as pd
from model import DisasterRecordSchema  # assuming your code is in model.py

df = pd.read_csv("dataset/drone_disaster_area_identification_dataset.csv")
df.columns = df.columns.str.strip()

# Test the first row directly and print the exact error
try:
    row_dict = df.iloc[0].to_dict()
    print("First row data:", row_dict)
    DisasterRecordSchema.model_validate(row_dict)
except Exception as e:
    print("\nEXACT VALIDATION ERROR:\n", e)