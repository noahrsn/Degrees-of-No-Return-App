import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

MODEL_DIR = Path('models')

class ClimateModels:
    def __init__(self):
        # Load scalar and models
        self.temp_model = joblib.load(MODEL_DIR / 'ridge_temperature.pkl')
        self.temp_scaler = joblib.load(MODEL_DIR / 'scaler_temperature.pkl')
        
        self.sea_model = joblib.load(MODEL_DIR / 'ridge_sea_level.pkl')
        self.sea_scaler = joblib.load(MODEL_DIR / 'scaler_sea_level.pkl')
        
        with open(MODEL_DIR / 'model_metadata.json', 'r') as f:
            self.metadata = json.load(f)
            
        self.ssp_co2_scenarios = self._generate_ssp_paths()
        
    def _generate_ssp_paths(self):
        # Basis CO2 2024 is ~420 ppm
        # Simplified projections paths until 2050
        years = np.arange(2024, 2051)
        return {
            'ssp1-1.9': {'co2': 420 + (years - 2024) * 1.5, 'desc': '🟢 SSP1-1.9 (Ambitioniert)'},
            'ssp2-4.5': {'co2': 420 + (years - 2024) * 2.5, 'desc': '🟡 SSP2-4.5 (Moderat)'},
            'ssp5-8.5': {'co2': 420 + (years - 2024) * 3.5, 'desc': '🔴 SSP5-8.5 (Weiter so)'}
        }
    
    def simulate_features_for_year(self, year, scenario):
        base_year = 2024
        co2_today = 420.0
        
        if year < base_year: year = base_year
        if year > 2050: year = 2050
        
        idx = year - base_year
        projected_co2 = self.ssp_co2_scenarios[scenario]['co2'][idx]
        
        # Simplified Feature building for Ridge Models matching the metadata
        co2_change = projected_co2 - co2_today
        co2_5yr = projected_co2 - (1.5 * 5) # mock
        
        # Sea Level Features: ["co2_deseason", "co2_5yr_mean", "co2_change"]
        sea_features = np.array([[projected_co2, co2_5yr, co2_change]])
        sea_scaled = self.sea_scaler.transform(sea_features)
        
        sea_pred_baseline = self.sea_model.predict(sea_scaled)[0]
        
        # Temp Features: ["co2_deseason", "co2_lag1", "co2_lag3", "co2_lag5", "co2_change", "co2_5yr_mean", "sea_level_cm"]
        temp_features = np.array([[projected_co2, projected_co2-2, projected_co2-6, projected_co2-10, co2_change, co2_5yr, sea_pred_baseline]])
        temp_scaled = self.temp_scaler.transform(temp_features)
        temp_pred_baseline = self.temp_model.predict(temp_scaled)[0]
        
        # Because we used normalized anomalies in C-Phase, we calibrate them to total actuals here (rough calibration for display).
        sea_level_rise_cm = (year - base_year) * (sea_pred_baseline * 0.1) # scale simulation
# Add Uncertainty based on Scenario (Higher emissions = Higher uncertainty)
        if scenario == 'ssp1-1.9': 
            sea_level_rise_cm += (year-base_year)*0.4    
            uncertainty_sea = 0.15 
            uncertainty_temp = 0.10
        elif scenario == 'ssp2-4.5': 
            sea_level_rise_cm += (year-base_year)*0.6  
            uncertainty_sea = 0.25 
            uncertainty_temp = 0.20
        else: 
            sea_level_rise_cm += (year-base_year)*0.9
            uncertainty_sea = 0.40 
            uncertainty_temp = 0.35

        # Temp calibration
        temp_increase = temp_pred_baseline * 0.05 + (year-base_year) * 0.03     
        if scenario == 'ssp5-8.5': temp_increase += (year-base_year) * 0.02     
        
        # Calculate derived Heat Days (Approximation)
        heat_days_base = 10
        heat_days = int(heat_days_base + (temp_increase * 15))
        
        # Ranges
        sea_min = max(0.0, sea_level_rise_cm * (1 - uncertainty_sea))
        sea_max = sea_level_rise_cm * (1 + uncertainty_sea)
        temp_min = max(0.0, temp_increase * (1 - uncertainty_temp))
        temp_max = temp_increase * (1 + uncertainty_temp)
        heat_days_min = max(0, int(heat_days_base + (temp_min * 15)))
        heat_days_max = int(heat_days_base + (temp_max * 15))

        return {
            'year': year,
            'scenario': scenario,
            'sea_level_rise_cm': max(0.0, sea_level_rise_cm),
            'sea_level_rise_cm_min': sea_min,
            'sea_level_rise_cm_max': sea_max,
            'temp_increase_c': max(0.0, temp_increase),
            'temp_increase_c_min': temp_min,
            'temp_increase_c_max': temp_max,
            'expected_heat_days': max(0, heat_days),
            'expected_heat_days_min': heat_days_min,
            'expected_heat_days_max': heat_days_max,
            'co2_ppm': projected_co2
        }

# Singleton for caching
GLOBAL_MODELS = None

def get_models():
    global GLOBAL_MODELS
    if GLOBAL_MODELS is None:
        GLOBAL_MODELS = ClimateModels()
    return GLOBAL_MODELS
