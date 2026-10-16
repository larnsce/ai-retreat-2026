# Datenaufbereitung für die Folien zur Use-Case-Wanderung.
# Liest die Datensätze aus shared/daten (nicht committet) und die Codelisten
# aus products/daten. Ergebnis: Tabellen, die die Plot-Chunks direkt nutzen.

library(readr)
library(dplyr)
library(tidyr)
library(forcats)

pfad_shared <- here::here("shared", "daten")
pfad_codes <- here::here("products", "daten")

lies <- function(pfad, datei) read_csv(file.path(pfad, datei), show_col_types = FALSE, col_types = cols(.default = col_character()))

transcripts <- lies(pfad_shared, "transcripts.csv")
speakers <- lies(pfad_shared, "speakers.csv")
findings <- lies(pfad_shared, "findings.csv")
use_cases <- lies(pfad_shared, "use_cases.csv")
themes <- lies(pfad_codes, "themes.csv")
clusters <- lies(pfad_codes, "clusters.csv")
tool_mentions <- lies(pfad_codes, "tool_mentions.csv") |> mutate(mentions = as.integer(mentions))

# Einführungen (T01, T02) sind nicht codiert; T15 und T16 sind zweite Aufnahmen
# von T04 und T08 und zählen bei Gesprächszahlen nicht doppelt.
einfuehrungen <- c("T01", "T02")
zweitaufnahmen <- c("T15", "T16")
aufnahmen <- setdiff(transcripts$transcript_id, einfuehrungen)
gespraeche <- setdiff(aufnahmen, zweitaufnahmen)

# Sortiert Balken innerhalb von Facetten (wie tidytext::reorder_within).
tidytext_order <- function(x, by, within) {
  key <- paste(x, within, sep = "___")
  reorder(key, by)
}

leitfragen <- tibble(
  question = as.character(1:6),
  frage = c("1 Zwischen den Zeilen", "2 Pink Elephants", "3 Ängste und Vorbehalte",
            "4 Use Cases", "5 Fragen fürs Wochenende", "6 Motto")
)

kennzahlen <- list(
  aufnahmen = length(aufnahmen),
  gespraeche = length(gespraeche),
  personen = n_distinct(speakers$speaker_id[speakers$speaker_id != "unklar"]),
  aussagen = nrow(findings),
  use_cases = nrow(use_cases)
)

# Folie 2: Aussagen pro Leitfrage, sortiert nach Häufigkeit
pro_frage <- findings |>
  count(question) |>
  left_join(leitfragen, by = "question") |>
  mutate(frage = fct_reorder(frage, n))

# Folie 3: pro Leitfrage die drei Themen, die in den meisten Gesprächen vorkommen.
# Leitfrage 4 hat eine eigene Folie; ihre Aussagen wurden meist als
# "begeisterung" codiert und würden hier verzerren.
fragen_karte <- c("1", "2", "3", "5", "6")
top_themen <- findings |>
  filter(transcript_id %in% gespraeche, question %in% fragen_karte) |>
  distinct(question, theme_code, transcript_id) |>
  count(question, theme_code, name = "gespraeche") |>
  group_by(question) |>
  slice_max(gespraeche, n = 3, with_ties = FALSE) |>
  ungroup() |>
  left_join(select(themes, theme_code, label), by = "theme_code") |>
  left_join(leitfragen, by = "question") |>
  mutate(
    frage = factor(frage, levels = leitfragen$frage),
    zeile = tidytext_order(label, gespraeche, frage)
  )

# Folie 5: Use Cases in fünf Gruppen, gelebt und Wunsch
gruppen <- c(
  gestaltung = "Schreiben und Gestalten", dokumente = "Schreiben und Gestalten",
  transkription = "Schreiben und Gestalten",
  assistenz = "Organisieren", planung = "Organisieren", gedaechtnis = "Organisieren",
  eigene_daten = "Auswerten und Bauen", software = "Auswerten und Bauen", lokal = "Auswerten und Bauen",
  vertrieb = "Vertrieb und Kontakte",
  sparring = "Lernen und Orientierung", orientierung = "Lernen und Orientierung"
)
use_cases <- use_cases |> mutate(gruppe = unname(gruppen[cluster]))

use_case_gruppen <- use_cases |>
  count(gruppe, status) |>
  group_by(gruppe) |>
  mutate(gesamt = sum(n)) |>
  ungroup() |>
  mutate(
    wert = if_else(status == "gelebt", -n, n),
    status = factor(status, levels = c("gelebt", "wunsch"), labels = c("gelebt", "Wunsch")),
    gruppe = fct_reorder(gruppe, gesamt)
  )

# Folie 6: KI-Werkzeuge, in wie vielen Gesprächen genannt
ki_werkzeuge <- c("Claude", "Claude Code", "Claude Cowork", "ChatGPT", "Copilot", "Gemini",
                  "NotebookLM", "Mistral", "Perplexity", "Granola", "OpenRouter",
                  "lokales Modell", "n8n", "Notion", "Obsidian", "Lovable")
werkzeuge <- tool_mentions |>
  filter(transcript_id %in% gespraeche, tool %in% ki_werkzeuge) |>
  group_by(tool) |>
  summarise(gespraeche = n_distinct(transcript_id), nennungen = sum(mentions), .groups = "drop") |>
  mutate(tool = fct_reorder(tool, gespraeche))

# Folie 8: Ängste offen und versteckt pro Thema
aengste <- findings |>
  filter(question == "3") |>
  count(theme_code, subtype) |>
  left_join(select(themes, theme_code, label), by = "theme_code") |>
  group_by(label) |>
  mutate(gesamt = sum(n)) |>
  ungroup() |>
  mutate(
    label = fct_reorder(label, gesamt),
    subtype = factor(subtype, levels = c("versteckt", "offen"))
  )

# Folie 9: Datensensibilität der Use Cases pro Gruppe
sensibilitaet <- use_cases |>
  count(gruppe, data_sensitivity) |>
  group_by(gruppe) |>
  mutate(anteil = n / sum(n), gesamt = sum(n)) |>
  ungroup() |>
  mutate(
    data_sensitivity = factor(data_sensitivity, levels = c("personenbezogen", "intern", "keine"),
                              labels = c("Daten über Personen", "interne Daten", "keine heiklen Daten")),
    gruppe = fct_reorder(gruppe, gesamt)
  )
anteil_personen <- mean(use_cases$data_sensitivity == "personenbezogen")

# Folie 10: Motto-Vorschläge nach Thema
motto <- findings |>
  filter(question == "6") |>
  count(theme_code) |>
  left_join(select(themes, theme_code, label), by = "theme_code") |>
  slice_max(n, n = 5, with_ties = FALSE) |>
  mutate(label = fct_reorder(label, n))

# Folie 3: je drei Beispiele für Leitfrage 1 und 2, mit Person (Pseudonym und Bereich).
# Ausgewählt: nicht sensibel, Person zugeordnet, aus den häufigsten Themen der Frage.
beispiel_ids <- c("F0425", "F0035", "F0516", "F0490", "F0008", "F0613")
bereiche <- c(wissenschaft = "Wissenschaft", personal = "Personal", beratung = "Beratung",
              coaching = "Coaching", bildung = "Bildung", projektmanagement = "Projektmanagement",
              gesundheit = "Gesundheit", medien = "Medien", technik = "Technik", andere = "andere")
personen <- speakers |>
  distinct(speaker_id, sector) |>
  mutate(person = paste0(speaker_id, ", ", unname(bereiche[sector])))
beispiele <- findings |>
  filter(finding_id %in% beispiel_ids) |>
  left_join(select(personen, speaker_id, person), by = "speaker_id") |>
  left_join(select(themes, theme_code, label), by = "theme_code") |>
  mutate(finding_id = factor(finding_id, levels = beispiel_ids)) |>
  arrange(finding_id)

# Folie 10: Zusammenfassung der als sensibel markierten Aussagen, nur Zahlen
sensibel <- findings |> filter(sensitive == "ja")
sensibel_kennzahlen <- list(
  n = nrow(sensibel),
  anteil = nrow(sensibel) / nrow(findings),
  aufnahmen = n_distinct(sensibel$transcript_id),
  personen = n_distinct(sensibel$speaker_id[sensibel$speaker_id != "unklar"])
)
sensibel_themen <- sensibel |>
  count(theme_code) |>
  left_join(select(themes, theme_code, label), by = "theme_code") |>
  mutate(label = if_else(n < 6, "weitere Themen", label)) |>
  group_by(label) |>
  summarise(n = sum(n), .groups = "drop") |>
  mutate(label = fct_relevel(fct_reorder(label, n), "weitere Themen"))
sensibel_fragen <- sensibel |>
  count(question) |>
  left_join(leitfragen, by = "question") |>
  arrange(desc(n))
