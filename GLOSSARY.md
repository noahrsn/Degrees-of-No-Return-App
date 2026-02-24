# 📖 Glossar & Begriffserklärungen

Dieses Glossar erklärt wichtige Begriffe, Methoden und Metriken aus dem Projekt „Degrees of No Return“ in verständlicher Sprache. Es dient als Nachschlagewerk für alle, die tiefer in die Materie eintauchen möchten, ohne Data-Science-Experten zu sein.

## 🌡️ Klimatologische Begriffe

**Hitzetag**
Ein meteorologischer Begriff. Ein Tag gilt dann als Hitzetag, wenn die **Tageshöchsttemperatur 30 °C erreicht oder überschreitet**. In unseren Modellen prognostizieren wir die jährliche Anzahl dieser Tage, da sie ein direkter Indikator für Gesundheitsrisiken und städtische Hitzeinseln sind.

**Emissionspfade (Szenarien)**
Zukunftsprojektionen darüber, wie viel Treibhausgas die Menschheit in den kommenden Jahren ausstoßen wird. Das Projekt unterscheidet oft zwischen einem „Weiter-wie-bisher“-Szenario (hohe Emissionen) und einem „Klimaziel“-Szenario (starke Reduktion der Emissionen).

**Downscaling**
Das "Herunterrechnen" von globalen Daten auf eine lokale Ebene. Ein globales Klimamodell sagt vielleicht vorher, dass die Erde im Schnitt 1 Grad wärmer wird. Downscaling berechnet, was das *konkret* für z.B. Berlin oder München bedeutet (da sich Landmassen schneller erwärmen als Ozeane).

---

## 🤖 Machine Learning & Data Science (Die „A-Phasen“)

**Algorithmus**
In unserem Kontext ein „Rezept“ für den Computer. Es ist eine Rechenvorschrift, die aus Daten lernt. Wir testen verschiedene Algorithmen (z.B. *Lineare Regression*, *Random Forest*), um zu sehen, welcher die Zusammenhänge zwischen CO₂ und Temperatur am besten versteht.

**Training & Testen**
Wir geben dem Modell nie *alle* Daten zum Lernen. Wir behalten einen Teil (die jüngsten Jahre) zurück („Testdaten“). Das Modell lernt mit den alten Daten („Trainingsdaten“) und muss dann beweisen, dass es die Testdaten korrekt vorhersagen kann, ohne sie vorher gesehen zu haben.

**Features (Merkmale)**
Die „Zutaten“, mit denen wir das Modell füttern.
*   *Beispiel:* Um die Temperatur von morgen vorherzusagen, könnten Features sein: „Temperatur heute“, „CO₂-Konzentration aktuell“, „Jahreszeit“.
*   **Lag-Features (Verzögerung):** Ein spezielles Feature. Da das Klima träge ist (wie ein schwerer Güterzug), wirkt sich CO₂ von heute erst später voll aus. Lag-Features berücksichtigen diese Verzögerung (z.B. „CO₂-Wert von vor 10 Jahren“).

**Hyperparameter**
Die „Einstellungen am Backofen“. Während der Algorithmus das Rezept ist, sind Hyperparameter die Feinjustierungen (z.B. wie schnell soll das Modell lernen? Wie komplex darf die Formel sein?). Wir optimieren diese, um das bestmögliche Ergebnis zu erzielen.

**Overfitting (Überanpassung)**
Ein häufiges Problem. Das Modell lernt die Trainingsdaten *zu* gut auswendig, anstatt die allgemeinen Regeln zu verstehen.
*   *Metapher:* Ein Schüler, der die Lösungen für die Mathe-Hausaufgabe auswendig lernt, aber in der Klassenarbeit (neue Aufgaben) versagt. Wir vermeiden das durch Techniken wie *Cross-Validation*.

---

## 📊 Messgrößen der Genauigkeit

**RMSE (Root Mean Square Error)**
Unser wichtigstes Maß für die Genauigkeit bei Temperaturvorhersagen.
*   Er gibt an, um wie viel Grad das Modell im Durchschnitt daneben liegt.
*   **Ziel:** Wir wollen einen RMSE von unter **0,2 °C**. Das bedeutet, unsere Vorhersage weicht durchschnittlich weniger als 0,2 Grad vom tatsächlichen Wert ab.

**R² (Bestimmtheitsmaß)**
Ein Wert zwischen 0 und 1 (oder 0% und 100%). Er sagt aus, wie viel Prozent der Schwankungen in den Daten unser Modell erklären kann.
*   Ein R² von 0,95 bedeutet: Das Modell erklärt 95% der Temperaturveränderungen korrekt.

---

## 🔄 Prozessmodell: QUA³CK

Wir arbeiten nach dem **QUA³CK-Prozessmodell** (gesprochen: "Quack"). Es ist unser strukturierter Fahrplan, um von der ersten Idee zur fertigen Anwendung zu gelangen. Das "Hoch 3" steht für die drei intensiven Entwicklungsphasen im Bereich Machine Learning.

**Q – Question (Fragestellung)**
*   Am Anfang steht das "Warum?". Wir definieren das konkrete Problem, die Zielgruppe (z.B. Stadtplaner) und die Erfolgskriterien.
*   *Ziel:* Ein klares Verständnis davon, was wir lösen wollen (z.B. "Wie heiß wird es 2050 in Berlin?").

**U – Understanding the Data (Datenverständnis)**
*   Bevor wir modellieren, müssen wir unsere Daten kennenlernen. Wir prüfen Qualität, Ursprung und Verteilung.
*   *Ziel:* Sicherstellen, dass unsere Datenbasis ("Single Source of Truth") sauber und vertrauenswürdig ist.

**A1 – Algorithm Selection (Algorithmenauswahl)**
*   Die Suche nach dem passenden Werkzeug. Testen verschiedener Modelle (z.B. Lineare Regression vs. Random Forest).
*   *Ziel:* Den Algorithmus finden, der unser Problem am besten lösen kann.

**A2 – Adapting Features (Feature-Anpassung)**
*   Datenaufbereitung für Fortgeschrittene. Wir transformieren Rohdaten so, dass das Modell sie besser versteht (z.B. durch "Lag-Features" oder zeitliche Synchronisierung).
*   *Ziel:* Den Rohdiamanten schleifen, damit das Modell Muster leichter erkennt.

**A3 – Adjusting Hyperparameters (Hyperparameter-Optimierung)**
*   Feinjustierung. Wir drehen an den Stellschrauben des gewählten Modells, um das letzte Quäntchen Genauigkeit herauszuholen (z.B. RMSE unter 0,2 °C drücken).
*   *Ziel:* Maximale Performance und Robustheit.

**C – Conclusion & Compare (Schlussfolgerung)**
*   Der Realitätscheck. Wir bewerten das fertig trainierte Modell kritisch und vergleichen es mit Alternativen.
*   *Ziel:* Die Entscheidung für das finale Modellsetup, das in die App kommt.

**K – Knowledge Transfer (Wissenstransfer)**
*   Vom Code zur Anwendung. Wir bauen die Streamlit-Web-App und dokumentieren unsere Ergebnisse verständlich.
*   *Ziel:* Die komplexen Ergebnisse für den Endnutzer nutzbar machen (Dashboard, Karten, KPIs).
