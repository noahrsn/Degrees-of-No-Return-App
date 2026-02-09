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
| **Q** - Question | GitHub Copilot (GPT-4o), Google Gemini 1.5 Pro | Recherche Datensätze, Konzept | "Finde aktuelle öffentliche Datensätze (CC-Lizenz) zum Thema 'Telco Customer Churn'. Liste Features und Zielvariablen auf." |
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
| **Telco Customer Churn** | Kaggle / IBM Sample Data Sets | Datensatz mit 7043 Kunden, inkl. Demografie, Services und Churn-Label. | Hauptdatensatz für Training, Validierung und EDA (Phase **U**, **A**). |
| **Bank Customer Churn** | Kaggle (Public Domain) | Daten von 10.000 Bankkunden mit Kredit-Score, Balance und Produktanzahl. | Validierung der Pipeline-Generalisierbarkeit auf Finanzdaten (Phase **C**). |
| **Synthetic Churn Data** | Generiert (`scikit-learn`) | Synthetischer Datensatz (100k Samples) mit simulierten Features. | Lasttests für die API und Benchmarking der Inferenzzeit (Phase **K**). |
| **US Zip Code Database** | SimpleMaps (Basic) | Zuordnungstabelle von PLZ zu US-Bundesstaaten und Koordinaten. | Feature Engineering zur Anreicherung geografischer Informationen (Phase **A**). |