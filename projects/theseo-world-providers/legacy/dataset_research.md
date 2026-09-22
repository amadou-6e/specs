
Öffentlich verfügbare Datensätze für 3D‑Routing mit STL‑Szenen und Ground‑Truth‑3D‑Pfaden
Executive Summary
Für die enge Anforderungskombination (i) Szenengeometrie als .stl und (ii) Ground‑Truth‑3D‑Pfade (Centerlines/Skeletons) in Weltkoordinaten existieren öffentlich verfügbare Datensätze – allerdings fast ausschließlich in Domänen, in denen „Routing eines langen flexiblen Objekts“ natürlich als Katheter-/Guidewire‑Navigation in Gefäßlumen oder als geometrische Centerline‑Analyse auftritt. Ein dezidierter Open‑Dataset‑Standard für Kabel-/Draht-/Rohr‑Routing in industriellen 3D‑Umgebungen mit .stl‑Obstakeln und annotierten 3D‑Routen ist in den hier geprüften Primärquellen nicht nachweisbar; diese Lücke bleibt zentral.

Was die Kernforderung am klarsten erfüllt:

AAA‑100 (Zenodo) liefert pro Fall .stl‑Oberflächen und Centerlines als .vtp; explizit wird angegeben, dass Modelle und Centerlines in Weltkoordinaten (mm) der CTA‑Scans bereitgestellt werden. 
AneuriskData (GitHub‑Mirror) enthält pro Fall model.stl und centerlines.csv/centerlines.vtp; die Koordinatenreferenz ist in den Repos nicht spezifiziert, weshalb „Weltkoordinaten“ nicht belegt werden kann. 
ASOCA (Koronar‑CTCA) bietet .stl‑Meshes und Centerlines als .vtp für 40 Fälle (20 normal/20 diseased); die Datensatzbeschreibung nennt die Modalitäten und die Dateiformate, die Koordinatenreferenz der Centerlines ist in den zitierten Quellen nicht explizit als „world coordinates“ formuliert. Der aktuelle Download ist zudem zugangsbeschränkt über UK Data Service. 
AneuX morphology database (Zenodo) erwähnt in der Content‑Beschreibung, dass Oberflächen und Centerlines in VTP oder STL gespeichert sind; Details zur Koordinatenreferenz und zur „Routing‑Eignung“ als Pfad‑GT in frei befahrbarem Raum sind nicht spezifiziert. 
Für (b) „zu STL+3D‑Pfad GT konvertierbar“ sind besonders stark:

4D‑CTA AAA (Zenodo): STL‑Modelle + NRRD‑Zeitserien; Centerlines fehlen, sind aber gut automatisierbar (z. B. über VMTK). 
AAA‑Stress/FE (Mendeley Data DOI): STL‑Geometrien + Bilddaten + FE‑Modelle; Centerlines fehlen. 
Für (c) Sim‑to‑Real eignet sich eine Kombination aus synthetischem Centerline‑Datensatz (z. B. SynthAorta, liefert Skelette/Centerlines, aber kein STL) und realen CTA‑basierten STL‑Datensätzen (AAA‑100, ASOCA, AneuriskData). 

Auswahlkriterien und Abgrenzung
Als „geeignet“ wurden Datensätze gewertet, wenn Primärquellen explizit belegen:

Szenen-/Umgebungsgeometrie als .stl (oder als andere Meshformate, die zuverlässig nach STL konvertierbar sind).
Ground‑Truth‑3D‑Pfade als explizite 3D‑Polylines (Centerlines/Skeletons/Graph‑Kanten) – idealerweise in Weltkoordinaten.
Für „nahe Matches“ wurden Datensätze aufgenommen, die nur (1) oder nur (2) erfüllen, wenn eine robuste Konvertierungs-/Annotierungsstrategie existiert.
Wichtig: In vielen medizinischen Datensätzen ist die Geometrie implizit an die physikalischen Scan‑Koordinaten gebunden (Spacing/Origin). Wenn dies nicht ausdrücklich im Datensatztext bestätigt wird, wird das Attribut strikt als „nicht spezifiziert“ markiert.

Datensätze mit STL‑Meshes und 3D‑Pfaden
AAA‑100: A Curated Dataset of 3D Watertight Abdominal Aortic Aneurysm Models
Name: AAA‑100 

Autoren/Owner: Patryk Rygiel, Dieuwertje Alblas, Christoph Brune, Stefan Smorenburg, Kak Khee Yeung, Jelmer M. Wolterink; Affiliations u. a. University of Twente und Amsterdam UMC Location VUmc. 

Jahr: 2024 (Zenodo‑Publikation; Version 0.1.0). 

Lizenz: CC BY‑NC 4.0. 

Datenmodalitäten (vorhanden/fehlend)

.stl‑Meshes: ja (pro Fall triangulierte .stl‑Surface‑Meshes). 
Andere Meshformate: nicht spezifiziert (neben .stl sind Centerlines als .vtp explizit). 
Point Clouds: nicht spezifiziert
RGB/RGB‑D: nein (nicht angegeben)
Simulation Logs: nicht spezifiziert
Force/Torque: nicht spezifiziert
Contact Maps: nicht spezifiziert
Größe: 100 AAA‑Modelle; in der Datensatzstruktur IDs AAA001–AAA100. 

Annotationen

GT‑3D‑Pfade/Centerlines: ja (Centerlines als separate .vtp pro Gefäßast). 
Kollisionslabels: nicht spezifiziert
Kontaktpunkte: nicht spezifiziert
Deformationsfelder: nein (nicht angegeben)
Koordinaten: explizit „world coordinates (mm) der CTA‑Scans“ für Meshes und Centerlines. 

Eignung für Routing/Planung: Sehr hoch als Korridor‑Routing‑Benchmark (Centerline ≙ Referenzroute durch ein enges 3D‑Lumen). Für echtes „flexibles Objekt“ kann man die Route als diskretisierte DLO‑Mittellinie interpretieren. Für Sim‑to‑Real eingeschränkt, da (in der beschriebenen Version) die Bilddaten selbst nicht enthalten sind. 

Umgebungstyp: real (CTA‑abgeleitete patientenspezifische Geometrien). 

Sensorik: CTA (Bilddaten nicht mitgeliefert; Scanparameter beschrieben). 

Code/Tools: Datensatz verlinkt auf begleitende Arbeiten; Verarbeitung/Extraktion in der Beschreibung erläutert, konkreter Code im Zenodo‑Eintrag nicht spezifiziert. 

Benchmarks/Metriken: Topologische Validität wird über Betti‑Zahlen/Euler‑Charakteristik thematisiert; keine dedizierte Path‑Planning‑Benchmark‑Suite ausgewiesen. 

Bekannte Limitierungen (laut Beschreibung): kein Thrombus, keine Bilddaten, Patientenkohorte EVAR‑selektiert (Bias möglich). 

AneuriskData (GitHub‑Mirror des Aneurisk‑Repositories)
Name: AneuriskData (Mirror) 

Owner/Quelle: GitHub‑Repo verweist auf AneuriskWeb; Mirror/Repo‑Owner im README nicht weiter spezifiziert. 

Jahr: nicht spezifiziert (GitHub‑Repo selbst enthält kein Publikationsjahr im README; Aneurisk‑Projektzeitraum nicht in diesen Quellen ausformuliert). 

Lizenz: CC BY‑NC 3.0. 

Datenmodalitäten (vorhanden/fehlend)

.stl‑Meshes: ja (model.stl pro Fall/Segment). 
Andere Meshformate: ja (model.vtp). 
3D‑Pfade: ja (centerlines.vtp und centerlines.csv). 
DICOM/Volumina/Labels: ja (Ordner dicom, volumes, labels). 
RGB/RGB‑D: nicht spezifiziert
Simulation Logs / Force/Torque / Contact Maps: nicht spezifiziert
Größe: Im models/‑Verzeichnis sind mindestens 24 Fall‑Ordner sichtbar (z. B. C0001…C0076). 

Annotationen

GT‑3D‑Pfade/Centerlines: ja (centerlines.csv, centerlines.vtp). 
Kollisionslabels/Kontaktpunkte/Deformationsfelder: nicht spezifiziert
Koordinaten: nicht spezifiziert (es ist nicht explizit dokumentiert, ob die Centerlines in Scan‑Weltkoordinaten, Mesh‑Koordinaten oder normalisierten Koordinaten vorliegen). 

Eignung für Routing/Planung: Hoch für „Routing im engen Lumen“ (Centerline als Referenzroute) und gut für Sim‑to‑Real‑Pipelines, weil DICOM/Volumen/Labels vorhanden sind. 

Umgebungstyp: real (Bilddaten/Segmentierung/Modelle). 

Sensorik: DICOM‑Bildserien (Modalität nicht spezifiziert). 

Code/Tools: nicht spezifiziert
Benchmarks/Metriken: nicht spezifiziert
Limitierungen: Mirror‑Struktur ist nicht als „Benchmark“ kuratiert (kein standardisiertes Start‑Ziel‑Set, keine expliziten Planungsmetriken). (Ableitung aus bereitgestellter Struktur; keine zusätzliche Benchmarkbeschreibung im Repo.) 

ASOCA: Annotated CT Coronary Angiogram Images … (Koronararterien)
Name: ASOCA (Automated Segmentation of Coronary Arteries Challenge / Dataset) 

Autoren/Owner: Datensatz‑Creators u. a. Ramtin Gharleghi und Susann Beier; Affiliation u. a. University of New South Wales. 

Jahr: Datensatzbeschreibung/Preprint 2022; Datensatz‑Eintrag nennt Veröffentlichung (in UK Data Service) 2022, zuletzt modifiziert 2024. 

Lizenz: UK Data Service End User Licence (Downloadpakete); Dokumentation CC BY‑SA 4.0. 

Datenmodalitäten (vorhanden/fehlend)

.stl‑Meshes: ja („SurfaceMeshes … provided in STL format“). 
Andere Meshformate: nicht spezifiziert
3D‑Pfade/Centerlines: ja (VTP‑Centerlines pro Patient). 
Bilddaten: ja (CTCA als NRRD; DICOM erwähnt im Prozess). 
Point Clouds / RGB/RGB‑D: nicht spezifiziert
Simulation Logs / Force/Torque / Contact Maps: nicht spezifiziert
Größe: 40 Patientenfälle (20 normal, 20 diseased) als Trainingsdatensatz; zusätzlich 20 CTCA‑Fälle als Testset ohne GT‑Annotationen/Centerlines. 

Annotationen

GT‑3D‑Pfade/Centerlines: ja (.vtp) 
Voxel‑GT‑Segmentierungen: ja (Mehrheitsvotum aus 3 Experten). 
Kollisionslabels/Kontaktpunkte/Deformationsfelder: nicht spezifiziert
Koordinaten: Weltkoordinaten der Paths: nicht spezifiziert (der Datensatz beschreibt Anisotropie/Spacing der NRRD‑Volumina; eine explizite „world coordinates“‑Aussage für Centerlines in den zitierten Textstellen fehlt). 

Eignung für Routing/Planung: Sehr hoch als realer Datensatz für „Pfad im engen 3D‑Lumen“, mit zusätzlicher Option, aus Volumen→Mesh neue Geometrien zu rekonstruieren (z. B. andere Glättung/Extensions). Ein Plus ist die dokumentierte Toolchain (3D Slicer, VMTK). 

Umgebungstyp: real (klinische CTCA). 

Sensorik: CTCA (Scanner/ECG‑Gating in Beschreibung). 

Code/Tools:

Evaluations-/Hilfsrepo: ASOCADataDescription (GitHub, enthält u. a. Skript). 
In der Datensatzbeschreibung: 3D Slicer + VMTK werden für Annotation/Glättung/Centerline‑Extraktion genannt. 
Benchmarks/Metriken: Für Segmentierung werden DSC und (95‑Perzentil) Hausdorff Distanz berichtet. 

Limitierungen: Zugriff über UK Data Service ist genehmigungspflichtig (Closed access). 

AneuX morphology database
Name: AneuX morphology database 

Creators: Norman Juchler, Philippe Bijlenga, Sven Hirsch; Affiliations u. a. Zurich University of Applied Sciences und Geneva University Hospital and Faculty of Medicine. 

Jahr: 2022 (Zenodo‑Publikation). 

Lizenz: CC BY‑NC 4.0 (mit zusätzlichen Zitations-/Deklarationsanforderungen). 

Datenmodalitäten (vorhanden/fehlend)

.stl‑Meshes: ja (in der Content‑Beschreibung: Geometrien in VTP oder STL). 
Andere Meshformate: ja (VTP). 
Centerlines/Skeletons: ja (Content‑Beschreibung nennt Centerlines). 
Point Clouds/RGB/RGB‑D/Simulation/Force/Contact Maps: nicht spezifiziert
Größe: 750 Aneurysma‑Domes und 668 Vessel Trees (Surface Meshes). 

Annotationen (für Routing relevant)

GT‑3D‑Pfade/Centerlines: ja (Existenz/Formate belegt; semantische Bedeutung pro Fall nicht weiter spezifiziert). 
Klinische Parameter/Morphometrie: ja (170 Indizes; 5 klinische Parameter). 
Kollisionslabels/Kontaktpunkte/Deformationsfelder: nicht spezifiziert
Koordinaten: nicht spezifiziert (keine explizite Aussage zu Weltkoordinaten). 

Eignung für Routing/Planung: Gut als größerer Korpus von STL/VTP‑Gefäßgeometrien mit Centerlines (Routing‑Surrogat). Für echte Path‑Planning‑Benchmarks fehlen standardisierte Start/Ziel‑Definitionen und kollisions-/kontaktbezogene Labels (nicht spezifiziert). 

Nahe Alternativen für Konvertierung zu STL + 3D‑Pfad‑GT
4D‑CTA Images and Surface Models of Abdominal Aortic Aneurysms from Ten Patients
Name: 4D‑CTA Images and Surface Models … 

Creators: Mostafa Jamshidian, Adam Wittek, u. a. (Zenodo listet die vollständigen Creators). 

Jahr: 2025 (Zenodo‑Publikation). 

Lizenz: CC BY 4.0. 

Modalitäten

.stl‑Meshes: ja (AAA‑Surface‑Models; Dateiformate ausdrücklich NRRD + STL). 
Centerlines: nein (nicht erwähnt)
Bildsequenzen: ja (zeitaufgelöste 3D‑CTA‑NRRD). 
Deformations-/Displacement‑GT: „synthetic ground truth“ für Patient 1 (Displacement Field via biomech. Modell; Details als Bestandteil des Datensatzes beschrieben). 
Force/Torque/Contact Maps: nicht spezifiziert
Größe: 10 Patienten; pro Patient typischerweise 10 ECG‑gegatete 3D‑Frames; ZIP‑Bundle ~81.8 MB im Zenodo‑Eintrag. 

Eignung: Sehr gut als Real‑World‑Geometriequelle in STL, um nachträglich Centerlines als GT‑Pfade zu extrahieren (automatisierbar). Zusätzlich interessant für dynamische „Routing unter Deformation“ (Zeitphasen); jedoch fehlen direkte Centerline‑Annotationen. 

Data for: Is There a Relationship Between Stress in Walls of AAA and Symptoms? (Mendeley Data)
Name: Data for: Is There A Relationship Between Stress … 

Creator: Adam Wittek (mit weiteren Contributors). 

Jahr: 2021 (Date made available). 

Lizenz: CC BY‑NC 3.0 (Access Dataset). 

Modalitäten

.stl‑Meshes: ja (discretised surfaces in STL). 
Bilddaten: ja (anonymised image‑sets; Format nicht spezifiziert auf dieser Seite) 
FE‑Modelle: ja (patient‑specific finite element models). 
Centerlines: nein (nicht erwähnt)
Größe: 19 Patienten (implizit „all 19 patients … analysed“). 

Eignung: Sehr gut als STL‑Quelle für enge 3D‑Gefäßumgebungen; Centerlines lassen sich mit etablierten Tools extrahieren (siehe Workflow unten). 

SynthAorta Dataset
Name: SynthAorta Dataset 

Creators: Domagoj Bošnjak, Gian Marco Melito, Katrin Ellermann, Thomas‑Peter Fries. 

Jahr: 2025 (Repository record, Version 1.1; modifiziert 2025‑12). 

Lizenz: GPL‑3.0‑or‑later. 

Modalitäten

.stl‑Meshes: nein (nicht angegeben; Output/Beispiele sind .msh, Daten binär). 
Andere Meshformate: ja (.msh, strukturierte Hex‑Meshes). 
Centerlines/Skeletons: ja (Centerlines mit lokalem Radius; explizit für Oberflächen‑Rekonstruktion). 
RGB/RGB‑D/Force/Contact: nicht spezifiziert
Größe: 30 000 synthetische Geometrien (4 Refinement‑Levels). 

Eignung: Sehr gut als synthetische Path‑GT‑Quelle (viele Centerlines), um Sim‑Training zu skalieren. Für die harte .stl‑Anforderung ist Konvertierung nötig (Mesh‑Surface extrahieren/konvertieren). 

Vergleichstabelle
Datensatz	.stl‑Szene	3D‑Pfad‑GT (Centerline/Skeleton)	„World coords“ explizit	Größe	Umgebung	Lizenz	Zugriff
AAA‑100	ja 
ja (.vtp) 
ja (mm) 
100 Fälle 
real	CC BY‑NC 4.0 
offen 
AneuriskData (Mirror)	ja (model.stl) 
ja (centerlines.csv/.vtp) 
nicht spezifiziert 
≥24 Fallordner 
real	CC BY‑NC 3.0 
offen 
ASOCA	ja 
ja (.vtp) 
nicht spezifiziert 
40 train (+20 test img‑only) 
real	UKDS EUL 
genehmigungspflichtig 
AneuX morphology database	ja (VTP oder STL) 
ja (Centerlines) 
nicht spezifiziert 
750 domes, 668 trees 
real/mixed (mehrere Quellen) 
CC BY‑NC 4.0 
offen 
4D‑CTA AAA (10 Pat.)	ja 
nein 
nicht spezifiziert 
10×(~10 Phasen) 
real (zeitaufgelöst) 
CC BY 4.0 
offen 
AAA‑Stress/FE (19 Pat.)	ja 
nein 
nicht spezifiziert 
19 Patienten 
real	CC BY‑NC 3.0 
offen 
SynthAorta	nein (.msh) 
ja (Skelette/Centerlines) 
nicht spezifiziert 
30 000 
synthetisch	GPL‑3.0+ 
offen 

Empfehlungen nach Zielsetzung
Path‑Planning mit .stl‑Szenen und 3D‑Pfad‑GT
Beste Wahl (klare Erfüllung inkl. Weltkoordinaten): AAA‑100. 

Begründung: .stl‑Meshes + .vtp‑Centerlines und explizite Weltkoordinaten, kuratiert/topologisch validiert. 

Sehr brauchbar (STL+Centerline vorhanden; Koordinaten nicht belegt): AneuriskData (Mirror). 

Begründung: pro Fall explizite model.stl und Centerlines; plus Bild-/Volumendaten für eigene Rekonstruktion. 

Stark, aber Zugangshürde: ASOCA. 

Begründung: 40 CTCA‑Fälle mit .stl und .vtp‑Centerlines, plus Segmentierungs‑GT; jedoch aktuell genehmigungspflichtiger Download über UKDS. 

Skalierung (mehr Fälle), aber weniger „Planungs‑Benchmark‑fertig“: AneuX morphology database. 

Begründung: große Geometriesammlung, Centerlines vorhanden; Start/Ziel‑Definitionen und Koordinatenreferenz sind nicht spezifiziert. 

Datensätze zum Konvertieren/Augmentieren zu .stl + 3D‑Pfad‑GT
Geringe Konvertierungsarbeit (STL schon da; Centerline automatisierbar)

4D‑CTA AAA (Zenodo): Centerlines lassen sich aus STL‑Oberfläche oder aus segmentierten Volumina rekonstruieren; Zeitphasen erlauben zudem konsistente Pfade über den Zyklus. 
AAA‑Stress/FE (Mendeley): STL‑Oberflächen + Bilddaten/FE‑Modelle; Centerlines nachträglich extrahierbar. 
Mittlere Konvertierungsarbeit (Centerlines da; STL fehlt/andere Formate)

SynthAorta: Centerlines + strukturierte .msh‑Meshes; man muss zunächst eine Oberfläche extrahieren und als STL exportieren. 
Sim‑to‑Real Path‑Planning
Praktikables Setup aus den gefundenen Quellen:

Sim (synthetisch): SynthAorta (viele Skelette/Centerlines; konvertierbar zu STL‑Surfaces). 
Real (Bild→Mesh→Centerline): ASOCA (CTCA+STL+VTP; Zugang), AneuriskData (DICOM+STL+Centerlines), 4D‑CTA AAA (NRRD+STL, Centerlines selbst erzeugen), AAA‑100 (STL+Centerlines, aber ohne Bilddaten). 
Die Domänenlogik (Gefäßlumen) passt sehr gut zu „Routing eines flexiblen Objekts durch enge 3D‑Räume“ (Katheter ≙ flexibles Langobjekt), auch wenn es kein „Kabelbaum‑Routing“ im CAD‑Sinne ist.

Konkrete Workflows zur Gewinnung von STL‑Meshes und 3D‑Pfad‑Ground‑Truth
Centerline‑Extraction aus vorhandenen STL‑Oberflächen
Für Datensätze mit STL‑Geometrie, aber ohne Pfad‑GT (z. B. 4D‑CTA, AAA‑Stress/FE), ist der Standard‑Weg:

STL‑Surface vorbereiten: Löcher schließen (Capping), ggf. Glättung/Remeshing.
VMTK Centerlines: Das Tool vmtkcenterlines nimmt eine Tubus‑Oberfläche als Input und gibt Centerlines u. a. als VTK‑Objekte aus. 
Export: als .vtp (Polyline/Graph) oder als CSV (XYZ‑Samples), je nach Downstream‑Tooling.
Das ist exakt die Art Pipeline, die auch in ASOCA für die Centreline‑Extraktion beschrieben wird (Inlet/Outlet markieren, VMTK berechnet automatisch). 

Mesh‑Generierung aus Volumen (CT/NRRD/DICOM) → STL
Für Datensätze mit Volumen‑Bilddaten:

Segmentierung (manual/semi‑automatic) → binäre Maske.
Surface‑Extraction: z. B. Marching Cubes/Flying‑Edges (im ASOCA‑Kontext explizit erwähnt). 
Mesh‑Nachbearbeitung: Glättung (Taubin wird im ASOCA‑Workflow genannt), Topologie reparieren, ggf. Extensions/Anschlüsse. 
Export: STL.
3D‑Pfad‑Annotation (wenn Centerline nicht wohldefiniert ist)
Wenn „Pfad“ nicht die Medialachse eines Tubus ist (z. B. Kabel in freiem Raum):

Manuelle Spline‑Annotation: 3D‑Editor/Viewer (Markups‑Kurven) → Sampling in Weltkoordinaten.
Semi‑automatisch:
Abstandsfeld (Signed Distance Field) des Freiraums, dann geodätischer Pfad (z. B. Fast‑Marching/Dijkstra im Voxel‑Gitter) und anschließendes Smoothing.
Für enge Kanäle: Medial‑Axis/Centerline‑Extraktion (VMTK‑artig). 
Voxel‑Benchmarks als Ergänzung (Alternative Geometrieform)
Die Warframe/MovingAI‑Benchmarks liefern 3D‑Voxel‑Maps (44 Karten; textuelles Format mit gefüllten Voxeln) als frei verfügbare Datenbasis für 3D‑Pathfinding. 

Auch wenn das kein STL ist, kann man (a) Voxel→Mesh via Marching Cubes, (b) Pfadprobleme als Start‑Ziel‑Paare definieren und (c) diese als algorithmische GT‑Pfade speichern. Für „flexible Objekte“ ist das nur ein approximatives Surrogat, aber als Benchmark‑Infrastruktur nützlich. 

Evaluationsmetriken und Visualisierungsideen für 3D‑Pfadplanung
Metriken
Für Datensätze mit GT‑Centerline (AAA‑100, AneuriskData, ASOCA, AneuX) lassen sich Pfad‑Planer systematisch bewerten:

Pfadlänge (arc length) und Längenüberschuss gegenüber GT.
Clearance‑Metriken: minimale und mittlere Distanz zur Wand (über SDF zur STL‑Oberfläche).
Kollisionszählung: Anzahl/Integral von Penetrationen bei diskretisiertem Pfad (0 ist Ziel).
Hausdorff/Chamfer‑Distanz zwischen vorhergesagtem Pfad und GT‑Centerline (analoge Idee wird in ASOCA für geometrische Distanzmetriken diskutiert; dort für Segmentierungen/Labels; Prinzip übertragbar). 
Topologische Korrektheit: bei verzweigten Strukturen (Koronarbaum, Nieren-/Iliakalabgänge) – stimmt die Branch‑Sequenz (Graph‑Pfad) mit GT überein?
Krümmungs-/Biegegrenzen: max. Krümmung κ_max als Proxy für „flexibles Objekt mit Biegesteifigkeit“ (wichtig für Kabel/Guidewire‑Modelle).
Dynamische Konsistenz (4D‑CTA): Pfadvariation über Zeitphasen (Stabilität/Tracking‑Fehler), falls man pro Phase einen Pfad plant. 
Visualisierungsideen
Overlay‑Rendering: STL‑Oberfläche halbtransparent, GT‑Centerline vs. Planer‑Pfad farbcodiert.
Clearance‑Heatmap entlang der Pfadparameter s (z. B. Farbe = min distance to wall).
Querschnitts‑Viewer: orthogonale Schnittebenen entlang Centerline; in der Medizin Standard, aber auch für Kabelrouting hilfreich (Engstellen).
Interaktive 3D‑Viewer: VTK‑basierte Viewer oder Web‑Viewer (z. B. glTF‑Export) – besonders nützlich, um Fehlerfälle (falscher Abzweig) schnell zu diagnostizieren.
Mermaid‑Diagramme
mermaid
Kopieren
graph TD
  A[STL+3D-Pfad GT vorhanden] --> AAA100[AAA-100]
  A --> Aneurisk[AneuriskData Mirror]
  A --> ASOCA[ASOCA]
  A --> AneuX[AneuX morphology database]
  B[STL vorhanden, Pfad GT fehlt] --> CTA4D[4D-CTA AAA]
  B --> AAAFE[AAA Stress/FE (Mendeley)]
  C[Pfad GT vorhanden, STL fehlt] --> SynthAorta[SynthAorta]
  D[Voxel-Geometrie statt STL] --> Warframe[3D Voxel Benchmarks (MovingAI)]
Volumen/Scan oder STL

Mesh-Aufbereitung / Repair

Free-Space / Lumen Definition

Centerline-Extraction oder manuelle Spline-Annotation

Train/Test Splits + Start/Ziel-Protokoll

Planner / Policy

Evaluation: Clearance, Collision, Hausdorff/Chamfer, Topologie

Visual Debugging: Overlays + Heatmaps



Code anzeigen
Direkte Download-/Zugriffslinks und Beispiel‑STL
Die folgenden Links sind direkt nutzbar (DOIs/Projektseiten/Repos). Beispiele für einzelne .stl‑Dateien sind enthalten, wo verlässlich verfügbar.

text
Kopieren
AAA-100 (Zenodo Record)
https://zenodo.org/records/10932957
(enthält meshes.zip, centerlines.zip, description.pdf)

AAA-100 Beschreibung (PDF, Inhalt der Struktur inkl. World-Coordinates)
https://www.researchgate.net/profile/Stefan-Smorenburg/publication/381156447_AAA-100_A_Curated_Dataset_of_3D_Watertight_Abdominal_Aortic_Aneurysm_Models/data/665f7a4e0856f96e7f2de19d/description.pdf

AneuriskData (GitHub)
https://github.com/permfl/AneuriskData

Beispiel-STL aus AneuriskData (ein Fall)
https://raw.githubusercontent.com/permfl/AneuriskData/master/models/C0001_models/C0001/surface/model.stl
Beispiel-Centerline (VTP/CSV) aus AneuriskData
https://raw.githubusercontent.com/permfl/AneuriskData/master/models/C0001_models/C0001/morphology/centerlines.vtp
https://raw.githubusercontent.com/permfl/AneuriskData/master/models/C0001_models/C0001/morphology/centerlines.csv

ASOCA (UK Data Service / ReShare – Zugriff genehmigungspflichtig)
https://reshare.ukdataservice.ac.uk/855916/
DOI: https://doi.org/10.5255/UKDA-SN-855916

ASOCA Datensatzbeschreibung (arXiv PDF, Dateiformate u. a. STL+VTP genannt)
https://arxiv.org/pdf/2211.01859

ASOCA Hilfs-/Evaluationsrepo
https://github.com/Ramtingh/ASOCADataDescription

AneuX morphology database (Zenodo Record)
https://zenodo.org/records/6678442

4D-CTA AAA (Zenodo Record – enthält 4DCTA_AAA_Dataset.zip)
https://zenodo.org/records/15477710

AAA Stress/FE (Mendeley Data DOI via UWA Repo)
https://doi.org/10.17632/d3g2v8nthy.1

SynthAorta Dataset (TU Graz Repository)
https://repository.tugraz.at/records/ft6av-k4w55
SynthAorta Code/Repo
https://github.com/domagoj-bosnjak/SynthAorta

3D Voxel Pathfinding Benchmarks (MovingAI)
https://www.movingai.com/benchmarks/
Paper "Benchmarks for Pathfinding in 3D Voxel Space"
https://webdocs.cs.ualberta.ca/~nathanst/papers/voxels.pdf

VMTK Centerline Tutorial/Docs (Centerlines aus Tubus-Oberflächen)
https://www.vmtk.org/tutorials/Centerlines.html
https://www.vmtk.org/vmtkscripts/vmtkcenterlines.html
Empfohlene Suchanfragen und Repositories für die Weiterrecherche
Suchanfragen
"model.stl" "centerlines.vtp" dataset
site:zenodo.org centerlines vtp stl dataset
("centerlines.csv" OR "centerlines.vtp") "model.stl" github
cable routing dataset CAD mesh ground truth path
wire harness routing benchmark dataset stl
rope routing dataset 3D path annotations
catheter navigation dataset stl centerline world coordinates
(de) Datensatz STL Centerline Weltkoordinaten
Repositories/Index‑Quellen, die sich erfahrungsgemäß lohnen
Zenodo (DOI‑stable Datasets; häufig STL/VTP‑Artefakte)
GitHub (Mirrors & Processing‑Pipelines)
PubMed Central (Data‑Descriptor‑Papers mit Dateistrukturen)
Grand‑Challenge‑Plattformen (bei ASOCA relevant) 
Papers With Code (für viele medizinische Geometry‑Datasets existieren jedoch keine dedizierten Dataset‑Landing‑Pages; in dieser Recherche nicht auffindbar für AAA‑100/ASOCA/Aneurisk/AneuX – daher „nicht spezifiziert“)