import rasterio
from rasterio.session import AWSSession
import matplotlib.pyplot as plt

# Die direkte S3-URL für die Kachel Düsseldorf/Rheinland
url = "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N51_00_E006_00_DEM/Copernicus_DSM_COG_10_N51_00_E006_00_DEM.tif"

# Umgebung mit anonymem Zugriff starten, Daten verkleinert (512x512) laden und direkt plotten
with rasterio.Env(AWSSession(aws_unsigned=True)):
    with rasterio.open(url) as src:
        plt.imshow(src.read(1, out_shape=(512, 512)), cmap='terrain')
        plt.colorbar(label='Höhe über NN (m)')
        plt.title("Topografie Region Düsseldorf (N51, E006)")
        plt.show()