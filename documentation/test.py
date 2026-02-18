import pandas as pd
from pathlib import Path
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def main():
    base_dir = Path(__file__).resolve().parent.parent / "data"
    co2 = base_dir / "co2_mm_mlo.csv"
    epa_sea_level = base_dir / "epa_sea_level.csv"
    gistemp1200_GHCNv4_ERSSTv5 = base_dir / "gistemp1200_GHCNv4_ERSSTv5.nc"

    if not co2.exists():
        print(f"Datei nicht gefunden: {co2}")
        return

    dataset = xr.open_dataset(gistemp1200_GHCNv4_ERSSTv5)
    temp_anomaly = dataset["tempanomaly"].sel(time="2026-01-15")

    # Plot erstellen
    fig, ax = plt.subplots(
        figsize=(12, 8),
        subplot_kw={"projection": ccrs.PlateCarree()}  # Kartenprojektion
    )

    # Weltkarte hinzufügen
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)  # Küstenlinien
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)    # Ländergrenzen
    ax.add_feature(cfeature.LAND, facecolor="lightgray")  # Landflächen
    ax.add_feature(cfeature.OCEAN, facecolor="lightblue")  # Ozeanflächen

    # Temperaturanomalien plotten
    temp_anomaly.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),  # Projektion der Daten
        cmap="coolwarm",               # Farbskala
        cbar_kwargs={"label": "Temperaturanomalie (°C)"},  # Farblegende
    )

    # Titel hinzufügen
    ax.set_title("Temperaturanomalien am 15. Januar 2026", fontsize=14)

    # Plot anzeigen
    plt.show()

    
    #df = pd.read_csv(epa_sea_level, comment="#", on_bad_lines="skip", engine="python")
    #print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()