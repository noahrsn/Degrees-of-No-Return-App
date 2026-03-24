import pydeck as pdk
import pandas as pd
import numpy as np

def generate_global_heat_grid(global_temp_increase_c):
    """
    Simulates a grid for the whole world showing heat days.
    """
    # Create coarse global grid, avoiding extreme poles for better visual
    lats = np.linspace(-55, 65, 45)
    lons = np.linspace(-180, 180, 90)
    
    data = []
    for lat in lats:
        for lon in lons:
            # Heat days are higher near the equator
            base_heat_days = base_heat_days = max(0, 80 - abs(lat) * 1.5)
            
            # Add amplification based on global temp increase
            # Equator suffers more from global increase
            amplification = 1.0 + (abs(lat) / 90.0)
            projected_days = base_heat_days + (global_temp_increase_c * 15 * amplification)
            
            # Noise
            projected_days += np.random.normal(0, 5)
            
            data.append({
                'lat': lat,
                'lon': lon,
                'heat_days': max(0, int(projected_days))
            })
            
    df = pd.DataFrame(data)
    
    def get_heat_color(days):
        # Weiche Interpolation anstatt harter Grenzen für einen echten Gradienten-Look
        # Start: Hellgelb [255, 255, 178] -> Ende: Dunkelrot/Violett [128, 0, 38]
        if days < 0: days = 0
        
        # Color stops:
        # 0:   [255, 255, 178] (Hellgelb)
        # 30:  [254, 204, 92]  (Gelb-Orange)
        # 60:  [253, 141, 60]  (Orange)
        # 90:  [240, 59, 32]   (Rot)
        # 120: [128, 0, 38]    (Tiefviolett)
        
        opacity = 150 # feste mittlere transparenz
        
        if days <= 30:
            pct = days / 30.0
            r = int(255 - pct * (255 - 254))
            g = int(255 - pct * (255 - 204))
            b = int(178 - pct * (178 - 92))
            return [r, g, b, opacity]
        elif days <= 60:
            pct = (days - 30) / 30.0
            r = int(254 - pct * (254 - 253))
            g = int(204 - pct * (204 - 141))
            b = int(92 - pct * (92 - 60))
            return [r, g, b, opacity]
        elif days <= 90:
            pct = (days - 60) / 30.0
            r = int(253 - pct * (253 - 240))
            g = int(141 - pct * (141 - 59))
            b = int(60 - pct * (60 - 32))
            return [r, g, b, opacity]
        else:
            pct = min(1.0, (days - 90) / 30.0)
            r = int(240 - pct * (240 - 128))
            g = int(59 - pct * (59 - 0))
            b = int(32 - pct * (32 - 38))
            return [r, g, b, opacity]
    df['color'] = df['heat_days'].apply(get_heat_color)
    
    # Calculate a normalized weight for the heatmap intensity
    df['weight'] = df['heat_days'] / df['heat_days'].max()
    
    return df

def render_global_heat_map(global_temp_increase_c):
    df_heat = generate_global_heat_grid(global_temp_increase_c)
    
    # Use ColumnLayer flattened for a beautiful raster/pixel grid look
    layer = pdk.Layer(
        "ColumnLayer",
        data=df_heat,
        get_position=["lon", "lat"],
        get_fill_color="color",
        radius=250000, # 250km breite Pixel
        elevation_scale=0, # Komplett flach, wie eine 2D Karte
        get_elevation=0,
        pickable=True,
    )
    
    view_state = pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1,
        pitch=0,
        bearing=0
    )
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Geplante Hitzetage: {heat_days}"},
        map_provider="carto",
        map_style="light",
    )
    
    return r
