import streamlit as st
from geopy.geocoders import Nominatim
import pydeck as pdk

from src.ml_pipelines import get_models
from src.flood_mapper import render_flood_map
from src.global_heat_mapper import render_global_heat_map

st.set_page_config(page_title="Degrees of No Return", layout="wide", page_icon="🌍")

@st.cache_resource
def get_geocoder():
    # user_agent is required by Nominatim
    return Nominatim(user_agent="degrees_of_no_return_app")

@st.cache_data
def geocode_city(city_name):
    geolocator = get_geocoder()
    try:
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude, location.address
        return None
    except Exception as e:
        return None

# Sidebar Content
st.sidebar.title("🌍 Degrees of No Return")
st.sidebar.markdown("### Einstellungen")

scenario = st.sidebar.selectbox(
    "IPCC Emissions-Szenario",
    ["ssp1-1.9", "ssp2-4.5", "ssp5-8.5"],
    format_func=lambda x: {
        "ssp1-1.9": "🟢 SSP1-1.9 (Ambitioniert, 1.5°C)",
        "ssp2-4.5": "🟡 SSP2-4.5 (Moderat)",
        "ssp5-8.5": "🔴 SSP5-8.5 (Weiter wie bisher)"
    }[x],
    index=2
)

target_year = st.sidebar.slider(
    "Prognose-Jahr:",
    min_value=2024,
    max_value=2050,
    value=2050,
    step=1
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Modell-Informationen:**
    - Modelle: Ridge Regression
    - Features: CO2 Lag, CO2 5yr mean
    - Quelle: C-Phase (trainierte Parameter)
    """
)

# Load ML Prediction
models = get_models()
predictions = models.simulate_features_for_year(target_year, scenario)

# Layout
st.title("Globale und Lokale Klimarisiken (2024 - 2050)")

tab1, tab2 = st.tabs(["🌊 Lokale Überflutung", "🌡️ Globale Heatmap"])

# TAB 1: Lokale Überflutung
with tab1:
    st.markdown("### Wähle eine beliebige Stadt, um das lokale Überflutungsrisiko zu simulieren")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        city_input = st.text_input("Stadt suchen:", "Hamburg")
        search_pressed = st.button("📍 Suchen & Zoomen")
        
        # We store lat/lon in session state to persist it
        if "lat" not in st.session_state:
            st.session_state.lat, st.session_state.lon, st.session_state.addr = geocode_city("Hamburg")
            
        if search_pressed:
            res = geocode_city(city_input)
            if res:
                st.session_state.lat, st.session_state.lon, st.session_state.addr = res
            else:
                st.error(f"Stadt '{city_input}' nicht gefunden. Bitte versuche einen anderen Namen.")
                
        st.success(f"**Gewählter Ort:**\n{st.session_state.addr}")
        
        st.markdown(f"#### 📊 KPI für {target_year}")
        st.metric("Meeresspiegelanstieg vs. 2024", f"+{predictions['sea_level_rise_cm']:.1f} cm")
        st.metric("Erwartete Hitzetage/Jahr", f"{predictions['expected_heat_days']}")
        
        st.markdown(
            """
            #### 🎨 Farb-Legende (Topographie vs Wasserstand)
            - 🔴 **ROT:** Überflutet (Höhe ≤ Meeresspiegel)
            - 🟠 **ORANGE:** Bedrohte Zone (0-1m über MS)
            - 🟡 **GELB:** Gefährdet (1-3m über MS)
            - 🟢 **GRÜN:** Sicher (>3m über MS)
            
            *🌍 Disclaimer: Das Höhenmodell (DEM) ist hier für jede Koordinate als interaktive Mock-Topographie für das Pydeck-Overlay implementiert. Es berechnet den lokalen Wasserstand.*
            """
        )

    with col2:
        # Convert map cm to meters
        slr_m = predictions['sea_level_rise_cm'] / 100.0
        deck = render_flood_map(st.session_state.lat, st.session_state.lon, slr_m)
        st.pydeck_chart(deck)


# TAB 2: Globale Heatmap
with tab2:
    st.markdown("### Globale Temperaturentwicklung: Hitzetage")
    st.markdown(f"**Globale Temperaturerhöhung (vs Baseline):** +{predictions['temp_increase_c']:.2f} °C")
    
    global_deck = render_global_heat_map(predictions['temp_increase_c'])
    st.pydeck_chart(global_deck)
    
    st.markdown("**(Dunkelrot/Violett = Kritische Hitzebelastung / Kipppunkte, Hellgelb = Angenehm)**")
