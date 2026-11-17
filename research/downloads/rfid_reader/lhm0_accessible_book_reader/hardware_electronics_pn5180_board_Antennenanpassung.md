# Antennenanpassung in drei Schritten

Dieses Dokument beschreibt die Berechnung einer Antennenanpassung anhand der Formeln aus `NXP_antenna_matching.xls`, Arbeitsblatt `Tuning`. Die Berechnung gliedert sich in die Beschreibung der Antenne, die Dimensionierung des EMC-Filters und die Berechnung des Matching Circuit.

Die Antenne wird über ihre Spuleninduktivität beschrieben. Geometrieparameter einer PCB-Spule wie Leiterbahnbreite, Windungsabstand oder Platinenabmessungen werden nicht benötigt. Die Induktivität kann aus einer Messung, einem Datenblatt oder einer separaten Berechnung stammen.

Die Formeln übernehmen das symmetrische Modell der Vorlage mit einem differentiellen Anschluss zwischen Tx1 und Tx2. Die Faktoren 2 und 1/2 gehören zu diesem Modell und dürfen bei einer anderen Schaltungstopologie nicht ungeprüft übernommen werden. Die genaue Verdrahtung und die Zuordnung der Kondensatoren C1 und C2 sind dem zugehörigen Schaltbild zu entnehmen.

## Eingangsgrößen und Einheiten

| Symbol | Bedeutung | Verwendung |
|---|---|---|
| $f$ | Betriebsfrequenz | Alle drei Schritte |
| $L_a$ | Induktivität der Antennenspule | Antenne und Matching |
| $Q$ | Gewünschte belastete Antennengüte | Antenne |
| $R_a$ | Serienverlustwiderstand der Spule bei der Betriebsfrequenz, sofern bekannt | Eigengüte und Dämpfungswiderstände |
| $C_a$ | Parasitäre Antennenkapazität, sofern berücksichtigt | Matching; im vereinfachten Modell null |
| $f_E$ | Gewählte charakteristische Frequenz des EMC-Filters | EMC-Filter |
| $L_0$ | Gewählte Filterinduktivität gemäß Schaltungstopologie der Vorlage | EMC-Filter |
| $R_m$ | Gewünschter differentieller Anpassungswiderstand zwischen Tx1 und Tx2 | Matching |

Alle Formeln verwenden SI-Einheiten: Frequenzen in Hz, Induktivitäten in H, Kapazitäten in F und Widerstände in Ω. Die Güte $Q$ ist dimensionslos.

$$
1\,\mathrm{MHz}=10^6\,\mathrm{Hz},\qquad
1\,\mathrm{nH}=10^{-9}\,\mathrm{H},\qquad
1\,\mathrm{pF}=10^{-12}\,\mathrm{F}
$$

## Schritt 1: Antenne

### 1.1 Spuleninduktivität und Betriebsfrequenz festlegen

Die zentrale Antenneneingangsgröße ist die Spuleninduktivität $L_a$. Zunächst wird aus der Betriebsfrequenz die Kreisfrequenz berechnet:

$$
\boxed{\omega=2\pi f}
$$

Der induktive Blindwiderstand der Spule bei dieser Frequenz lautet:

$$
X_a=\omega L_a
$$

### 1.2 Gewünschte Güte festlegen

Zusätzlich zur Induktivität wird eine Zielgüte $Q$ vorgegeben. Damit ergibt sich der im Modell erforderliche gesamte Serienwiderstand:

$$
\boxed{R_{s,\mathrm{soll}}=\frac{\omega L_a}{Q}}
$$

Die Induktivität allein bestimmt somit noch keine eindeutige Anpassung. Betriebsfrequenz und Zielgüte sind ebenfalls erforderlich.

### 1.3 Dämpfungswiderstände bestimmen, sofern der Spulenverlust bekannt ist

Ist der Serienverlustwiderstand $R_a$ bekannt, kann zunächst die Eigengüte der Spule berechnet werden:

$$
Q_a=\frac{\omega L_a}{R_a}
$$

Die Vorlage berücksichtigt zwei gleiche zusätzliche Serienwiderstände $R_q$. Es gilt:

$$
R_a+2R_q=R_{s,\mathrm{soll}}
$$

Daraus folgt für jeden der beiden Widerstände:

$$
\boxed{R_q=\frac12\left(\frac{\omega L_a}{Q}-R_a\right)}
$$

Ohne Kenntnis von $R_a$ lässt sich der erforderliche Gesamtwiderstand angeben, aber kein verlässlicher Wert für die tatsächlich hinzuzufügenden Dämpfungswiderstände. Die Annahme $R_a=0$ ist nur ein idealisiertes Spulenmodell. Ergibt sich $R_q<0$, kann die gewünschte Güte mit zusätzlichen passiven Serienwiderständen nicht erreicht werden.

### 1.4 Ersatzwiderstand für die Matching-Berechnung

Die Vorlage berechnet den parallelen Ersatzwiderstand mit:

$$
R_{pa}=\frac{(\omega L_a)^2}{R_a+2R_q}
$$

Durch Einsetzen des auf die Zielgüte abgestimmten Serienwiderstands ergibt sich:

$$
\boxed{R_{pa}=Q\,\omega L_a}
$$

Damit benötigt die weitere Matching-Berechnung im Modell nur $L_a$, $f$ und $Q$. Der Verlustwiderstand bleibt für die praktische Dimensionierung von $R_q$ und die Erreichbarkeit der Zielgüte relevant.

Die Formel für $R_{pa}$ wird unverändert aus der Vorlage übernommen. Bei einer exakten Serien-Parallel-Umrechnung einer isolierten RL-Reihenschaltung wäre $R_p=R_s+(\omega L_a)^2/R_s$. Die Vorlage lässt den Summanden $R_s$ weg und verwendet damit die Näherung für hohe Güte.

**Ergebnis von Schritt 1:** Kreisfrequenz $\omega$, Ersatzwiderstand $R_{pa}$ und, bei bekanntem Spulenverlust, die beiden Dämpfungswiderstände $R_q$.

## Schritt 2: EMC-Filter dimensionieren

### 2.1 Filterfrequenz und Induktivität wählen

Die Eingangsgrößen dieses Schritts sind die gewünschte Filterfrequenz $f_E$ und die gewählte Induktivität $L_0$.

**Zur Bedeutung der Filterkante:** Die Excel-Vorlage bezeichnet diese Frequenz als „fres filter“ und berechnet sie als LC-Resonanzfrequenz. In diesem Dokument ist $f_E$ deshalb die charakteristische LC-Frequenz zur Dimensionierung. Eine tatsächliche −3-dB-Grenzfrequenz ist damit nicht automatisch festgelegt; diese hängt auch von Beschaltung und Belastung ab.

### 2.2 Erforderliche Filterkapazität berechnen

Aus der Resonanzbedingung

$$
f_E=\frac{1}{2\pi\sqrt{L_0C_{0,\mathrm{soll}}}}
$$

folgt:

$$
\boxed{C_{0,\mathrm{soll}}=\frac{1}{(2\pi f_E)^2L_0}}
$$

### 2.3 Reale Kondensatorwerte auswählen

Die Vorlage bildet die wirksame Filterkapazität als Summe zweier gewählter Werte:

$$
\boxed{C_0=C_{01}+C_{02}}
$$

Die Werte werden so gewählt, dass ihre Summe möglichst nahe am berechneten Sollwert liegt. Für alle nachfolgenden Berechnungen wird diese tatsächlich gewählte Summe eingesetzt.

Die dadurch resultierende charakteristische Filterfrequenz ist:

$$
\boxed{f_{E,\mathrm{real}}=\frac{1}{2\pi\sqrt{L_0(C_{01}+C_{02})}}}
$$

**Ergebnis von Schritt 2:** Gewählte Filterbauteile $L_0$, $C_{01}$ und $C_{02$, ihre wirksame Kapazität $C_0$ sowie die daraus resultierende Filterfrequenz.

## Schritt 3: Matching Circuit berechnen

Das Matching wird bei der Betriebsfrequenz $f$ berechnet, nicht bei der Filterfrequenz $f_E$. Benötigt werden $\omega$ und $R_{pa}$ aus Schritt 1, die gewählten Filterwerte aus Schritt 2 sowie der gewünschte differentielle Anpassungswiderstand $R_m$.

### 3.1 Hilfsgrößen des Filters

Zunächst werden zwei dimensionslose Größen berechnet:

$$
a=1-\omega^2L_0C_0
$$

$$
b=\frac{\omega R_mC_0}{2}
$$

Ihr gemeinsamer quadratischer Nenner lautet:

$$
D=a^2+b^2
$$

### 3.2 Transformierten Widerstand und transformierte Reaktanz berechnen

Der im Tabellenmodell durch den Filter transformierte Widerstand lautet:

$$
\boxed{R_{\mathrm{tr}}=\frac{R_m}{D}}
$$

Die zugehörige Reaktanz lautet:

$$
\boxed{X_{\mathrm{tr}}=
2\omega\frac{L_0a-\dfrac{R_m^2C_0}{4}}{D}}
$$

Beide Ergebnisse haben die Einheit Ω.

### 3.3 Matching-Kondensator C1

Zur Vereinfachung der Schreibweise wird definiert:

$$
S=\sqrt{\frac{R_{\mathrm{tr}}R_{pa}}{4}}
$$

Damit ergibt sich:

$$
\boxed{C_1=\frac{1}{\omega\left(S+\dfrac{X_{\mathrm{tr}}}{2}\right)}}
$$

Ausgeschrieben:

$$
C_1=\frac{1}{\omega\left(
\sqrt{\dfrac{R_{\mathrm{tr}}R_{pa}}{4}}
+\dfrac{X_{\mathrm{tr}}}{2}\right)}
$$

### 3.4 Matching-Kondensator C2

Mit einer gegebenenfalls berücksichtigten parasitären Antennenkapazität $C_a$ gilt:

$$
\boxed{C_2=\frac{2}{\omega^2L_a}-\frac{1}{\omega S}-2C_a}
$$

Wird die Antenne vereinfacht allein über ihre Induktivität modelliert, wird ausdrücklich $C_a=0$ angenommen:

$$
\boxed{C_2=\frac{2}{\omega^2L_a}-\frac{1}{\omega S}}
$$

Diese Vereinfachung vermeidet zusätzliche Antennenparameter. Sie bedeutet nicht, dass die reale Spule keine parasitäre Kapazität besitzt.

### 3.5 Bauteilwerte verwenden

Die Formeln liefern $C_1$ und $C_2$ in F. Zur Darstellung in pF werden die Zahlenwerte mit $10^{12}$ multipliziert.

Positive, endliche Ergebnisse sind Voraussetzung für die Umsetzung mit den vorgesehenen Kondensatoren. Bei einem nicht positiven Nenner für $C_1$ oder einem negativen Wert für $C_2$ liefern die gewählten Vorgaben keine entsprechende positive Kondensatorlösung. Dann müssen die Vorgaben oder die Schaltungstopologie überprüft werden.

**Ergebnis von Schritt 3:** Berechnete Kondensatorwerte $C_1$ und $C_2$. Nach der Auswahl verfügbarer Bauteilwerte ist die reale Anpassung unter Berücksichtigung der Bauteiltoleranzen zu überprüfen.

## Durchgerechnetes Beispiel

Die folgenden Werte entsprechen den Eingaben der Excel-Vorlage. Es werden keine geometrischen PCB-Spulenparameter verwendet.

| Eingangsgröße | Wert |
|---|---:|
| Betriebsfrequenz $f$ | 13,56 MHz |
| Spuleninduktivität $L_a$ | 1204 nH |
| Zielgüte $Q$ | 25 |
| Spulenverlustwiderstand $R_a$ | 1,8 Ω |
| Angenommene parasitäre Kapazität $C_a$ | 0 pF |
| Gewünschte Filterfrequenz $f_E$ | 21 MHz |
| Filterinduktivität $L_0$ | 470 nH |
| Gewählte Filterkapazitäten $C_{01}$ und $C_{02}$ | 68 pF und 56 pF |
| Differentieller Anpassungswiderstand $R_m$ | 20 Ω |

| Schritt | Berechnete Größe | Ergebnis |
|---|---|---:|
| 1 | $\omega$ | 85 199 992,77 s⁻¹ |
| 1 | $Q_a$ | 56,9893 |
| 1 | $R_{s,\mathrm{soll}}$ | 4,10323 Ω |
| 1 | $R_q$, je Widerstand | 1,15162 Ω |
| 1 | $R_{pa}$ | 2564,5198 Ω |
| 2 | $C_{0,\mathrm{soll}}$ | 122,2092 pF |
| 2 | $C_0$, gewählt | 124 pF |
| 2 | $f_{E,\mathrm{real}}$ | 20,8478 MHz |
| 3 | $a$ | 0,576943 |
| 3 | $b$ | 0,105648 |
| 3 | $R_{\mathrm{tr}}$ | 58,1353 Ω |
| 3 | $X_{\mathrm{tr}}$ | 128,1688 Ω |
| 3 | $C_1$ | **45,6439 pF** |
| 3 | $C_2$ | **168,0411 pF** |

## Zuordnung zur Excel-Vorlage

| Berechnung oder Eingabe | Zelle(n) in `Tuning` |
|---|---|
| $f$, $\omega$ | C3, C4 |
| $L_a$, $C_a$, $R_a$ | C7, C8, C9 |
| $Q$, $R_m$, $f_E$ | C12, C13, C14 |
| $Q_a$, $R_q$, $R_{pa}$ | C17, C18, C20 |
| Kopie von $R_{pa}$ für die Matching-Formeln | C21 |
| $L_0$, $C_{0,\mathrm{soll}}$ | C24, C25 |
| $C_{01}$, $C_{02}$ | C27, C28 |
| $f_{E,\mathrm{real}}$ | F14 |
| $a$, $a^2$, $b$, $b^2$ | H7, I7, J7, K7 |
| $R_{\mathrm{tr}}$, $X_{\mathrm{tr}}$ | C30, C31 |
| $C_1$, $C_2$ | C34, C35 |

Die Größen $X_a$, $R_{s,\mathrm{soll}}$, $D$ und $S$ sind erklärende Abkürzungen dieses Dokuments. Sie sind keine zusätzlichen Eingaben. In der Vorlage wird der Sollwert C25 nicht automatisch in die gewählten Kondensatorwerte C27 und C28 übernommen.
