# Daten zur Use-Case-Wanderung

Strukturierte Datensätze aus den Transkripten der Use-Case-Wanderung (AI Retreat, 16. Oktober 2026), ausgewertet mit den sechs Leitfragen. Sie sind die Grundlage für Visualisierungen.

## Wo die Dateien liegen

- In diesem Ordner (committet): das Codebuch `themes.csv`, die Bündel `clusters.csv`, die Werkzeugzählung `tool_mentions.csv` und die Skripte in `scripts/`.
- In `shared/daten/` (nicht committet): `transcripts.csv`, `speakers.csv`, `findings.csv` und `use_cases.csv`. Sie stehen nah an dem, was Menschen gesagt haben, und bleiben deshalb lokal. `scripts/build.py` erzeugt sie aus den codierten Teilen in `shared/daten/fragmente/` und prüft sie.

Alle Tabellen sind CSV (UTF-8, Komma, Kopfzeile) im Langformat: eine Zeile pro Beobachtung. Die Tabellen hängen über `transcript_id`, `speaker_id` und `theme_code` zusammen.

## Personen sind pseudonymisiert

Die Tabellen enthalten keine Namen. Personen tragen eine `speaker_id` (P01, P02, ...). Die Zuordnung zu Namen liegt in `shared/daten/speaker_key.csv` und wird nicht committet.

## Tabellen

### transcripts.csv

Eine Zeile pro Transkript.

| Spalte | Bedeutung |
|---|---|
| transcript_id | T01, T02, ... |
| source | Quelle: `lars` (eigene Aufnahme) oder `gruppe` |
| date | Datum der Aufnahme (JJJJ-MM-TT) |
| n_words | Anzahl Wörter, berechnet |
| n_speakers | Anzahl erkennbarer Personen |
| speakers_labelled | `ja`, `teilweise` oder `nein`: ob das Transkript Sprecher:innen ausweist |
| format | `md`, `txt` oder `docx` |
| quality | `gut`, `mittel` oder `schwach` |
| note | Hinweis, zum Beispiel Duplikat oder sehr kurz |

### speakers.csv

Eine Zeile pro Person und Transkript.

| Spalte | Bedeutung |
|---|---|
| transcript_id | Transkript |
| speaker_id | Pseudonym, über alle Transkripte gleich für dieselbe Person |
| role | `teilnehmend` oder `organisation` |
| sector | Bereich, feste Liste (siehe unten) |
| ai_experience | `wenig`, `mittel`, `viel` oder `unklar`, nach eigener Aussage |

### findings.csv

Eine Zeile pro Aussage zu einer Leitfrage. Das ist der Haupt-Datensatz.

| Spalte | Bedeutung |
|---|---|
| finding_id | F0001, ... |
| transcript_id | Transkript |
| speaker_id | Person, oder `unklar` |
| question | 1 bis 6, die Leitfrage |
| subtype | Frage 3: `offen` oder `versteckt`; Frage 4: `gelebt`, `wunsch` oder `buendelbar`; sonst leer |
| theme_code | Thema aus `themes.csv` |
| summary | kurze Zusammenfassung in einem Satz, ohne Namen |
| quote | kurzes wörtliches Zitat, wenn vorhanden |
| sensitive | `ja` oder `nein` |

### use_cases.csv

Eine Zeile pro Anwendungsfall (vertieft Frage 4).

| Spalte | Bedeutung |
|---|---|
| use_case_id | U001, ... |
| transcript_id | Transkript |
| speaker_id | Person, oder `unklar` |
| status | `gelebt` oder `wunsch` |
| task_type | Art der Aufgabe, feste Liste (siehe unten) |
| sector | Bereich, feste Liste |
| tools | Werkzeuge, mit `;` getrennt |
| data_sensitivity | `keine`, `intern` oder `personenbezogen` |
| cluster | Bündel, dem der Fall zugeordnet ist |
| summary | ein Satz, ohne Namen |

### tool_mentions.csv

Eine Zeile pro Werkzeug und Transkript, berechnet durch Textsuche.

| Spalte | Bedeutung |
|---|---|
| transcript_id | Transkript |
| tool | Werkzeug |
| mentions | Anzahl Nennungen |

### themes.csv

Das Codebuch: eine Zeile pro Thema.

| Spalte | Bedeutung |
|---|---|
| theme_code | kurzer Code, zum Beispiel `kontrolle` |
| label | Bezeichnung |
| description | ein Satz |
| questions | Leitfragen, bei denen das Thema vorkommt |

## Feste Listen

- **sector:** verwaltung, wissenschaft, bildung, personal, vertrieb, coaching, beratung, projektmanagement, technik, gesundheit, medien, unternehmensfuehrung, andere, unklar
- **task_type:** schreiben, zusammenfassen, recherchieren, daten_auswerten, automatisieren, programmieren, gestalten, planen, lernen, kommunizieren, wissen_verwalten, andere

## Leitfragen

1. Lest zwischen den Zeilen: Was schwingt mit, ohne dass es jemand direkt ausspricht?
2. Pink Elephants: Welches Thema steht im Raum, über das niemand spricht?
3. Welche Ängste und Vorbehalte gegenüber KI zeigen sich, offen oder versteckt?
4. Welche Use Cases sind schon gelebter Alltag, welche noch Wunsch, und wo lassen sich mehrere bündeln?
5. Welche Fragen sollten wir uns an diesem Wochenende stellen?
6. Wenn diese Gruppe ein Motto für das Wochenende hätte: Wie würde es lauten?

## Grenzen

- Die Transkripte sind automatisch erstellt und enthalten Hörfehler.
- Viele Transkripte weisen keine Sprecher:innen aus. Dann ist `speaker_id` oft `unklar`.
- Die Codierung ist eine Auslegung durch ein Sprachmodell und von Lars geprüft. Zählungen von Themen zeigen, wie oft etwas angesprochen wurde, und keine Gewichtung.
