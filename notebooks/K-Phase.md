# K-Phase: Knowledge Transfer & Web-Deployment

Diese Dokumentation beschreibt den finalen Schritt im QUA³CK-Framework für das Projekt **"Degrees of No Return"**. In der K-Phase (Knowledge Transfer) wurde die technische und wissenschaftliche Modellierung aus den vorherigen Phasen (Q, U, A, C) in eine interaktive, nutzerzentrierte Web-Anwendung (Streamlit-Dashboard) überführt.

---

## 1. Zielsetzung der K-Phase

Das vorrangige Ziel war es, **komplexe Klima- und Geodatenmodelle** so aufzubereiten, dass sie für Entscheidungsträger (Stadt- und Raumplaner, Versicherungsanalysten) sowie für private Immobilienbesitzer intuitiv nutzbar sind. Die K-Phase stellte sicher, dass aus abstrakten Algorithmen verständliche Erkenntnisse ("Insights") und visualisierbare Risikoszenarien generiert werden.

**Leitfragen des Knowledge Transfers:**
* Wie lassen sich die Machine-Learning-Vorhersagen (Hitzetage, Meeresspiegelanstieg bis 2050) greifbar an Endnutzer kommunizieren?
* Wie können lokale topografische Daten zur Überschwemmung interaktiv mit globalen Modellen verknüpft werden?
* Wie verhindert das Frontend eine Fehlinterpretation der Prognosen (Scheingenauigkeit)?

---

## 2. Architektur & Frontend-Entwicklung (Streamlit)

Als Kerntechnologie für das Deployment wurde **Streamlit** gewählt. Es ermöglicht ein nahtloses Zusammenspiel aus Python-basiertem Backend (ML-Pipelines, Geo-Verarbeitung) und interaktivem Web-Frontend.

### 2.1 Struktur der Anwendung
Die App (`app.py`) ist in ein Dashboard mit zwei Hauptkomponenten (Tabs) unterteilt, die unsere beiden Leitrisiken abdecken:

* **Tab 1 ("🌊 Lokale Überflutung"):** Ein lokaler "Flood Mapper", der topografische Überschwemmungsrisiken in Echtzeit visualisiert.
* **Tab 2 ("🌡️ Globale Heatmap"):** Ein globaler Temperatur-Mapper, der den Anstieg der Hitzetage rasterbasiert darstellt.

### 2.2 Benutzeroberfläche (UI) & Benutzerführung (UX)
Um die Zielgruppe bestmöglich zu führen, wurden folgende UI/UX-Konzepte umgesetzt:
* **Seitenleisten-Steuerung (Sidebar):** Sämtliche globale Parameter (Zieljahr, SSP-Szenarien, Temperatur- und Meeresspiegelerhöhung) lassen sich über intuitive Slider steuern. So ist sofort ein "Was wäre wenn?"-Szenario erlebbar.
* **Schlüsselkennzahlen-Panels (KPIs):** Über Streamlit `st.metric()` werden die wissenschaftlichen Kernmetriken (wie erwartete Hitzetage, Meeresspiegel-Anomalie) direkt oben eingeblendet.
* **Transparenz durch Konfidenzintervalle:** Anstatt starrer Werte für die Zukunft (die als irreführend genaue "Fakten" missverstanden werden könnten), gibt das Tool Schwankungsbreiten (z.B. "±0.5°C") aus.
* **Disclaimer & Expander:** In Akkordeon-Elementen (`st.expander`) werden methodische Einschränkungen (z.B. dass Binnenhochwasser durch Regen nicht simuliert wird, oder städtische Hitzeinseleffekte) transparent kommuniziert.

---

## 3. Tool-Entwicklung & Datenanbindung

### 3.1 Der Local Flood Mapper (`src/flood_mapper.py`)
Dieses Modul ist das Herzstück zur Einschätzung von Überflutungsrisiken. 

* **Ursprünglicher Prototyp (Open-Meteo):** Zunächst wurden Höhendaten über die kostenlose Open-Meteo-API (REST) abgefragt. Dies führte zu starken Limitationen (Rate-Limits, Interpolationsfehler für Binnenmeere wie "NaN"-Werte für Wasser, mangelnde Auflösung).
* **Der wissenschaftliche Pivot (Single Source of Truth):** Im Verlauf der K-Phase wurde der Flood Mapper radikal umgebaut. Er lädt nun via `rasterio` und `boto3` **direkt von AWS S3** die hochaufgelösten **Copernicus DEM (GLO-30)** Kacheln.
* **Räumliches Stitching:** Die Logik berechnet für eine Stadt eigenständig das Bouding-Box-Raster (circa 45km Umkreis) und verbindet ("stitched") falls nötig mehrere Cloud Optimized GeoTIFFs nahtlos miteinander.
* **Visuelles Rendering:** Anstelle von runden Punktsäulen wird nun ein zusammenhängendes, polygonales 3D-Gitter (`pydeck` PolygonLayer mit `extruded=True`) in die Karte gerendert, was die physische Landschaft akkurat und lückenlos nachbildet. Rote, flache Flächen repräsentieren den Meeresspiegel beziehungsweise Überflutungsstand, der mit der Topografie kollidiert.

### 3.2 Die Globale Heatmap (`src/global_heat_mapper.py`)
Dieses Modul überträgt den globalen Temperaturanstieg auf ein Raster von Hitzetagen.
* **Korrektur der Kartendarstellung:** Zunächst führten "Meter-basierte" Rasterpunkte zu starker Verzerrung am Äquator vs. an den Polen (Mercator-Projektion). Dies wurde in der K-Phase durch einen physikalischen `GridCellLayer` bzw. geographisch korrekten Längen-/Breitengrad-`PolygonLayer` ersetzt, sodass die Hitze-Cluster über den gesamten Globus lückenlos eine zusammenhängende Hitzekarte bilden.
* **Farbskalen:** Eine wissenschaftlichen Normen entsprechende Interpolation (Gelb bis Tiefviolett) zeigt grafisch verständlich die Härte der Belastung.

---

## 4. ML-Integration und Vorhersagen (`src/ml_pipelines.py`)

Die in der A-Phase und C-Phase trainierten Machine Learning Modelle (wie Random Forest für die Temperatur, Polynomiale Regression für den Meeresspiegel) wurden in einer sauberen, gekapselten Python-Klasse `MLPipelines` vereint.
Diese Klasse abstrahiert die komplexen Formeln und ermöglicht das einfache Abrufen via `predict`-Methoden direkt aus dem Frontend.

* **Szenarien-Mapping (SSP):** Die App bietet die IPCC-SSP-Szenarien als Auswahl (z.B. SSP1-1.9 vs. SSP5-8.5). Die Pipeline übersetzt dieses Kürzel im Backend in die jeweiligen CO₂-Wachstumsraten und feedet diese als Eingangs-Features in die Machine Learning Modelle.

---

## 5. Resultat

Die K-Phase schließt die Lücke von der reinen Daten-Jupyter-Analyse hin zur nutzerorientierten Applikation. Durch iteratives Refactoring – vom Wegfall limitierender APIs hin zum direkten Zugriff auf Copernicus Rasterdaten – ist das finale **"Degrees of No Return"**-Dashboard ein robustes, lauffähiges und interaktives Instrument entstanden.

Es erfüllt die Anforderungen, globale Abstraktionen greifbar und, insbesondere wichtig für Raumplaner, **lokal anwendbar** zu visualisieren, wobei der QUA³CK-Anspruch auf Validität und Transparenz der Vorhersagen zu jeder Zeit gewahrt wurde.