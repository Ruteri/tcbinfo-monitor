import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE = SCRIPT_DIR / "index.template.html"
DIFFS_DIR = SCRIPT_DIR / "diffs"
TCBS_JSON = SCRIPT_DIR / "tcbs.json"


def build_diff_entries():
    if not DIFFS_DIR.is_dir():
        return ""

    # Sort diff files by name descending (newest date first)
    files = sorted(DIFFS_DIR.iterdir(), reverse=True)

    parts = []
    for f in files:
        if f.is_file():
            content = f.read_text()
            parts.append(f'<div class="diff-entry">\n{content}\n</div>')

    return "\n".join(parts)


def load_tcb_data():
    if TCBS_JSON.is_file():
        return TCBS_JSON.read_text()
    return "null"


def main():
    template = TEMPLATE.read_text()
    entries = build_diff_entries()
    tcb_json = load_tcb_data()
    html = template.replace("<!-- DIFF_ENTRIES -->", entries)
    html = html.replace("/* TCB_DATA_JSON */null", tcb_json)
    print(html)


if __name__ == "__main__":
    main()
