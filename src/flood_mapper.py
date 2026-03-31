import pydeck as pdk
import pandas as pd
import numpy as np
import streamlit as st
import json
import os
import math
import rasterio
from rasterio.session import AWSSession
from collections import defaultdict

@st.cache_data
def load_precomputed_cities():
    """
    Lädt vorberechnete Städte (nur für Name, Koordinaten, Beschreibung).
    Diese Daten umgehen das API-Rate-Limit nicht mehr beim Laden (da wir AWS nutzen).
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
    Die Daten im JSON sind bereits als dichtes Grid (35x35) vorberechnet.
    """
    return None

def get_copernicus_tile_name(lat, lon):
    """
    Berechnet den Namen der Copernicus-Kachel (1x1 Grad) für gegebene Koordinaten.
    """
    lat_floor = math.floor(lat)
    lon_floor = math.floor(lon)
    
    n_or_s = "N" if lat_floor >= 0 else "S"
    e_or_w = "E" if lon_floor >= 0 else "W"
    
    lat_str = f"{abs(lat_floor):02d}"
    lon_str = f"{abs(lon_floor):03d}"
    
    # Format z.B.: Copernicus_DSM_COG_10_N53_00_E009_00_DEM
    tile = f"Copernicus_DSM_COG_10_{n_or_s}{lat_str}_00_{e_or_w}{lon_str}_00_DEM"
    return f"s3://copernicus-dem-30m/{tile}/{tile}.tif"

@st.cache_data(ttl=3600)
def get_real_elevation_data(center_lat, center_lon, grid_size=50, spread_km=10.0):
    """
    Lädt hochpräzise Höhendaten direkt vom AWS Copernicus DEM S3-Bucket.
    """
    lat_spread = (spread_km / 111.0) / 2
    lon_spread = (spread_km / (111.0 * math.cos(math.radians(center_lat)))) / 2
    
    lats = np.linspace(center_lat - lat_spread, center_lat + lat_spread, grid_size)
    lons = np.linspace(center_lon - lon_spread, center_lon + lon_spread, grid_size)
    
    # Rasterpunkte erstellen
    points = []
    for lt in lats:
        for ln in lons:
            points.append((ln, lt))
            
    # Punkte den jeweiligen 1x1 Grad S3-Kacheln zuordnen
    tiles = defaultdict(list)
    for ln, lt in points:
        tile_name = get_copernicus_tile_name(lt, ln)
        tiles[tile_name].append((ln, lt))
        
    results = {}
    
    # Verbindung zum öffentlichen Bucket aufbauen
    env = rasterio.Env(AWSSession(aws_unsigned=True), AWS_NO_SIGN_REQUEST="YES")
    with env:
        for tile_url, pts in tiles.items():
            try:
                with rasterio.open(tile_url) as src:
                    # Direkter, punktgenauer Zugriff auf Pixel ohne alles herunterzuladen
                    samples = list(src.sample(pts))
                    for pt, val in zip(pts, samples):
                        # Bei Fehlern/Wasser ist der Wert oft eine sehr große negative Zahl oder NaN
                        elev = float(val[0])
                        # Setze NoData/Wasser auf 0
                        if elev < -500 or math.isnan(elev):
                            elev = 0.0
                        results[pt] = elev
            except Exception as e:
                # Kachel existiert evtl. nicht (z.B. offener Ozean)
                for pt in pts:
                    results[pt] = 0.0

    grid_data = []
    
    # Wir speichern nun als Polygon, damit es als flächendeckende Grid-Karte gezeichnet wird!
    lat_step = lats[1] - lats[0]
    lon_step = lons[1] - lons[0]
    
    for lt in lats:
        for ln in lons:
            elev = results.get((ln, lt), 0.0)
            
            # Koordinaten des Rasters (Viereck) berechnen
            lon1, lon2 = ln - lon_step/2, ln + lon_step/2
            lat1, lat2 = lt - lat_step/2, lt + lat_step/2
            polygon = [
                [lon1, lat1],
                [lon2, lat1],
                [lon2, lat2],
                [lon1, lat2],
                [lon1, lat1]
            ]
            
            grid_data.append({
                'lat': lt,
                'lon': ln,
                'elevation': elev,
                'polygon': polygon
            })
            
    df = pd.DataFrame(grid_data)
    
    # Validierung
    if len(df) == 0:
        return generate_elevation_grid(center_lat, center_lon, grid_size, spread_km)
        
    return df

def generate_elevation_grid(center_lat, center_lon, grid_size=30, spread_km=5.0):
    """
    FALLBACK function: Generates a synthetic elevation grid when real data is unavailable.
    """
    lat_spread = (spread_km / 111.0) / 2
    lon_spread = (spread_km / (111.0 * math.cos(math.radians(center_lat)))) / 2
    
    lats = np.linspace(center_lat - lat_spread, center_lat + lat_spread, grid_size)
    lons = np.linspace(center_lon - lon_spread, center_lon + lon_spread, grid_size)
    
    lat_step = lats[1] - lats[0] if grid_size > 1 else 0.01
    lon_step = lons[1] - lons[0] if grid_size > 1 else 0.01
    
    grid_data = []
    
    for lat in lats:
        for lon in lons:
            dist_origin = np.sqrt((lat - center_lat)**2 + (lon - center_lon)**2)
            base_elevation = 5.0 + np.sin(lat * 80)*3 + np.cos(lon * 80)*3 + (dist_origin * 40)
            base_elevation = max(base_elevation, 0.5)
            
            lon1, lon2 = lon - lon_step/2, lon + lon_step/2
            lat1, lat2 = lat - lat_step/2, lat + lat_step/2
            polygon = [
                [lon1, lat1],
                [lon2, lat1],
                [lon2, lat2],
                [lon1, lat2],
                [lon1, lat1]
            ]
            
            grid_data.append({
                'lat': lat, 
                'lon': lon, 
                'elevation': float(base_elevation), 
                'polygon': polygon
            })
            
    return pd.DataFrame(grid_data)

def render_flood_map(lat, lon, sea_level_rise_m, city_name=None):
    """
    Renders a Pydeck PolygonLayer around the provided coordinates showing flood risk.
    """
    # Lade jetzt immer die Copernicus-Daten aus der AWS S3 Registry
    # spread_km auf 45.0 hochgesetzt, um eine 9-mal so große Fläche (3x3) abzubilden
    df_grid = get_real_elevation_data(lat, lon, grid_size=90, spread_km=45.0)
    
    # Calculate water depth and colors
    def get_color(elev, sea_level):
        diff = elev - sea_level
        # 🔴 ÜBERFLUTET: Höhe <= Meeresspiegel
        if diff <= 0:
            depth = abs(diff)
            # Blau-Gradient: Dunkler = Tiefer
            if depth > 5: return [8, 48, 107, 220]      # Sehr tief (Dunkelblau)
            elif depth > 2: return [33, 113, 181, 200]    # Mittel
            else: return [107, 174, 214, 180]             # Flachwasser (Hellblau)
            
        # 🟢 SICHER: Höhe > Meeresspiegel
        else:
            # Grün/Braun-Gradient basierend auf Höhe
            if diff < 2: return [116, 196, 118, 120]      # Sehr nah am Wasser, gefärdet
            elif diff < 10: return [49, 163, 84, 120]     # Sicher (Grün)
            elif diff < 50: return [166, 217, 106, 120]   # Hügelig
            else: return [217, 217, 217, 120]             # Hoch gelegen / Gebirge
            
    df_grid['color'] = df_grid['elevation'].apply(lambda x: get_color(x, sea_level_rise_m))
    
    # Überflutetes Volumen berechnen (reine Landfläche, bestehendes Meer wird ausgeschlossen)
    land_points = df_grid[df_grid['elevation'] > 0]
    if len(land_points) > 0:
        newly_flooded_points = len(land_points[land_points['elevation'] <= sea_level_rise_m])
        flood_ratio = (newly_flooded_points / len(land_points)) * 100
    else:
        flood_ratio = 0.0
        
    st.markdown(f"**🌊 Anteil überfluteter Landfläche (Radius 45km):** `{flood_ratio:.1f}%`")
    
    # Wir nutzen den PolygonLayer um eine geschlossene, realistische Fläche zu zeichnen.
    # extrude=True erlaubt es uns, die Erhebungen der Polygone als 3D Block darzustellen (wie Minecraft)
    layer = pdk.Layer(
        "PolygonLayer",
        data=df_grid,
        get_polygon="polygon",
        get_fill_color="color",
        get_elevation="elevation",
        elevation_scale=15,  # überhöht, um Topographie besser zu erkennen
        extruded=True,
        wireframe=False,
        pickable=True,
        auto_highlight=True
    )
    
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=10,
        pitch=45,
        bearing=0
    )
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Höhe:</b> {elevation} m über NN<br/><b>Lat/Lon:</b> {lat}, {lon}",
            "style": {"color": "white"}
        },
        map_provider="carto",
        map_style="light",
    )
    
    return r
