# 🌍 Degrees of No Return

## Über das Projekt
„Degrees of No Return“ ist ein Machine-Learning-Projekt, das abstrakte globale Klimamodelle in lokal verständliche Risikobilder übersetzt. Der Fokus liegt darauf, Entscheidungsträgern (wie Stadtplanern oder Immobilienbesitzern) konkrete Vorhersagen zu **lokalen Hitzetagen** und **Überflutungsrisiken** bis zum Jahr 2050 zu liefern.

Anstatt nur globale Durchschnittswerte zu betrachten, bricht dieses Projekt die Daten herunter: Was bedeutet die Erderwärmung konkret für meine Stadt?

## Installation & Einrichtung

Folgen Sie diesen Schritten, um die Entwicklungsumgebung einzurichten:

1.  **Repository klonen**
    ```bash
    git clone <repository-url>
    cd Streamlit-App
    ```

2.  **Virtuelle Umgebung erstellen (Optional, aber empfohlen)**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

3.  **Abhängigkeiten installieren**
    Installieren Sie alle benötigten Pakete über die `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jupyter Notebooks starten**
    Um die Analysephasen (Q, U, A) anzusehen oder auszuführen:
    ```bash
    jupyter notebook
    ```

## 🗂️ Verwendete Datensätze

Das Projekt stützt sich ausschließlich auf validierte, wissenschaftliche "Single Source of Truth"-Datenquellen, um maximale Glaubwürdigkeit zu gewährleisten:

*   **Atmosphäre (CO₂): `co2_mm_mlo.csv`**
    *   *Quelle:* NOAA Global Monitoring Laboratory (GML) – Mauna Loa Observatorium.
    *   *Beschreibung:* Die längste kontinuierliche Messreihe der atmosphärischen CO₂-Konzentration der Welt ("Keeling-Kurve"). Sie dient als zentraler Indikator für den menschgemachten Treibhauseffekt.

*   **Meeresspiegel: `epa_sea_level.csv`**
    *   *Quelle:* US Environmental Protection Agency (EPA) / CSIRO / NOAA.
    *   *Beschreibung:* Historische Daten zum globalen absoluten Meeresspiegelanstieg seit 1880. Dieser Datensatz kombiniert Pegelmessungen und moderne Satellitendaten.

*   **Temperatur: `gistemp1200_GHCNv4_ERSSTv5.nc`**
    *   *Quelle:* NASA Goddard Institute for Space Studies (GISS).
    *   *Beschreibung:* Ein hochkomplexer, rasterbasierter Datensatz (NetCDF), der monatliche globale Oberflächentemperaturen und Anomalien speichert. Er ist der Goldstandard für die Analyse der globalen Erwärmung.

*   **Topographie: Copernicus DEM (GLO-30)**
    *   *Quelle:* ESA / OpenTopography.
    *   *Beschreibung:* Ein digitales Oberflächenmodell der Erde mit einer extrem hohen Auflösung von 30 Metern. Es ist essenziell, um lokale Überflutungsrisiken (z.B. "Welche Straßen stehen unter Wasser?") präzise zu berechnen.

## Der QUA³CK-Prozess (Methodik)

Wir arbeiten nach dem **QUA³CK-Prozessmodell** (gesprochen: "Quack"). Dies stellt sicher, dass wir wissenschaftlich sauber von der Frage zur Lösung kommen. Die Phasen sind in entsprechenden Jupyter Notebooks dokumentiert:

### 1. [Q-Phase: Question (Fragestellung)](Q-Phase.ipynb)
Hier definieren wir das "Warum?".
*   *Inhalt:* Definition der Forschungsfragen, Identifikation der Zielgruppen (Stadtplaner, Versicherer) und Festlegung der harten Erfolgsmetriken (z.B. RMSE < 0,2°C).

### 2. [U-Phase: Understanding the Data (Datenverständnis)](U-Phase.ipynb)
Hier lernen wir unsere Rohdaten kennen.
*   *Inhalt:* Explorative Datenanalyse (EDA), Prüfung der Datenqualität, Visualisierung erster Trends und Bereinigung von Fehlwerten.

### 3. [A-Phasen: Algorithm, Adaptation, Adjustment (Modellierung)](A-Phase.ipynb)
Das Herzstück des maschinellen Lernens – aufgeteilt in drei Schritte (A³):
*   **A1 – Algorithm Selection:** Auswahl des passenden Modells (z.B. Ridge Regression).
*   **A2 – Adapting Features:** Anpassung der Daten (z.B. Verzögerungseffekte/Lag-Features einbauen), damit das Modell die Trägheit des Klimas versteht.
*   **A3 – Adjusting Hyperparameters:** Feinjustierung der Modelleinstellungen für maximale Präzision.

### 4. C-Phase: Conclude (Schlussfolgerung)
*   *Status:* (In Entwicklung)
*   *Inhalt:* Finale Bewertung der trainierten Modelle und Entscheidung für das beste Setup.

### 5. K-Phase: Knowledge Transfer (Wissenstransfer)
*   *Status:* (Geplant)
*   *Inhalt:* Aufbau der **Streamlit WebApp**. Übersetzung der komplexen Zahlen in interaktive Karten und Regler für den Endanwender.
