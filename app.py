import streamlit as st
from geopy.geocoders import Nominatim

from src.ml_pipelines import get_models
from src.flood_mapper import render_flood_map, load_precomputed_cities
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
    st.markdown("### Wähle eine Stadt, um das lokale Überflutungsrisiko zu simulieren")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Lade vorberechnete Städte
        precomputed_cities = load_precomputed_cities()
        city_names = list(precomputed_cities.keys())
        
        st.markdown("#### 🏙️ Schnellauswahl (ohne API-Limit)")
        selected_city = st.selectbox(
            "Vorberechnete Städte:",
            options=[""] + city_names,
            format_func=lambda x: "-- Bitte wählen --" if x == "" else f"{x} - {precomputed_cities[x]['description']}" if x else ""
        )
        
        st.markdown("---")
        st.markdown("#### 🔍 Freie Suche (API-begrenzt)")
        city_input = st.text_input("Andere Stadt suchen:", placeholder="z.B. Berlin")
        search_pressed = st.button("📍 Suchen & Zoomen")
        
        # We store lat/lon/city in session state to persist it
        if "lat" not in st.session_state:
            # Standard: Hamburg
            st.session_state.lat = precomputed_cities["Hamburg"]["lat"]
            st.session_state.lon = precomputed_cities["Hamburg"]["lon"]
            st.session_state.addr = "Hamburg, Deutschland"
            st.session_state.city_name = "Hamburg"
            
        # Dropdown-Auswahl hat Priorität
        if selected_city and selected_city != "":
            city_data = precomputed_cities[selected_city]
            st.session_state.lat = city_data["lat"]
            st.session_state.lon = city_data["lon"]
            st.session_state.addr = f"{selected_city}, {city_data['description']}"
            st.session_state.city_name = selected_city
            
        # Suche nur wenn explizit gedrückt
        elif search_pressed and city_input:
            res = geocode_city(city_input)
            if res:
                st.session_state.lat, st.session_state.lon, st.session_state.addr = res
                st.session_state.city_name = None  # Keine vorberechneten Daten
            else:
                st.error(f"Stadt '{city_input}' nicht gefunden. Bitte versuche einen anderen Namen.")
                
        st.success(f"**Gewählter Ort:**\n{st.session_state.addr}")
        
        # Cache-Clear Button für Debug-Zwecke
        st.markdown("---")
        if st.button("🔄 Cache leeren"):
            st.cache_data.clear()
            st.success("✅ Cache geleert! Lade Seite neu (F5).")
        
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
            
            *🌍 Disclaimer: Das Höhenmodell basiert auf Open-Meteo Elevation API. 
            Alle Höhendaten werden ohne Filterung angezeigt. 
            Negative Werte zeigen Gebiete unter Meeresspiegel (z.B. Polder, Häfen, Kanäle).*
            """
        )

    with col2:
        # Convert map cm to meters
        slr_m = predictions['sea_level_rise_cm'] / 100.0
        
        # Nutze city_name wenn verfügbar (vorberechnete Daten)
        city_name = st.session_state.get('city_name', None)
        deck = render_flood_map(st.session_state.lat, st.session_state.lon, slr_m, city_name=city_name)
        
        if deck is not None:
            st.pydeck_chart(deck)
        else:
            st.warning("⚠️ Keine Kartendaten verfügbar. Bitte versuche eine andere Stadt.")


# TAB 2: Globale Heatmap
with tab2:
    st.markdown("### Globale Temperaturentwicklung: Hitzetage")
    st.markdown(f"**Globale Temperaturerhöhung (vs Baseline):** +{predictions['temp_increase_c']:.2f} °C")

    global_deck = render_global_heat_map(predictions['temp_increase_c'])
    st.pydeck_chart(global_deck)
    
    st.markdown("**(Dunkelrot/Violett = Kritische Hitzebelastung / Kipppunkte, Hellgelb = Angenehm)**")
