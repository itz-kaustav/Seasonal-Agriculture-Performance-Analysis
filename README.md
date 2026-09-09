# Seasonal Agriculture Performance Analysis

An end-to-end data analytics and machine learning pipeline evaluating the impact of seasonal variations on agricultural outcomes, resource consumption, and farm-level profitability across India.

---

## 📌 Project Overview

Agricultural productivity varies widely across seasons due to changing meteorological conditions, farming techniques, and input allocations. This project analyzes agricultural field data across the three primary Indian crop cycles—**Kharif**, **Rabi**, and **Zaid**—to uncover patterns in input efficiency, environmental dynamics, and net margins, while deploying predictive machine learning models to forecast per-hectare yield (`Yield_Tonnes_Ha`).

---

## 🎯 Key Objectives

- **Exploratory Data Analysis (EDA):** Identify seasonal trends in precipitation, temperature, humidity, and sunlight hours.
- **Resource Management:** Evaluate water efficiency, pesticide usage, and fertilizer distribution across crop types and irrigation methods.
- **Economic Viability:** Perform cost-revenue break-even analyses and examine crop-wise profitability across seasons.
- **Predictive Modeling:** Train and evaluate regression models (Linear Regression, Ridge, Random Forest, and Gradient Boosting) to forecast crop yield.

---

## 📊 Key Findings

| Metric | Kharif (Monsoon) | Rabi (Winter) | Zaid (Summer) |
| :--- | :--- | :--- | :--- |
| **Mean Rainfall** | ~848.7 mm | ~437.9 mm | ~304.3 mm |
| **Mean Temperature** | 28.5°C | 23.5°C | 31.1°C |
| **Average Yield** | 5.64 t/ha | 5.08 t/ha | 4.67 t/ha |
| **Disease/Pest Risk** | 54.5% (High) | 40.5% | 38.2% |
| **Net Mean Profit** | +₹1,79,367 | +₹88,197 | -₹26,592 |

- **Kharif** delivers the highest yield and overall profitability due to natural monsoon rainfall, but requires strict pest management due to high ambient humidity.
- **Zaid** suffers from thermal stress (>31°C) and higher irrigation energy costs, requiring precision drip irrigation to prevent negative profit margins.
- **Top Yield Drivers:** Crop type (particularly high-biomass crops like Sugarcane), optimal soil pH (6.2–7.2), and rainfall volume.

---

## 🤖 Model Performance Benchmark

Models evaluated on an 80/20 train-test split:

| Model | $R^2$ Score | RMSE | MAE |
| :--- | :---: | :---: | :---: |
| **Linear Regression** | 0.8412 | 4.95 | 1.95 |
| **Ridge Regression** | 0.8409 | 4.95 | 1.95 |
| **Random Forest Regressor** | 0.9560 | 2.61 | 0.75 |
| **Gradient Boosting Regressor (Best)** | **0.9702** | **2.14** | **0.62** |

---

## 🛠️ Tech Stack & Libraries

- **Language:** Python 3.10+
- **Data Manipulation:** `pandas`, `numpy`
- **Visualization:** `matplotlib`, `seaborn`
- **Machine Learning:** `scikit-learn` (Pipelines, ColumnTransformer, GradientBoostingRegressor)

---

## 📂 Repository Structure

```text
├── data/
│   └── seasonal_agriculture_performance_dataset.csv
├── notebooks/
│   └── Seasonal_Agriculture_Performance_Analysis.ipynb
├── plots/
│   ├── fig1_environmental_variations.png
│   ├── fig2_crop_and_yield_analysis.png
│   ├── fig3_resource_usage.png
│   ├── fig4_economic_analysis.png
│   └── fig5_heatmap_and_diagnostics.png
├── requirements.txt
└── README.md
