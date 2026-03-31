# 📖 Glossar & Begriffserklärungen

Dieses Glossar erklärt wichtige Begriffe, Methoden und Metriken aus dem Projekt „Degrees of No Return“ in verständlicher Sprache. Es dient als Nachschlagewerk für alle, die tiefer in die Materie eintauchen möchten, ohne Data-Science-Experten zu sein.

## 🌡️ Klimatologische Begriffe

**Hitzetag**
Ein meteorologischer Begriff. Ein Tag gilt dann als Hitzetag, wenn die **Tageshöchsttemperatur 30 °C erreicht oder überschreitet**. In unseren Modellen prognostizieren wir die jährliche Anzahl dieser Tage, da sie ein direkter Indikator für Gesundheitsrisiken und städtische Hitzeinseln sind.
*   *Quelle:* [Deutscher Wetterdienst (DWD) - Wetterlexikon: Hitzetag](https://www.dwd.de/DE/service/lexikon/Functions/glossar.html?lv2=101094&lv3=101192)

**Emissionspfade (Szenarien / SSPs)**
Zukunftsprojektionen darüber, wie viel Treibhausgas die Menschheit in den kommenden Jahren ausstoßen wird. Die Wissenschaft nutzt dafür sogenannte *Shared Socioeconomic Pathways (SSPs)*. Das Projekt unterscheidet oft zwischen einem „Weiter-wie-bisher“-Szenario (hohe Emissionen, z.B. SSP5-8.5) und einem „Klimaziel“-Szenario (starke Reduktion der Emissionen, z.B. SSP1-2.6).
*   *Quelle:* [IPCC (Intergovernmental Panel on Climate Change) - AR6 Scenarios](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter_01.pdf)

**Downscaling**
Das "Herunterrechnen" von globalen Daten auf eine lokale Ebene. Ein globales Klimamodell sagt vielleicht vorher, dass die Erde im Schnitt 1 Grad wärmer wird. Downscaling berechnet, was das *konkret* für z.B. Berlin oder München bedeutet (da sich Landmassen schneller erwärmen als Ozeane und lokale Topografie eine Rolle spielt).
*   *Quelle:* [Climate Data Guide (NCAR) - Statistical Downscaling](https://climatedataguide.ucar.edu/climate-data/statistical-downscaling)

**Temperaturanomalie**
Die Abweichung der Temperatur von einem langjährigen Durchschnittswert (Referenzperiode, z.B. 1951–1980). In der Klimaforschung arbeitet man fast ausschließlich mit Anomalien statt mit absoluten Temperaturen, da diese robuster gegenüber Messfehlern einzelner Stationen sind und globale Trends besser abbilden.
*   *Quelle:* [NASA Earth Observatory - Why Anomalies?](https://earthobservatory.nasa.gov/world-of-change/DecadalTemp)

**Urban Heat Island (UHI) / Städtischer Hitzeinseleffekt**
Ein Phänomen, bei dem städtische Gebiete aufgrund von dichter Bebauung, Versiegelung und fehlender Vegetation deutlich wärmer sind als ihr ländliches Umland. Globale Klimamodelle unterschätzen diesen Effekt oft, weshalb lokales Downscaling für Städte besonders komplex ist.
*   *Quelle:* [U.S. EPA - Heat Island Effect](https://www.epa.gov/heatislands)

**Kipppunkte (Tipping Points)**
Kritische Schwellenwerte im Klimasystem. Werden sie überschritten, kommt es zu unumkehrbaren und oft abrupten Veränderungen (z.B. Abschmelzen des Grönlandeises). Machine-Learning-Modelle, die nur auf historischen Daten basieren, können solche nie dagewesenen, nicht-linearen Effekte nur schwer vorhersagen.
*   *Quelle:* [Potsdam-Institut für Klimafolgenforschung (PIK) - Kippelemente](https://www.pik-potsdam.de/de/produkte/infothek/kippelemente)

**Pluviales und Fluviales Hochwasser**
*   **Pluvial:** Hochwasser durch extremen Starkregen, der die Kanalisation oder Böden überlastet (kann überall auftreten).
*   **Fluvial:** Hochwasser durch übertretende Flüsse nach langanhaltendem Regen oder Schneeschmelze.
*   *Hinweis:* Unser Modell fokussiert sich primär auf küstennahe Überflutungen durch Meeresspiegelanstieg und deckt diese Binnenhochwasser-Arten nicht vollständig ab.

---

## 🤖 Machine Learning & Data Science (Die „A-Phasen“)

**Algorithmus**
In unserem Kontext ein „Rezept“ für den Computer. Es ist eine mathematische Rechenvorschrift, die aus historischen Daten lernt. Wir testen verschiedene Algorithmen (z.B. *Lineare Regression*, *Random Forest*), um zu sehen, welcher die Zusammenhänge zwischen CO₂ und Temperatur am besten versteht.
*   *Quelle:* [IBM - What is Machine Learning?](https://www.ibm.com/topics/machine-learning)

**Training & Testen (Train-Test-Split)**
Wir geben dem Modell nie *alle* Daten zum Lernen. Wir behalten einen Teil (z.B. die jüngsten 20% der Jahre) zurück („Testdaten“). Das Modell lernt mit den alten Daten („Trainingsdaten“) und muss dann beweisen, dass es die Testdaten korrekt vorhersagen kann, ohne sie vorher gesehen zu haben. Dies verhindert, dass das Modell die Daten nur auswendig lernt.
*   *Quelle:* [Scikit-Learn Documentation - Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

**Features (Merkmale)**
Die „Zutaten“, mit denen wir das Modell füttern. Es sind die messbaren Eigenschaften, die zur Vorhersage genutzt werden.
*   *Beispiel:* Um die Temperatur von morgen vorherzusagen, könnten Features sein: „Temperatur heute“, „CO₂-Konzentration aktuell“.
*   **Lag-Features (Verzögerung):** Ein spezielles Feature. Da das Klima träge ist (wie ein schwerer Güterzug), wirkt sich CO₂ von heute erst später voll aus. Lag-Features berücksichtigen diese Verzögerung (z.B. „CO₂-Wert von vor 5 Jahren“).
*   *Quelle:* [Machine Learning Mastery - Feature Engineering for Time Series](https://machinelearningmastery.com/basic-feature-engineering-time-series-data-python/)

**Hyperparameter**
Die „Einstellungen am Backofen“. Während der Algorithmus das Rezept ist, sind Hyperparameter die Feinjustierungen, die *vor* dem Training festgelegt werden müssen (z.B. wie stark soll das Modell bestraft werden, wenn es zu komplex wird? = `alpha` bei der Ridge-Regression). Wir optimieren diese systematisch (z.B. per Grid Search), um das bestmögliche Ergebnis zu erzielen.
*   *Quelle:* [Towards Data Science - Understanding Hyperparameters](https://towardsdatascience.com/understanding-hyperparameters-and-its-optimisation-techniques-f0debba07568)

**Overfitting (Überanpassung) & Data Leakage**
*   **Overfitting:** Das Modell lernt die Trainingsdaten *zu* gut auswendig (inklusive Rauschen und Fehlern), anstatt die allgemeinen Regeln zu verstehen. Es versagt dann bei neuen Daten.
*   **Data Leakage:** Ein schwerer Fehler, bei dem Informationen aus den Testdaten versehentlich ins Training fließen (z.B. durch falsches Skalieren vor dem Aufteilen). Das Modell "schummelt" und wirkt besser, als es ist.
*   *Quelle:* [Kaggle - Data Leakage](https://www.kaggle.com/code/alexisbcook/data-leakage)

---

## 📊 Messgrößen der Genauigkeit

**RMSE (Root Mean Square Error)**
Unser wichtigstes Maß für die Genauigkeit bei Temperatur- und Meeresspiegelvorhersagen.
*   Er berechnet die Wurzel aus dem Durchschnitt der quadrierten Vorhersagefehler.
*   Er gibt an, um wie viel Grad (oder cm) das Modell im Durchschnitt daneben liegt. Große Ausreißer werden durch das Quadrieren stärker bestraft.
*   **Ziel:** Wir wollen einen RMSE von unter **0,2 °C**. Das bedeutet, unsere Vorhersage weicht durchschnittlich weniger als 0,2 Grad vom tatsächlichen Wert ab.
*   *Quelle:* [Statology - RMSE](https://www.statology.org/root-mean-square-error-python/)

**R² (Bestimmtheitsmaß / R-Squared)**
Ein statistischer Wert zwischen 0 und 1 (oder 0% und 100%). Er sagt aus, wie viel Prozent der Varianz (Schwankungen) in der Zielgröße durch unser Modell erklärt werden kann.
*   Ein R² von 0,95 bedeutet: Das Modell erklärt 95% der Temperaturveränderungen korrekt durch die eingegebenen Features (wie CO₂).
*   *Quelle:* [Investopedia - R-Squared](https://www.investopedia.com/terms/r/r-squared.asp)

**Konfidenzintervall (Unsicherheitsbereich)**
Ein statistischer Bereich, der angibt, mit welcher Wahrscheinlichkeit der wahre Wert innerhalb bestimmter Grenzen liegt. Da Klimaprognosen nie 100% sicher sind, geben wir statt eines absoluten Wertes (z.B. "15 Hitzetage") oft einen Bereich an (z.B. "10 bis 22 Hitzetage mit 90% Wahrscheinlichkeit"). Dies verhindert eine falsche Scheingenauigkeit.
*   *Quelle:* [Statista - Konfidenzintervall](https://de.statista.com/statistik/lexikon/definition/76/konfidenzintervall/)

---

## 🗺️ IT & Geodaten (Die „K-Phase“ / App-Entwicklung)

**Copernicus DEM (GLO-30) & COG**
Ein digitales Höhenmodell (DEM = Digital Elevation Model) mit einer Auflösung von 30 Metern. In unserem Dashboard verarbeiten wir diese Daten live im modernen *Cloud Optimized GeoTIFF (COG)*-Format direkt aus einer öffentlichen *AWS S3 Public Registry* via `rasterio` und `boto3`. Dies umgeht Rate-Limits offener APIs.

**PyDeck (PolygonLayer)**
Die 3D-Kartenbibliothek, die wir im Streamlit-Frontend verwenden, um Datenlücken zu schließen und Raster sauber zu visualisieren. Über `PolygonLayer` zeichnen wir ein geografisch exaktes, durchgängiges Raster ohne Lücken oder Verzerrungen (im Gegensatz zu einfachen Zylinder-Säulen oder starren Quadraten).

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
