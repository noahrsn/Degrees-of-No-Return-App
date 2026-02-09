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
| **Q** - Question | GitHub Copilot (GPT-4o), Google Gemini 1.5 Pro | Recherche Datensätze, Konzept | "Finde aktuelle öffentliche Datensätze zu historischen lokalisierbaren Daten zur Erderwärmung auf. Liste Features und Zielvariablen auf." |
| **U** - Understanding |  | Explorative Datenanalyse (EDA) |  |
| **A** - Algorithm Selection |  | Algorithmenauswahl |  |
| **A** - data Adaption |  | `scikit-learn` Preprocessing |  |
| **A** - parameter Adjustment |  | `mlflow` & `scikit-learn` Integration |  |
| **C** - Conclusion & **C**omparison |  | Analyse von `mlflow`-Daten |  |
| **K** - Knowledge **T**ransfer |  | `streamlit`-Dashboard |  |
| **K** - Knowledge **T**ransfer |  | Dokumentation, Übersetzung |  | 

## Verwendete Datensätze

Im Rahmen des Projekts wurden folgende öffentlich zugängliche Datensätze verwendet:

| Datensatz | Quelle | Beschreibung | Verwendungszweck |
| :--- | :--- | :--- | :--- |
| **NASA GISS Surface Temp (GISTEMP v4)** | NASA GISS (Goddard Institute) | Globale monatliche Temperaturanomalien (1880–heute) auf 2°×2°-Raster; kombiniert Landstationen und Ozeandaten (ERSSTv5). | Historische Basisdaten („Ground Truth“) für das Training der lokalen Temperaturmodelle und Input für die globale Heatmap-Visualisierung. |
| **NOAA Mauna Loa CO₂ Record** | NOAA Global Monitoring Laboratory (GML) | Längste kontinuierliche Messreihe (seit 1958) der atmosphärischen CO₂-Konzentration (in ppm); bekannt als „Keeling-Kurve“. | Zentrales globales Feature (Prädiktor) für das ML-Modell, um den statistischen Zusammenhang zwischen Treibhausgasen und lokaler Temperatur zu lernen. |
| **Global Mean Sea Level Reconstruction** | EPA / CSIRO / NOAA | Rekonstruierte Zeitreihe (1880–heute) des globalen mittleren Meeresspiegels; fusioniert historische Pegelmessungen (Tide Gauges) mit präzisen Satellitendaten. | Dient als historische Zielvariable (Target) für das Training des ML-Modells, um den Zusammenhang zwischen Temperaturanstieg und Meeresspiegeländerung zu lernen. |
| **Copernicus DEM (GLO-30)** | ESA / OpenTopography / AWS | Globales digitales Oberflächenmodell (DSM) mit 30m Auflösung. Aktueller wissenschaftlicher Standard für weltweite Höhenanalysen (höhere vertikale Genauigkeit als SRTM). | Globale & Regionale Ebene: Basis für die Berechnung von Überflutungsflächen auf der Weltkarte und für größere Regionen. |
| **DGM1 (Digitales Geländemodell)** | Geodatenzentren der Bundesländer (Open Data) | Höchstaufgelöstes Geländemodell mit 1m Raster für Deutschland. Bildet die reine Bodenhöhe (ohne Vegetation/Gebäude) extrem präzise ab. | Lokale Ebene (Zoom): Ermöglicht die im Pitch versprochene „grundstücksgenaue“ Risikoanalyse für deutsche Kommunen und Immobilienbesitzer. |