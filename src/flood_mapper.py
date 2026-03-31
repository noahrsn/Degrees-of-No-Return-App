import pydeck as pdk
import pandas as pd
import numpy as np
import requests
import streamlit as st
import time
import json
import os

@st.cache_data
def load_precomputed_cities():
    """
    Lädt vorberechnete Elevation-Daten für die wichtigsten deutschsprachigen Städte.
    Diese Daten umgehen das API-Rate-Limit.
    """
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'precomputed_cities.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Fehler beim Laden vorberechneter Städte: {e}")
        return {}

def get_precomputed_elevation_data(city_name):
    """
    Holt vorberechnete Elevation-Daten für eine Stadt.
    Generiert ein dichtes Grid basierend auf den gespeicherten Datenpunkten.
    Nutzt Inverse Distance Weighting (IDW) für realistische Interpolation.
    """
    cities = load_precomputed_cities()
    
    if city_name not in cities:
        return None
    
    city_data = cities[city_name]
    base_points = city_data['elevation_data']
    
    # Erweitere die Datenpunkte zu einem dichteren Grid
    center_lat = city_data['lat']
    center_lon = city_data['lon']
    
    grid_size = 35
    spread_km = 15.0
    
    lat_spread = (spread_km / 111.0) / 2
    lon_spread = (spread_km / (111.0 * np.cos(np.radians(center_lat)))) / 2
    
    lats = np.linspace(center_lat - lat_spread, center_lat + lat_spread, grid_size)
    lons = np.linspace(center_lon - lon_spread, center_lon + lon_spread, grid_size)
    
    grid_data = []
    
    # Inverse Distance Weighting (IDW) für realistische Interpolation
    for lat in lats:
        for lon in lons:
            # Berechne gewichteten Durchschnitt basierend auf Distanz zu allen Punkten
            total_weight = 0
            weighted_elevation = 0
            
            for point in base_points:
                # Distanz berechnen
                dist = np.sqrt((lat - point['lat'])**2 + (lon - point['lon'])**2)
                
                # Verhindere Division durch 0 (exakte Übereinstimmung)
                if dist < 0.0001:
                    weighted_elevation = point['elevation']
                    total_weight = 1
                    break
                
                # Inverse Distance Weighting (power=2)
                weight = 1.0 / (dist ** 2)
                weighted_elevation += point['elevation'] * weight
                total_weight += weight
            
            # Berechne finale Elevation
            if total_weight > 0:
                elev = weighted_elevation / total_weight
            else:
                elev = base_points[0]['elevation']  # Fallback
            
            # ✅ KEIN FILTER - Zeige ALLE Datenpunkte
            grid_data.append({
                'lat': lat,
                'lon': lon,
                'elevation': float(elev),
                'geometry': [lon, lat]
            })
    
    return pd.DataFrame(grid_data)

@st.cache_data(ttl=3600)
def get_real_elevation_data(center_lat, center_lon, grid_size=30, spread_km=8.0):
    """
    Fetches REAL elevation data using the Open-Meteo Free API.
    Builds a grid around the center point and fetches the true height above sea level.
    """
    # WE WILL ALLOW HIGH DENSITY AGAIN. BUT WITH BETTER SLEEP
    # We remove the "grid_size = min(grid_size, 15)" limitation
    
    lat_spread = (spread_km / 111.0) / 2
    lon_spread = (spread_km / (111.0 * np.cos(np.radians(center_lat)))) / 2
    
    lats = np.linspace(center_lat - lat_spread, center_lat + lat_spread, grid_size)
    lons = np.linspace(center_lon - lon_spread, center_lon + lon_spread, grid_size)
    
    # Create coordinate pairs
    coords = []
    for lat in lats:
        for lon in lons:
            coords.append((lat, lon))
            
    # Open-Meteo allows batches, max 100 per request. Using 50 to be safe on URL length.
    chunk_size = 50
    elevations = []
    
    try:
        for i in range(0, len(coords), chunk_size):
            chunk = coords[i:i + chunk_size]
            lats_str = ",".join(str(round(c[0], 5)) for c in chunk)
            lons_str = ",".join(str(round(c[1], 5)) for c in chunk)
            
            url = f"https://api.open-meteo.com/v1/elevation?latitude={lats_str}&longitude={lons_str}"
            resp = requests.get(url)
            
            if resp.status_code == 200:
                data = resp.json()
                # ✅ WICHTIG: None bedeutet meist Wasserfläche/Ozean -> als np.nan markieren
                chunk_elevs = []
                for e in data.get('elevation', []):
                    if e is None:
                        chunk_elevs.append(np.nan)  # Markiere als ungültig
                    else:
                        chunk_elevs.append(float(e))
                # Pad if the API returned fewer items than requested
                while len(chunk_elevs) < len(chunk):
                    chunk_elevs.append(np.nan)
                    
                elevations.extend(chunk_elevs)
            else:
                print(f"OM API Error {resp.status_code}: {resp.text}")
                # IF WE HIT RATE LIMIT, SLEEP LONGER AND RETRY ONCE
                if resp.status_code == 429:
                    print("Rate limit hit, sleeping for 3 seconds...")
                    time.sleep(3.0)
                    resp_retry = requests.get(url)
                    if resp_retry.status_code == 200:
                        data = resp_retry.json()
                        chunk_elevs = [e if e is not None else np.nan for e in data.get('elevation', [np.nan]*len(chunk))]
                        elevations.extend(chunk_elevs)
                    else:
                        print(f"Retry failed with {resp_retry.status_code}")
                        elevations.extend([np.nan] * len(chunk))
                else:
                    elevations.extend([np.nan] * len(chunk)) # fallback for chunk

            # Schlafe kurz, um Rate Limit Error (429) von Open-Meteo zu verhindern
            time.sleep(0.5)

        # Build DataFrame
        grid_data = []
        for i, (lat, lon) in enumerate(coords):
            elev = elevations[i] if i < len(elevations) else np.nan
            
            # ✅ Überspringe nur NaN-Werte (fehlende Daten)
            # Alle realen Höhenwerte werden angezeigt, auch negative!
            if np.isnan(elev):
                continue
            
            grid_data.append({
                'lat': lat,
                'lon': lon,
                'elevation': float(elev),
                'geometry': [lon, lat]
            })
            
        df = pd.DataFrame(grid_data)
        
        # Zusätzliche Sicherheit: Entferne verbleibende NaN-Zeilen
        df = df.dropna(subset=['elevation'])
        
        # ✅ VALIDIERUNG: Prüfe, ob genug Datenpunkte vorhanden sind
        if len(df) < 10:
            st.warning(f"⚠️ Nur {len(df)} gültige Höhenpunkte gefunden. Das Gebiet liegt möglicherweise überwiegend im Ozean oder Daten fehlen.")
            # Fallback für reine Ozeangebiete
            if len(df) == 0:
                return generate_elevation_grid(center_lat, center_lon, grid_size, spread_km)
        
        return df
        
    except Exception as e:
        st.warning(f"⚠️ API Fehler: {e}. Lade Fallback-Grid.")
        return generate_elevation_grid(center_lat, center_lon, grid_size, spread_km)

def generate_elevation_grid(center_lat, center_lon, grid_size=30, spread_km=5.0):
    """
    FALLBACK function: Generates a synthetic elevation grid when real data is unavailable.
    """
    lat_spread = (spread_km / 111.0) / 2
    lon_spread = (spread_km / (111.0 * np.cos(np.radians(center_lat)))) / 2
    
    lats = np.linspace(center_lat - lat_spread, center_lat + lat_spread, grid_size)
    lons = np.linspace(center_lon - lon_spread, center_lon + lon_spread, grid_size)
    
    grid_data = []
    
    for lat in lats:
        for lon in lons:
            dist_origin = np.sqrt((lat - center_lat)**2 + (lon - center_lon)**2)
            # Organic waves based on absolute coords - IMMER positiv halten für Land
            base_elevation = 5.0 + np.sin(lat * 80)*3 + np.cos(lon * 80)*3 + (dist_origin * 40)
            # ✅ Stelle sicher, dass synthetische Daten immer > 0 sind (kein Ozean simulieren)
            base_elevation = max(base_elevation, 0.5)
            grid_data.append({
                'lat': lat, 
                'lon': lon, 
                'elevation': float(base_elevation), 
                'geometry': [lon, lat]
            })
            
    return pd.DataFrame(grid_data)

def render_flood_map(lat, lon, sea_level_rise_m, city_name=None):
    """
    Renders a Pydeck ColumnLayer around the provided coordinates showing flood risk.
    If city_name is provided, uses precomputed data instead of API calls.
    """
    # Versuche zuerst vorberechnete Daten zu verwenden
    if city_name:
        df_grid = get_precomputed_elevation_data(city_name)
        if df_grid is not None and len(df_grid) > 0:
            st.info(f"✅ Verwende vorberechnete Daten für {city_name} (kein API-Call nötig)")
        else:
            # Fallback zu API wenn vorberechnete Daten fehlen
            df_grid = get_real_elevation_data(lat, lon, grid_size=35, spread_km=15.0)
    else:
        # Fetch TRUE data from Open-Meteo
        df_grid = get_real_elevation_data(lat, lon, grid_size=35, spread_km=15.0)
    
    # ✅ Entferne nur NaN-Werte, KEINE Höhenfilterung
    df_grid = df_grid.dropna(subset=['elevation'])
    
    # Prüfe auf leere Daten
    if len(df_grid) == 0:
        st.error("❌ Keine gültigen Höhendaten verfügbar. Bitte wähle eine andere Stadt.")
        return None
    
    # Calculate water depth and colors
    def get_color(elev, sea_level):
        diff = elev - sea_level
        # 🔴 ÜBERFLUTET: Höhe <= Meeresspiegel
        if diff <= 0:
            return [255, 0, 0, 140]  # Red transparenter
        # 🟠 BEDROHTE ZONE: 0 bis 1m über Meeresspiegel
        elif diff <= 1.0:
            return [255, 102, 0, 110]  # Orange
        # 🟡 GEFÄHRDET: 1 bis 3m über Meeresspiegel
        elif diff <= 3.0:
            return [255, 204, 0, 80]  # Yellow
        # 🟢 SICHER: > 3m
        else:
            return [102, 204, 51, 30]  # Green with low opacity
            
    df_grid['color'] = df_grid.apply(lambda row: get_color(row['elevation'], sea_level_rise_m), axis=1)
    df_grid['elevation_display'] = df_grid['elevation'].round(2)
    
    # ✅ FIX für negative Höhen + flache Gebiete
    # ColumnLayer kann keine negativen Höhen anzeigen
    # Für sehr flache Gebiete (z.B. Amsterdam): Nutze verstärkte Skalierung
    elevation_range = df_grid['elevation'].max() - df_grid['elevation'].min()
    
    if elevation_range < 5:  # Sehr flaches Gebiet (z.B. Amsterdam, Polder)
        # Nutze Abstand zum Minimum als Höhe (alle Punkte sichtbar)
        min_elev = df_grid['elevation'].min()
        df_grid['elevation_visual'] = (df_grid['elevation'] - min_elev + 0.5)
        elevation_scale = 100  # Stärkere Skalierung für flache Gebiete
    else:  # Normales Gebiet mit Variation
        # Nutze absolute Werte für negative Höhen
        df_grid['elevation_visual'] = df_grid['elevation'].apply(lambda x: max(x, 0.5) if x >= 0 else abs(x) + 0.5)
        elevation_scale = 50
    
    # Pydeck Layer
    column_layer = pdk.Layer(
        "ColumnLayer",
        data=df_grid,
        get_position='[lon, lat]',
        get_elevation='elevation_visual',  # ✅ Transformierte Werte
        elevation_scale=elevation_scale,    # ✅ Dynamische Skalierung
        radius=200,
        get_fill_color='color',
        pickable=True,
        auto_highlight=True,
    )
    
    # View State
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=11.5,
        pitch=45,
        bearing=0
    )
    
    # Map
    r = pdk.Deck(
        layers=[column_layer],
        initial_view_state=view_state,
        tooltip={"text": "Höhe ü. NN: {elevation_display}m"},
        map_provider="carto",
        map_style="light",
    )
    
    return r
