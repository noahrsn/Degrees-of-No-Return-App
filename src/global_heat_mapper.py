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

    lat_step = (65 - -55) / (45 - 1)
    lon_step = (180 - -180) / (90 - 1)

    data = []
    for lat in lats:
        for lon in lons:
            # Heat days are higher near the equator
            base_heat_days = max(0, 80 - abs(lat) * 1.5)

            # Add amplification based on global temp increase
            # Equator suffers more from global increase
            amplification = 1.0 + (abs(lat) / 90.0)
            projected_days = base_heat_days + (global_temp_increase_c * 15 * amplification)

            # Noise
            projected_days += np.random.normal(0, 5)
            
            # Polygon coordinates
            lon1, lon2 = lon - lon_step/2, lon + lon_step/2
            lat1, lat2 = lat - lat_step/2, lat + lat_step/2
            polygon = [
                [lon1, lat1],
                [lon2, lat1],
                [lon2, lat2],
                [lon1, lat2],
                [lon1, lat1]
            ]

            data.append({
                'lat': lat,
                'lon': lon,
                'polygon': polygon,
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
    
    # Use PolygonLayer for accurate rendering on a sphere without size distortions
    layer = pdk.Layer(
        "PolygonLayer",
        data=df_heat,
        get_polygon="polygon",
        get_fill_color="color",
        filled=True,
        extruded=False,
        wireframe=False,
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
