"""Merge the coded fragments into the final datasets and check them.

Usage: python3 products/daten/scripts/build.py (from the repository root)
Inputs: shared/daten/fragmente/T??_{meta,speakers,findings,use_cases}.csv,
shared/daten/transcript_key.csv, shared/daten/speaker_key.csv.
Outputs: shared/daten/{transcripts,speakers,findings,use_cases}.csv, the full
local version, and the same four tables in products/daten/ for publication:
summary and quote are emptied in rows flagged as sensitive, so every count
stays reproducible while sensitive content stays local.
Exits with an error listing every problem found; names from the speaker key
must never reach the outputs.
"""
import csv, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
FRAG = ROOT / "shared" / "daten" / "fragmente"
KEYS = ROOT / "shared" / "daten"
CODES = ROOT / "products" / "daten"
OUT = ROOT / "shared" / "daten"

SECTORS = set("verwaltung wissenschaft bildung personal vertrieb coaching beratung projektmanagement technik gesundheit medien unternehmensfuehrung andere unklar".split())
TASKS = set("schreiben zusammenfassen recherchieren daten_auswerten automatisieren programmieren gestalten planen lernen kommunizieren wissen_verwalten andere".split())
SUBTYPES = {"3": {"offen", "versteckt"}, "4": {"gelebt", "wunsch", "buendelbar"}}

def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write(name, rows, fields):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def main():
    problems = []
    tkey = {r["transcript_id"]: r for r in read(KEYS / "transcript_key.csv")}
    skey = {r["speaker_id"]: r for r in read(KEYS / "speaker_key.csv")}
    themes = {r["theme_code"] for r in read(CODES / "themes.csv")}
    clusters = {r["cluster"] for r in read(CODES / "clusters.csv")}
    names = set()
    for r in skey.values():
        for part in re.split(r"[\s()/-]+", r["name"]):
            if len(part) > 3 and part[0].isupper() and part not in {"Pharma", "Coach", "Projektmanager", "Franken", "unbekannt"}:
                names.add(part)
    names |= {"Andre", "Timo", "Christina", "Schöbitz", "Fischer", "Kieffer"}
    name_re = re.compile(r"\b(" + "|".join(sorted(names)) + r")\b")

    meta, speakers, findings, use_cases = [], [], [], []
    for tid in sorted(tkey):
        parts = {k: FRAG / f"{tid}_{k}.csv" for k in ("meta", "speakers", "findings", "use_cases")}
        if not parts["meta"].exists():
            if tid in ("T01", "T02"):
                meta.append({"transcript_id": tid, "date": "2026-10-16", "n_speakers": "", "speakers_labelled": "nein",
                             "quality": "gut", "note": "Einführung der Organisation, nicht codiert"})
                continue
            problems.append(f"{tid}: no fragments"); continue
        m = read(parts["meta"])[0]
        meta.append(m)
        speakers += read(parts["speakers"])
        findings += read(parts["findings"])
        use_cases += read(parts["use_cases"]) if parts["use_cases"].exists() else []

    for m in meta:
        k = tkey[m["transcript_id"]]
        m.update(source=k["source"], format=k["format"], n_words=k["n_words"])
    for s in speakers:
        sid = s["speaker_id"]
        if sid != "unklar" and sid not in skey:
            problems.append(f"speakers {s['transcript_id']}: unknown speaker_id {sid}")
        k = skey.get(sid, {})
        s["role"] = k.get("role", s.get("role", ""))
        s["sector"] = k.get("sector", "unklar")
    for i, f in enumerate(findings, 1):
        where = f"finding {f.get('finding_id')}"
        f["finding_id"] = f"F{i:04d}"
        if f["theme_code"] not in themes: problems.append(f"{where}: theme {f['theme_code']}")
        if f["question"] not in list("123456"): problems.append(f"{where}: question {f['question']}")
        allowed = SUBTYPES.get(f["question"], {""})
        if f["subtype"] not in allowed: problems.append(f"{where}: subtype {f['subtype']!r}")
        if f["speaker_id"] != "unklar" and f["speaker_id"] not in skey: problems.append(f"{where}: speaker {f['speaker_id']}")
        if f["sensitive"] not in ("ja", "nein"): problems.append(f"{where}: sensitive {f['sensitive']}")
    for i, u in enumerate(use_cases, 1):
        where = f"use case {u.get('use_case_id')}"
        u["use_case_id"] = f"U{i:03d}"
        if u["status"] not in ("gelebt", "wunsch"): problems.append(f"{where}: status {u['status']}")
        if u["task_type"] not in TASKS: problems.append(f"{where}: task_type {u['task_type']}")
        if u["sector"] not in SECTORS: problems.append(f"{where}: sector {u['sector']}")
        if u["cluster"] not in clusters: problems.append(f"{where}: cluster {u['cluster']}")
        if u["data_sensitivity"] not in ("keine", "intern", "personenbezogen"): problems.append(f"{where}: data_sensitivity {u['data_sensitivity']}")
        if u["speaker_id"] != "unklar" and u["speaker_id"] not in skey: problems.append(f"{where}: speaker {u['speaker_id']}")
    for row in findings + use_cases:
        for col in ("summary", "quote"):
            text = row.get(col) or ""
            if name_re.search(text): problems.append(f"{row.get('finding_id') or row.get('use_case_id')}: name in {col}: {name_re.search(text).group(0)}")
            if "—" in text: problems.append(f"{row.get('finding_id') or row.get('use_case_id')}: em dash in {col}")

    write("transcripts.csv", meta, ["transcript_id", "source", "date", "n_words", "n_speakers", "speakers_labelled", "format", "quality", "note"])
    write("speakers.csv", speakers, ["transcript_id", "speaker_id", "role", "sector", "ai_experience"])
    write("findings.csv", findings, ["finding_id", "transcript_id", "speaker_id", "question", "subtype", "theme_code", "summary", "quote", "sensitive"])
    write("use_cases.csv", use_cases, ["use_case_id", "transcript_id", "speaker_id", "status", "task_type", "sector", "tools", "data_sensitivity", "cluster", "summary"])
    # Public copies: sensitive findings keep their codes but lose their text.
    public = [dict(f, summary="", quote="") if f["sensitive"] == "ja" else f for f in findings]
    public_meta = [dict(m, note=m.get("note", "").replace(", Bruder wie in T26", " wie in T26")) for m in meta]
    for name, rows, fields in [
        ("transcripts.csv", public_meta, ["transcript_id", "source", "date", "n_words", "n_speakers", "speakers_labelled", "format", "quality", "note"]),
        ("speakers.csv", speakers, ["transcript_id", "speaker_id", "role", "sector", "ai_experience"]),
        ("findings.csv", public, ["finding_id", "transcript_id", "speaker_id", "question", "subtype", "theme_code", "summary", "quote", "sensitive"]),
        ("use_cases.csv", use_cases, ["use_case_id", "transcript_id", "speaker_id", "status", "task_type", "sector", "tools", "data_sensitivity", "cluster", "summary"]),
    ]:
        with open(CODES / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader(); w.writerows(rows)

    print(f"transcripts {len(meta)}, speaker rows {len(speakers)}, findings {len(findings)}, use cases {len(use_cases)}")
    if problems:
        print(f"{len(problems)} problems:"); print("\n".join(problems)); sys.exit(1)
    print("all checks passed")

if __name__ == "__main__":
    main()
