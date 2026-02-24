# Erklärung zur Nutzung von KI-Werkzeugen im Machine-Learning-Projekt

Dieses Dokument beschreibt den Einsatz von KI-basierten Werkzeugen im Rahmen des Machine-Learning-Projekts. Die Gliederung folgt dem **QUA³CK - Prozessmodell**, um transparent darzustellen, in welcher Phase des Projekts welche Werkzeuge zu welchem Zweck verwendet wurden.

Das QUA³CK - Modell ist ein iterativer Prozess für die Entwicklung von ML-Lösungen und steht für:
- **Q** - Question
- **U** - Understanding
- **A** - Algorithm Selection
- **A** - data Adaption
- **A** - parameter Adjustment
- **C** - Conclusion & Comparison
- **K** - Knowledge Transfer

Alle durch KI-Systeme generierten Ergebnisse (z.B. Code, Analysen, Texte) wurden von mir als verantwortlichem Entwickler kritisch geprüft, validiert und angepasst. Die finale Verantwortung für das Projekt liegt vollständig bei mir.

## Detaillierte Aufschlüsselung der Werkzeugnutzung nach Phase

| Phase (QUA³CK) | KI-Tool (Version) | Zweck | Beispielhafter Prompt / Anwendungsfall |
| :--- | :--- | :--- | :--- |
| **Q** - Question | GitHub Copilot, Google Gemini (1.5 Pro) | Recherche Datensätze, Projektkonzept (`C-Phase.ipynb`), Erstellung der Leitdokumente (`AGENT.md`, `README.md`) | "Finde aktuelle öffentliche Datensätze zu historischen lokalisierbaren Daten zur Erderwärmung... / Schreibe hieraus eine AGENT.md für mein Projekt." |
| **U** - Understanding | Google Gemini (1.5 Pro), GitHub Copilot | Explorative Datenanalyse (EDA) in der `U-Phase.ipynb`, Unterstützung bei spezifischen Geodaten-Bibliotheken (`xarray`, `rasterio`) | "Wie lade und visualisiere ich NetCDF-Klimadaten mit xarray und untersuche die Dimensionen?" |
| **A** - Algorithm Selection | GitHub Copilot | Auswahl und Implementierung von Regressionsmodellen (`Ridge`, `RandomForest`) in `A-Phase.ipynb`. Vergleich von linearen und nicht-linearen Ansätzen. | "Welche Scikit-Learn Modelle eignen sich für Zeitreihenvorhersage mit wenigen Datenpunkten? Erstelle einen Vergleich." |
| **A** - data Adaption | GitHub Copilot | Feature Engineering: Erstellung von Lag-Features und Rolling-Averages zur Abbildung von klimatischer Trägheit. | "Erzeuge Lag-Features für CO2 (1, 3, 5 Jahre) in Pandas, um verzögerte Temperatureffekte zu modellieren." |
| **A** - parameter Adjustment | GitHub Copilot | Hyperparameter-Tuning mittels `GridSearchCV` und `TimeSeriesSplit` zur Vermeidung von Data Leakage. | "Wie verhindere ich Data Leakage bei der Cross-Validation von Zeitreihen? Implementiere TimeSeriesSplit für Ridge." |
| **C** - Conclusion & Comparison | GitHub Copilot | (Geplant) Bewertung der Modellgüte und Selektion des finalen Modells. | "Vergleiche die RMSE-Werte der Modelle und visualisiere die Residuen." |
| **K** - Knowledge Transfer | GitHub Copilot | Erstellung von verständlicher Dokumentation (`README.md`, `GLOSSARY.md`) und Vorbereitung der Streamlit-App. | "Erstelle ein Glossar für Nicht-Experten, das Begriffe wie 'RMSE' und 'Hitzetag' einfach erklärt." | 

## Verwendete Datensätze

Im Rahmen des Projekts wurden folgende öffentlich zugängliche Datensätze verwendet:

| Datensatz | Quelle | Beschreibung | Verwendungszweck |
| :--- | :--- | :--- | :--- |
| **NASA GISS Surface Temp (GISTEMP v4)** | NASA GISS (Goddard Institute) | Globale monatliche Temperaturanomalien (1880–heute) auf 2°×2°-Raster; kombiniert Landstationen und Ozeandaten (ERSSTv5). | Historische Basisdaten („Ground Truth“) für das Training der lokalen Temperaturmodelle und Input für die globale Heatmap-Visualisierung. |
| **NOAA Mauna Loa CO₂ Record** | NOAA Global Monitoring Laboratory (GML) | Längste kontinuierliche Messreihe (seit 1958) der atmosphärischen CO₂-Konzentration (in ppm); bekannt als „Keeling-Kurve“. | Zentrales globales Feature (Prädiktor) für das ML-Modell, um den statistischen Zusammenhang zwischen Treibhausgasen und lokaler Temperatur zu lernen. |
| **Global Mean Sea Level Reconstruction** | EPA / CSIRO / NOAA | Rekonstruierte Zeitreihe (1880–heute) des globalen mittleren Meeresspiegels; fusioniert historische Pegelmessungen (Tide Gauges) mit präzisen Satellitendaten. | Dient als historische Zielvariable (Target) für das Training des ML-Modells, um den Zusammenhang zwischen Temperaturanstieg und Meeresspiegeländerung zu lernen. |
| **Copernicus DEM (GLO-30)** | ESA / OpenTopography / AWS | Globales digitales Oberflächenmodell (DSM) mit 30m Auflösung. Aktueller wissenschaftlicher Standard für weltweite Höhenanalysen (höhere vertikale Genauigkeit als SRTM). | Globale & Regionale Ebene: Basis für die Berechnung von Überflutungsflächen auf der Weltkarte und für größere Regionen. |