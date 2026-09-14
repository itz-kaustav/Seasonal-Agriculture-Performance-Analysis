import os
import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Load trained pipeline
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), 'model', 'crop_yield_model.pkl'
)
model = joblib.load(MODEL_PATH)


def parse_float(val, default=None):
    """Safely parse float values, handling empty strings and invalid inputs."""
    if val is None or str(val).strip() == '':
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Read inputs (supports both AJAX JSON and classic HTML Form POST)
        data = request.get_json() if request.is_json else request.form

        crop = data.get('crop')
        season = data.get('season')
        irrigation = data.get('irrigation_method')
        state = data.get('state', 'Maharashtra')

        # Validate that dropdowns were selected and not left on the default "Select" option
        if not crop or not season or not irrigation:
            raise ValueError("Please select Crop Variety, Cropping Season, and Irrigation System.")

        # Parse and validate farm area
        area = parse_float(data.get('farm_area'))
        if area is None or area <= 0:
            raise ValueError("Please enter a valid cultivated land area (greater than 0).")

        # Environmental & Soil parameters with sensible agronomic defaults
        rainfall = parse_float(data.get('rainfall'), 600.0)
        temp = parse_float(data.get('temp'), 27.0)
        humidity = parse_float(data.get('humidity'), 65.0)
        sunlight = parse_float(data.get('sunlight'), 7.5)
        soil_ph = parse_float(data.get('soil_ph'), 6.8)
        soil_moisture = parse_float(data.get('soil_moisture'), 26.0)
        nitrogen = parse_float(data.get('nitrogen'), 120.0)
        phosphorus = parse_float(data.get('phosphorus'), 58.0)
        potassium = parse_float(data.get('potassium'), 105.0)
        fertilizer = parse_float(data.get('fertilizer'), 185.0)
        pesticide = parse_float(data.get('pesticide'), 5.0)
        seed_score = parse_float(data.get('seed_score'), 0.85)
        water_used = parse_float(data.get('water_used'), 4500.0)
        pest_risk = parse_float(data.get('pest_risk'), 45.0)

        # Construct feature DataFrame matching pipeline input schema
        input_df = pd.DataFrame([
            {
                'Season': season,
                'Crop': crop,
                'State': state,
                'Irrigation_Method': irrigation,
                'Farm_Area_Hectares': area,
                'Rainfall_mm': rainfall,
                'Avg_Temperature_C': temp,
                'Humidity_pct': humidity,
                'Sunlight_Hours_Day': sunlight,
                'Soil_pH': soil_ph,
                'Soil_Moisture_pct': soil_moisture,
                'Nitrogen_kg_ha': nitrogen,
                'Phosphorus_kg_ha': phosphorus,
                'Potassium_kg_ha': potassium,
                'Fertilizer_kg_ha': fertilizer,
                'Pesticide_Litre_ha': pesticide,
                'Seed_Quality_Score': seed_score,
                'Water_Used_m3': water_used,
                'Disease_Pest_Risk_pct': pest_risk,
            }
        ])

        # Predict yield (Tonnes per Hectare)
        pred_yield = float(model.predict(input_df)[0])
        pred_yield = max(0.0, round(pred_yield, 2))
        total_production = round(pred_yield * area, 2)

        # Initialize actionable advisory tips
        insights = []

        # 1. WATER ADVICE
        if season == "Zaid":
            insights.append("💧 Water: It is very hot — water your field early in the morning or in the evening to avoid drying.")
        elif season == "Kharif":
            insights.append("💧 Water: Heavy rain expected — make sure excess rainwater drains out so roots do not rot.")
        elif irrigation == "Flood":
            insights.append("💧 Water: Open flooding wastes water and fertilizer — shift to drip or sprinkler pipes if possible.")
        elif irrigation == "Rainfed":
            insights.append("💧 Water: Field runs on rainwater — spread dry leaves or straw (mulch) on the ground to save soil moisture.")
        elif irrigation == "Drip":
            insights.append("💧 Water: Drip system running — wash the black filters once a week so drippers don't get choked with sand.")
        else:
            insights.append("💧 Water: Give light watering at regular intervals whenever topsoil feels dry.")

        # 2. PEST & INSECT CONTROL
        if pest_risk > 55:
            insights.append("🐛 Pests: High insect danger — spray recommended pest medicine or neem oil (5 ml per liter water) right away.")
        elif pest_risk > 40:
            insights.append("🐛 Pests: Medium risk — check the underside of the leaves twice a week for insects or egg clusters.")
        else:
            insights.append("🐛 Pests: Crop is safe — just pull out wild grass and weeds from the field borders.")

        # 3. SOIL & MANURE
        if soil_ph < 6.0:
            insights.append(f"🌱 Soil: Soil is too sour/acidic (pH {soil_ph}) — mix agricultural lime (Chuna) before next sowing to sweeten the ground.")
        elif soil_ph > 7.5:
            insights.append(f"🌱 Soil: Soil is hard/alkaline (pH {soil_ph}) — add desi cow dung manure or gypsum to soften it up.")
        else:
            insights.append(f"🌱 Soil: Soil condition is healthy (pH {soil_ph}) — perfect for growing {crop}.")

        # 4. PRACTICAL CROP TIPS
        crop_tips = {
            "Rice": "🌾 Crop Tip: Keep 2 inches of standing water in the field until grains form fully.",
            "Wheat": "🌾 Crop Tip: Give a solid watering 20–25 days after sowing (first root stage) to get big, heavy grains.",
            "Cotton": "🌾 Crop Tip: Cut down white urea fertilizer once flowers appear, otherwise flowers and buds will drop.",
            "Sugarcane": "🌾 Crop Tip: Pile loose soil high around the cane base so heavy winds don't knock the crop down.",
            "Chilli": "🌾 Crop Tip: Do not let water sit in the rows — standing water causes leaf curl and yellow leaves.",
            "Maize": "🌾 Crop Tip: Never let the field go thirsty when the tassels (flowers) and cobs are coming out.",
            "Pulses": "🌾 Crop Tip: Do not add extra nitrogen fertilizer (urea) — pulse roots make their own food.",
            "Groundnut": "🌾 Crop Tip: Keep the soil soft and loose so underground nut pegs can easily drill into the ground.",
        }
        insights.append(
            crop_tips.get(crop, f"🌾 Crop Tip: Keep the field weed-free and follow standard local package practices for {crop}.")
        )

        # 5. HARVEST PREPARATION
        insights.append(
            f"📦 Harvest & Storage: You can expect around {total_production} tonnes — clean your storage shed and arrange dry gunny bags now."
        )

        if request.is_json:
            return jsonify({
                'success': True,
                'yield': pred_yield,
                'total_production': total_production,
                'recommendations': insights,
            })

        return render_template(
            'index.html',
            selected_crop=crop,
            selected_season=season,
            selected_irrigation=irrigation,
            selected_area=area,
            pred_yield=pred_yield,
            total_production=total_production,
            recommendations=insights,
        )

    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        return render_template(
            'index.html',
            selected_crop=request.form.get('crop'),
            selected_season=request.form.get('season'),
            selected_irrigation=request.form.get('irrigation_method'),
            selected_area=request.form.get('farm_area'),
            recommendations=[f"⚠️ {str(e)}"]
        )


if __name__ == '__main__':
    app.run(debug=True, port=5000)