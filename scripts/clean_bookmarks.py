# clean_bookmarks.py — Delete the approved dead bookmarks.
# APPROVED by Paridhi Nov 25, 2026: 13 URLs, all 404 / DNS-gone.
# Usage: python3 scripts/clean_bookmarks.py
# Close Chrome first — it rewrites Bookmarks on exit.
# Backs up Bookmarks to Bookmarks.bak before deleting.

import json
import shutil
from pathlib import Path

APPROVED_URLS = [
    "https://www.hulu.com/switch-profile-error",
    "https://duels.ucsb.edu/advising/planning/degree#Area%20A:%20%20English%20Reading%20and%20Composition",
    "https://www.wolfsongalaska.org/chorus/node/193",
    "https://store.extemporeapp.com/classes/B2DFBBAA-00BD-454C-92B4-8A783EB1980B",
    "https://github.com/syndrya-ai/dev-tools",
    "https://github.com/syndrya-ai/dev-tools/blob/main/README.md",
    "https://github.com/syndrya-ai/dev-tools/tree/main/development",
    "https://my.ucla.edu/conference/spur2026-8wk/181/47187",
    "https://www.builder.io/blog/cursor-vs-claude-code?utm_source=youtube&utm_content=vg",
    "https://pastel-productivity-dashboard--paridhijaysingh.replit.app/",
    "https://jobs.ashbyhq.com/llamaindex/36a0249e-a672-44df-a08e-b5a5523dec26?utm_source=aRNGJbZ3z6",
    "https://pstat134.lsit.ucsb.edu/user/paridhijsingh/lab/tree/Winter2026",
    "https://console.cloud.intel.com/",
]


def clean(node):
    removed = 0
    children = node.get("children", [])
    kept = []
    for child in children:
        if child.get("type") == "url" and child.get("url") in APPROVED_URLS:
            print(f"Deleting: [{node.get('name', '')}] {child.get('name', '')}")
            removed += 1
        elif child.get("type") == "folder":
            removed += clean(child)
            kept.append(child)
        else:
            kept.append(child)
    node["children"] = kept
    return removed


def main():
    bookmarks_path = Path.home() / "Library/Application Support/Google/Chrome/Profile 1/Bookmarks"
    shutil.copy(bookmarks_path, bookmarks_path.with_suffix(".bak"))
    print(f"Backed up to: {bookmarks_path.with_suffix('.bak')}")

    data = json.loads(bookmarks_path.read_text())
    total = 0
    for root in data.get("roots", {}).values():
        if isinstance(root, dict):
            total += clean(root)

    bookmarks_path.write_text(json.dumps(data, indent=2))
    print(f"\nDeleted {total} bookmarks. Close Chrome was required — reopen it to see the change.")


if __name__ == "__main__":
    main()