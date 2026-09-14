import os
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

data_path = os.path.join(
    os.path.dirname(__file__),
    '..',
    'seasonal_agriculture_performance_dataset.csv',
)
df = pd.read_csv(data_path)

df_clean = df.dropna(subset=['Yield_Tonnes_Ha']).copy()
df_clean['Rainfall_mm'] = df_clean['Rainfall_mm'].fillna(
    df_clean['Rainfall_mm'].median()
)
df_clean['Soil_Moisture_pct'] = df_clean['Soil_Moisture_pct'].fillna(
    df_clean['Soil_Moisture_pct'].median()
)

cat_cols = ['Season', 'Crop', 'State', 'Irrigation_Method']
num_cols = [
    'Farm_Area_Hectares',
    'Rainfall_mm',
    'Avg_Temperature_C',
    'Humidity_pct',
    'Sunlight_Hours_Day',
    'Soil_pH',
    'Soil_Moisture_pct',
    'Nitrogen_kg_ha',
    'Phosphorus_kg_ha',
    'Potassium_kg_ha',
    'Fertilizer_kg_ha',
    'Pesticide_Litre_ha',
    'Seed_Quality_Score',
    'Water_Used_m3',
    'Disease_Pest_Risk_pct',
]

X = df_clean[cat_cols + num_cols]
y = df_clean['Yield_Tonnes_Ha']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_cols),
    ]
)

pipeline = Pipeline(
    [
        ('prep', preprocessor),
        (
            'reg',
            GradientBoostingRegressor(
                n_estimators=100, random_state=42, max_depth=5
            ),
        ),
    ]
)

pipeline.fit(X, y)

model_path = os.path.join(os.path.dirname(__file__), 'crop_yield_model.pkl')
joblib.dump(pipeline, model_path)
print(f"Trained model successfully saved to {model_path}")
