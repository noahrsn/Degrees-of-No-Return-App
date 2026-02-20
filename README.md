# 🌍 Degrees of No Return

> **Lokale Klimarisiken sichtbar machen.** > Eine interaktive WebApp, die komplexe globale Klimamodelle in lokal verständliche, visuelle Risikobilder übersetzt.

## 📖 Über das Projekt
Der Klimawandel wird oft über globale Kennzahlen (z. B. durchschnittliche Erderwärmung, globale Meeresspiegelanstiege) diskutiert. Für lokale Entscheidungsträger stellt sich jedoch die Frage: **Was bedeutet das konkret hier vor Ort?**

„Degrees of No Return“ setzt genau hier an. Das Projekt nutzt historische Klimadaten und Machine-Learning-Modelle, um globale Emissionsszenarien auf eine lokale Ebene herunterzubrechen. Es prognostiziert **Überflutungsrisiken** und die **Häufigkeit von Hitzetagen** bis zum Jahr 2050 und macht diese durch eine interaktive [Streamlit](https://streamlit.io/)-App für Nicht-Experten intuitiv greifbar.

### 🎯 Zielgruppe
* **Kommunale Stadt- und Raumplaner:** Entwicklung von Anpassungsstrategien und Schutz von Infrastruktur.
* **Versicherungsanalysten:** Datenbasierte Quantifizierung von Klimarisiken in Portfolios.
* **Private Immobilienbesitzer:** Einschätzung der zukünftigen Betroffenheit des eigenen Eigentums.

---

## ✨ Features (Geplant/In Entwicklung)
* **🗺️ Dynamische Weltkarte:** Stufenloser Zoom von globalen Klimamustern bis auf die lokale Ebene (Quartiersansicht).
* **📊 Lokale Schlüsselkennzahlen:** Echtzeit-Berechnung von erwarteten Temperaturänderungen, jährlichen Hitzetagen und potenziell überfluteten Flächenanteilen.
* **⏳ Zeit-Slider:** Intuitive Visualisierung der historischen Entwicklung und der Prognosen bis 2050.
* **🔀 Szenario-Switch:** Direkter Vergleich zwischen einem „Weiter-wie-bisher“-Emissionspfad und ehrgeizigen Klimaziel-Szenarien.

---

## 🗂️ Datengrundlage
Das Projekt stützt sich auf validierte, renommierte und offene Datenquellen der Klimaforschung:
* **Temperatur:** Earth Surface Temperature Dataset (Berkeley Earth) & GISS Surface Temperature Analysis (NASA)
* **CO₂-Konzentration:** Mauna-Loa-Observatorium (NOAA)
* **Meeresspiegel:** NASA Sea Level Change Data & IPCC-Szenarien
* **Topographie / Höhenmodelle (DEM):** SRTM & Copernicus DEM

---

## 🛠️ Repository-Struktur
* `data/` - Enthält die Rohdaten (NetCDF, CSV). *Hinweis: Große GeoTIFFs oder NetCDF-Dateien sind ggf. von der Versionskontrolle ausgeschlossen (`.gitignore`).*
* `U-Phase.ipynb` - **Understanding the Data:** Explorative Datenanalyse (EDA) und Untersuchung der Rohdatenstrukturen.
* `C-Phase.ipynb` - **Concept Phase:** Konzeptionelle Ausarbeitung und erste Methodentests.
* `AGENT.md` - System-Prompt und Leitfaden für KI-gestützte Entwicklungsarbeit an diesem Projekt.
* `AI_TOOL_DISCLOSURE.md` - Transparenzhinweis zur Nutzung von KI-Tools im Entwicklungsprozess.

---

## 🚀 Installation & Setup

Da sich das Projekt noch in einer frühen Phase befindet, liegt der Fokus aktuell auf der Datenexploration in den Jupyter Notebooks. 

### Voraussetzungen
* Python 3.9+
* Git

### Lokale Umgebung einrichten
1. **Repository klonen:**
   ```bash
   git clone https://github.com/noahrsn/Degrees-of-No-Return-App
   cd degrees-of-no-return

2. **Virtuelle Umgebung erstellen und aktivieren:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt

3. **Jupyter Notebooks starten:**
   ```bash
   jupyter notebook

---

## 🤝 Mitwirken

Beiträge sind willkommen! Wenn du Ideen zur Verbesserung der ML-Modelle, der Daten-Pipelines oder der Streamlit-App hast, öffne gerne ein Issue oder erstelle einen Pull Request.