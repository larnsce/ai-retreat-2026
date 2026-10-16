"""Count tool mentions per transcript and write tool_mentions.csv.

Usage: python3 products/daten/scripts/tool_mentions.py (from the repository root)
Reads shared/daten/transcript_key.csv and the transcripts in shared/.
Transcription errors are covered by the variant patterns below; "Cloud" alone
is counted separately as "Cloud oder Claude (unklar)", because in the
transcripts it stands for Claude about half the time and for cloud services otherwise.
"""
import csv, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
SHARED = ROOT / "shared"
OUT = ROOT / "products" / "daten" / "tool_mentions.csv"

CLAUDE = r"(?:claude|claud|clot|klot|klaude)"
TOOLS = {
    "Claude Code": rf"\b(?:{CLAUDE}|cloud)[\s-]*code\b",
    "Claude Cowork": rf"\b{CLAUDE}[\s-]*co-?work\b",
    "Claude": rf"\b{CLAUDE}\b(?![\s-]*(?:code|co-?work)\b)",
    "Cloud oder Claude (unklar)": r"\bcloud\b(?![\s-]*code\b)",
    "ChatGPT": r"\b(?:chat\s?gpt|chatgbt|chat-gpt|chippettin|chatopie)\b",
    "Copilot": r"\bco-?pilot\b",
    "Gemini": r"\bgemini\b",
    "NotebookLM": r"\bnotebook\s?lm\b|\bgemini notebook\b",
    "Mistral": r"\bmistral\b",
    "Perplexity": r"\bperplexity\b",
    "Granola": r"\bgranola\b",
    "Notion": r"\bnotion\b",
    "Obsidian": r"\bobsidian\b",
    "n8n": r"\bn8n\b",
    "Make": r"\bmake\.com\b",
    "OpenRouter": r"\bopen\s?router\b",
    "Lovable": r"\blovable\b",
    "Miro": r"\bmiro\b",
    "Canva": r"\bcanva\b",
    "Garmin": r"\bgarmin\b|\bgarmen\b",
    "Excel": r"\bexcel\b",
    "PowerPoint": r"\bpower\s?point\b",
    "Outlook": r"\boutlook\b",
    "Teams": r"\bteams\b",
    "LinkedIn": r"\blinked\s?in\b",
    "MCP": r"\bmcp\b",
    "lokales Modell": r"\blokale[nsm]?\s+(?:ki|modell|sprachmodell|open[\s-]?source)",
}

def main():
    rows = []
    with open(SHARED / "daten" / "transcript_key.csv") as f:
        for r in csv.DictReader(f):
            text = (SHARED / r["file"]).read_text(errors="replace")
            if "## Transkript" in text:
                text = text.split("## Transkript", 1)[1]
            low = text.lower()
            for tool, pat in TOOLS.items():
                n = len(re.findall(pat, low))
                if n:
                    rows.append({"transcript_id": r["transcript_id"], "tool": tool, "mentions": n})
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["transcript_id", "tool", "mentions"])
        w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} rows written to {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
