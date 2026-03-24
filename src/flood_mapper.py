import pydeck as pdk
import pandas as pd
import numpy as np
import requests
import streamlit as st
import time

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
                # Ensure we handle nulls correctly from the API!
                chunk_elevs = []
                for e in data.get('elevation', []):
                    if e is None:
                        chunk_elevs.append(0.0)
                    else:
                        chunk_elevs.append(float(e))
                # Pad if the API returned fewer items than requested
                while len(chunk_elevs) < len(chunk):
                    chunk_elevs.append(0.0)
                    
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
                        chunk_elevs = [e if e is not None else 0.0 for e in data.get('elevation', [0.0]*len(chunk))]
                        elevations.extend(chunk_elevs)
                    else:
                        print(f"Retry failed with {resp_retry.status_code}")
                        elevations.extend([0.0] * len(chunk))
                else:
                    elevations.extend([0.0] * len(chunk)) # fallback for chunk  

            # Schlafe kurz, um Rate Limit Error (429) von Open-Meteo zu verhindern
            time.sleep(0.5)

        # Build DataFrame
        grid_data = []
        for i, (lat, lon) in enumerate(coords):
            # Replace missing data or ocean artifacts with 0.0
            elev = elevations[i] if i < len(elevations) else 0.0
            if elev < -50: elev = 0.0 # Ocean surface
            
            grid_data.append({
                'lat': lat,
                'lon': lon,
                'elevation': float(elev),
                'geometry': [lon, lat]
            })
            
        return pd.DataFrame(grid_data)
        
    except Exception as e:
        st.warning(f"⚠️ API Fehler: {e}. Lade Fallback-Grid.")
        return generate_elevation_grid(center_lat, center_lon, grid_size, spread_km)

def generate_elevation_grid(center_lat, center_lon, grid_size=30, spread_km=5.0):
    # FALLBACK function 
    # ...existing code...
    lat_spread = (spread_km / 111.0) / 2
    lon_spread = (spread_km / (111.0 * np.cos(np.radians(center_lat)))) / 2
    
    lats = np.linspace(center_lat - lat_spread, center_lat + lat_spread, grid_size)
    lons = np.linspace(center_lon - lon_spread, center_lon + lon_spread, grid_size)
    
    grid_data = []
    
    for lat in lats:
        for lon in lons:
            dist_origin = np.sqrt((lat - center_lat)**2 + (lon - center_lon)**2)
            # Organic waves based on absolute coords
            base_elevation = 2.0 + np.sin(lat * 80)*2 + np.cos(lon * 80)*2 + (dist_origin * 60)
            grid_data.append({'lat': lat, 'lon': lon, 'elevation': float(base_elevation), 'geometry': [lon, lat]})
            
    return pd.DataFrame(grid_data)

def render_flood_map(lat, lon, sea_level_rise_m):
    """
    Renders a Pydeck ColumnLayer around the provided coordinates showing flood risk.
    """
    # Fetch TRUE data from Open-Meteo
    df_grid = get_real_elevation_data(lat, lon, grid_size=35, spread_km=15.0)
    
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
    
    # Pydeck Layer
    column_layer = pdk.Layer(
        "ColumnLayer",
        data=df_grid,
        get_position='[lon, lat]',
        get_elevation='elevation_display',
        elevation_scale=50,
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
