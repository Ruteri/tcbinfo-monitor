import json
import os
import re
import sys

import requests
from deepdiff import DeepDiff

SITE_URL = "https://ruteri.github.io/tcbinfo-monitor/"


def remap_tcb_data(data):
    return {
        "SGX": {it["tcbInfo"]["fmspc"]: it["tcbInfo"] for it in data if it["tcbInfo"]["id"] == "SGX"},
        "TDX": {it["tcbInfo"]["fmspc"]: it["tcbInfo"] for it in data if it["tcbInfo"]["id"] == "TDX"},
    }


def get_changed_fmspcs(diff):
    """Extract FMSPC values from DeepDiff keys via regex."""
    fmspcs = set()
    pattern = re.compile(r"root\['[^']+'\]\['([^']+)'\]")
    for change_type in diff:
        for key in diff[change_type]:
            m = pattern.match(key)
            if m:
                fmspcs.add(m.group(1))
    return fmspcs


def build_slack_message(changed_watched):
    lines = []
    for fmspc in sorted(changed_watched):
        lines.append(f":warning: TCB update: FMSPC {fmspc} changed")
        lines.append(f"{SITE_URL}?fmspc={fmspc}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main():
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    watched_raw = os.environ.get("WATCHED_FMSPCS", "")

    if not webhook_url or not watched_raw:
        print("SLACK_WEBHOOK_URL or WATCHED_FMSPCS not set, skipping notification.")
        sys.exit(0)

    watched = {f.strip().upper() for f in watched_raw.split(",") if f.strip()}
    if not watched:
        print("No FMSPCs in watch list, skipping.")
        sys.exit(0)

    old_path, new_path = sys.argv[1], sys.argv[2]

    with open(old_path, "r") as f:
        old_data = json.load(f)
    with open(new_path, "r") as f:
        new_data = json.load(f)

    old_remapped = remap_tcb_data(old_data)
    new_remapped = remap_tcb_data(new_data)

    issue_date_path = r"root\['.*'\]\['.*'\]\['issueDate'\]"
    next_update_path = r"root\['.*'\]\['.*'\]\['nextUpdate'\]"

    diff = DeepDiff(
        old_remapped, new_remapped,
        ignore_order=True, verbose_level=2,
        exclude_regex_paths=[issue_date_path, next_update_path],
    )

    if not diff:
        print("No meaningful changes detected.")
        sys.exit(0)

    changed = get_changed_fmspcs(diff)
    changed_watched = {f for f in changed if f.upper() in watched}

    if not changed_watched:
        print(f"Changes detected but none in watched list ({', '.join(sorted(watched))}).")
        sys.exit(0)

    message = build_slack_message(changed_watched)
    print(f"Sending Slack notification for: {', '.join(sorted(changed_watched))}")

    resp = requests.post(webhook_url, json={"text": message}, timeout=10)
    if resp.status_code != 200:
        print(f"Slack API error: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)

    print("Slack notification sent.")


if __name__ == "__main__":
    main()
