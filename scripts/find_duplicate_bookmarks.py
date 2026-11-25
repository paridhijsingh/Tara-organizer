# find_duplicate_bookmarks.py — Find duplicate bookmark URLs.
# Usage: python3 scripts/find_duplicate_bookmarks.py
# Read-only. Deletes nothing. Paridhi approves any delete first.

import json
from collections import defaultdict
from pathlib import Path


def collect(node, folder, by_url):
    for child in node.get("children", []):
        if child.get("type") == "url":
            by_url[child.get("url", "")].append((folder, child.get("name", "")))
        elif child.get("type") == "folder":
            collect(child, child.get("name", ""), by_url)


def main():
    bookmarks_path = Path.home() / "Library/Application Support/Google/Chrome/Profile 1/Bookmarks"
    data = json.loads(bookmarks_path.read_text())
    by_url = defaultdict(list)
    for root in data.get("roots", {}).values():
        if isinstance(root, dict):
            collect(root, root.get("name", ""), by_url)

    duplicates = {url: locs for url, locs in by_url.items() if len(locs) > 1}
    print(f"Total unique URLs: {len(by_url)}")
    print(f"Duplicate URLs: {len(duplicates)}")
    print("")
    for url, locs in sorted(duplicates.items(), key=lambda x: -len(x[1]))[:20]:
        print(f"{url} — {len(locs)} copies:")
        for folder, name in locs:
            print(f"    - [{folder}] {name}")
    if len(duplicates) > 20:
        print(f"\n... and {len(duplicates) - 20} more duplicate URLs (showing top 20).")


if __name__ == "__main__":
    main()