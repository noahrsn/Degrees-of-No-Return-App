# Glossar: Degrees of No Return

Dieses Glossar erklärt die wichtigsten Fachbegriffe aus den Bereichen Meteorologie und Data Science, die in diesem Projekt verwendet werden.

### 🌡️ Meteorologie & Klimawissenschaften

* **Hitzetag:** Dies ist ein fest definierter Begriff aus der Meteorologie. Ein Tag gilt offiziell als Hitzetag, wenn die an einer Wetterstation gemessene Lufttemperatur (in der Regel in 2 Metern Höhe) mindestens **30,0 °C** erreicht. 
* **Temperaturanomalie:** Hierbei handelt es sich um die Abweichung der Temperatur von einem langjährigen Durchschnittswert. Es wird also nicht gemessen, wie viel Grad es an einem Tag genau hatte, sondern um wie viel Grad es wärmer oder kälter war als im historischen Mittel.
* **Keeling-Kurve:** Die grafische Darstellung der kontinuierlichen Messung der CO₂-Konzentration in der Atmosphäre seit 1958 auf dem Vulkan Mauna Loa auf Hawaii. Sie gilt als Referenz für die globale CO₂-Entwicklung.
* **Deseasonalized (saisonbereinigt):** Bezeichnet Daten, bei denen regelmäßige jahreszeitliche Schwankungen herausgerechnet wurden. Zum Beispiel nehmen Pflanzen im Sommer CO₂ auf und geben es im Winter wieder ab. Durch die Glättung dieser Zacken wird der eigentliche, langfristige Trend sichtbar.
* **Tide Gauges (Küstenpegel):** Historische Messstationen an der Küste zur Bestimmung des Meeresspiegels. 
* **Altimetriedaten (Satelliten-Altimetrie):** Hochpräzise Messreihen, bei denen Satelliten (seit 1993) aus dem All die Höhe des Meeresspiegels erfassen.

### 💻 Data Science & App-Entwicklung

* **Downscaling:** Ein wichtiges Verfahren, bei dem grobmaschige, globale Daten auf kleine, lokale Koordinaten anwendbar gemacht werden (z. B. auf Straßenzüge oder bestimmte Städte). 
* **EDA (Explorative Datenanalyse):** Das Fundament der Datenverarbeitung. Hierbei werden Rohdaten zunächst auf ihre Struktur, Muster, Qualität und mögliche Fehler geprüft.
* **Ground Truth:** Bezeichnet die „absolute Wahrheit“ oder den verlässlichen Referenzdatensatz für ein Modell. In diesem Projekt dienen die historischen Temperaturdaten der NASA als Ground Truth, an der das Modell lernt, wie reale Erwärmung aussieht.
* **Imputation:** Ein statistisches Verfahren, um fehlende Datenpunkte in einer Messreihe künstlich zu berechnen ("erfinden"). Um die wissenschaftliche Glaubwürdigkeit der App nicht zu gefährden, wird hier im Projekt bewusst darauf verzichtet.
* **Prädiktor:** Der zentrale Einflussfaktor, der genutzt wird, um in einem Machine-Learning-Modell etwas vorherzusagen. Hier ist z. B. der CO₂-Wert der Prädiktor für die Klimaerwärmung.
* **Skalierung (Normalisierung):** Da verschiedene Datenreihen (wie CO₂-Konzentration mit Werten über 400 und Temperaturänderungen um 2 Grad) unterschiedliche Größenordnungen haben, müssen sie für das Machine-Learning-Modell auf einen einheitlichen Maßstab gebracht werden, um fehlerhafte Gewichtungen zu verhindern.
* **Copernicus DEM (Digitales Höhenmodell):** Eine extrem genaue, dreidimensionale Landkarte der Erde aus dem All. In dieser Karte ist für jeden Bildpunkt hinterlegt, wie hoch er über dem Meeresspiegel liegt.
* **GeoTIFF / NetCDF (.nc):** Dies sind Standard-Datenformate für die Wissenschaft. *GeoTIFF* wird oft für Bilder verwendet, in denen jeder Pixel mit echten geografischen Koordinaten und Höhenwerten verknüpft ist. *NetCDF* speichert mehrdimensionale Raster-Daten ab, um beispielsweise Temperaturänderungen über Raum (Längen-/Breitengrad) und Zeit (Monate) abzubilden.