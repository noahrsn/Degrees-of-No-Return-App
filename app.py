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
st.sidebar.markdown(
    """
    Willkommen beim interaktiven **Klimarisiko-Dashboard**. 
    Simuliere die Zukunft bis 2050 und betrachte die Folgen verschiedener Emissionspfade.
    """
)
st.sidebar.markdown("### ⚙️ Einstellungen", help="Wähle das Klimaszenario und das Zieljahr aus.")

scenario = st.sidebar.radio(
    "IPCC Emissions-Szenario",
    ["ssp1-1.9", "ssp2-4.5", "ssp5-8.5"],
    format_func=lambda x: {
        "ssp1-1.9": "🟢 SSP1-1.9 (Klimaziel, ~1.5°C)",
        "ssp2-4.5": "🟡 SSP2-4.5 (Moderat, ~2.5°C)",
        "ssp5-8.5": "🔴 SSP5-8.5 (Weiter-wie-bisher, >4°C)"
    }[x],
    index=2,
    help="Wechsle hier zwischen den SSP-Pfaden des Weltklimarats: Vom realistischen 'Weiter-wie-bisher' (SSP5-8.5) bis hin zu einem sehr ambitionierten Klimaziel (SSP1-1.9)."
)

target_year = st.sidebar.slider(
    "Zeitstrahl (Jahr):",
    min_value=2024,
    max_value=2050,
    value=2050,
    step=1,
    help="Navigiere visuell in die Zukunft. Alle Karten, Kennzahlen und Berechnungen werden für das gewählte Jahr dynamisch aktualisiert."
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Modell-Informationen:**
    - Modelle: Zeitreihenanalyse via Ridge Regression
    - Topografie: Copernicus DEM S3-Registry (30m)
    - Validiert für kommunale Stadtplaner & Versicherungsanalysten.
    """
)

# Load ML Prediction
models = get_models()
predictions = models.simulate_features_for_year(target_year, scenario)

# Layout
st.title("Globale und Lokale Klimarisiken (2024 - 2050)")

# --- Schlüsselkennzahlen-Panel ---
st.markdown("### 📊 Schlüsselkennzahlen (Prognose für das Jahr **{}**)".format(target_year))
st.info("Diese Metriken zeigen die erwarteten Auswirkungen des gewählten Szenarios im Vergleich zur Gegenwart (Basisjahr 2024).", icon="ℹ️")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        label="🌡️ Durchschnittliche Temperaturänderung", 
        value=f"+{predictions['temp_increase_c']:.2f} °C", 
        delta=f"Schwankungsbreite: +{predictions['temp_increase_c_min']:.2f} bis +{predictions['temp_increase_c_max']:.2f} °C",
        delta_color="off",
        help="Weltweiter durchschnittlicher Temperaturanstieg gegenüber dem Basisjahr 2024 basierend auf den CO2-Projektionen des Szenarios."
    )
    
with kpi2:
    st.metric(
        label="🔥 Hitzetage / Jahr (Äquator/Lokal)", 
        value=f"~{predictions['expected_heat_days']} Tage", 
        delta=f"95% KI: {predictions['expected_heat_days_min']} - {predictions['expected_heat_days_max']} Tage",
        delta_color="off",
        help="Erwartete Anzahl von extremen Hitzetagen. Hinweis: Lokale städtische Versiegelung (Hitzeinseleffekt) kann diese Gesamtzahl lokal nochmal um 20-30% erhöhen."
    )

with kpi3:
    st.metric(
        label="🌊 Globaler Meeresspiegel", 
        value=f"+{predictions['sea_level_rise_cm']:.1f} cm", 
        delta=f"KI: +{predictions['sea_level_rise_cm_min']:.1f} bis +{predictions['sea_level_rise_cm_max']:.1f} cm",
        delta_color="off",
        help="Erwarteter Netto-Anstieg ab 2024. Unsicherheiten (Spanne) beinhalten das potenzielle Kippen und schnelle Abschmelzen von Eisschilden."
    )

st.markdown("---")

tab1, tab2 = st.tabs(["🌊 Lokale Überflutung (Detailanalyse)", "🌡️ Globale Temperaturentwicklung"])    

# TAB 1: Lokale Überflutung
with tab1:
    st.markdown("### Analysiere lokale Überflutungsrisiken nach Straßenzug")
    st.markdown("Wähle eine Stadt oder Ortschaft, um eine hochauflösende 3D-Simulation der Topografie (Copernicus DEM) in Bezug auf den ansteigenden Meeresspiegel zu berechnen.")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Lade vorberechnete Städte
        precomputed_cities = load_precomputed_cities()
        city_names = list(precomputed_cities.keys())

        st.markdown("#### 🏙️ Direktauswahl Städte")
        selected_city = st.selectbox(
            "Auswahl Liste:",
            options=[""] + city_names,
            format_func=lambda x: "-- Bitte wählen --" if x == "" else f"{x} - {precomputed_cities[x]['description']}" if x else "",
            help="Häufig betroffene europäische Städte."
        )

        st.markdown("---")
        st.markdown("#### 🔍 Eigene Region Suchen")
        city_input = st.text_input("Name eines Ortes eingeben:", placeholder="z.B. Sylt, New York, Tokio")
        search_pressed = st.button("📍 Geokodieren & Analysieren")

        # Session State Logik
        if "lat" not in st.session_state:
            st.session_state.lat = precomputed_cities["Hamburg"]["lat"]
            st.session_state.lon = precomputed_cities["Hamburg"]["lon"]
            st.session_state.addr = "Hamburg, Deutschland"
            st.session_state.city_name = "Hamburg"

        if selected_city and selected_city != "":
            city_data = precomputed_cities[selected_city]
            st.session_state.lat = city_data["lat"]
            st.session_state.lon = city_data["lon"]
            st.session_state.addr = f"{selected_city}, {city_data['description']}"
            st.session_state.city_name = selected_city

        elif search_pressed and city_input:
            res = geocode_city(city_input)
            if res:
                st.session_state.lat, st.session_state.lon, st.session_state.addr = res
                st.session_state.city_name = None  
            else:
                st.error(f"Stadt '{city_input}' nicht gefunden. Bitte prüfe die Rechtschreibung.")

        st.success(f"**Fokus-Bereich:**\n{st.session_state.addr}", icon="📍")

        st.markdown("#### 🎨 Lesehilfe Karte")
        st.markdown(
            """
            - 🔵 **Blau (Wasser/Überflutet):** Land unter dem Meeresspiegel-Niveau.
            - 🟢/🟤 **Grün/Braun:** Land, das sicher über Wasser liegt.
            
            *Wir visualisieren statische Küsten-Übertritte.* Binnenhochwasser durch extreme temporäre Starkregenereignisse können hier abweichen.
            """
        )
        
        # Disclaimer Tooltip
        with st.expander("⚠️ Wichtiger Risiko-Haftungsausschluss"):
            st.write("""
            Diese Daten basieren auf 30-Meter Kacheln (Copernicus DEM). Auch wenn die Karte Gebäude erfasst, 
            sind **parzellengenaue Aussagen** aufgrund von lokalen Flutschutzanlagen 
            (Deiche, Dämme), die im Satellitenbild ggf. nicht die richtige Höhe aufweisen, nur als erste Risiko-Indikation zu verstehen.
            """)

    with col2:
        # Convert map cm to meters
        slr_m = predictions['sea_level_rise_cm'] / 100.0

        with st.spinner("🌍 Lade topografische 3D-Kacheln direkt von der ESA/Copernicus S3 Registry... das kann beim ersten Mal wenige Sekunden dauern."):
            city_name = st.session_state.get('city_name', None)
            deck = render_flood_map(st.session_state.lat, st.session_state.lon, slr_m, city_name=city_name)

        if deck is not None:
            st.pydeck_chart(deck)
        else:
            st.warning("⚠️ Es liegen für diese Region keine Ozean/Küstendaten in der Cloud vor.")

# TAB 2: Globale Heatmap
with tab2:
    st.markdown("### 🌡️ Weltweite Verschiebung von Hitze-Perioden")
    st.markdown(
        """
        Die folgende Karte visualisiert die Verteilung von extremen Hitzetagen weltweit.
        Rot/Violett markierte Flächen zeigen Gebiete, in denen die thermale Belastung für Infrastruktur und Landwirtschaft existenzbedrohend werden kann.
        """
    )
    
    global_deck = render_global_heat_map(predictions['temp_increase_c'])        
    st.pydeck_chart(global_deck)
    
    st.caption("*Farbverlauf: Hellgelb (0-30 Hitzetage), Orange (30-60 Tage), Rot (60-90 Tage), Tiefviolett (über 90 kritische Tage/Jahr)*")
