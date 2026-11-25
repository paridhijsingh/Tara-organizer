# list_bookmarks.py — List Chrome bookmark folders and counts.
# Usage: python3 scripts/list_bookmarks.py
# Read-only. Moves nothing. Paridhi approves any move first.

import json
from pathlib import Path


def count_bookmarks(node, folders):
    """Walk a bookmark node, collecting folder name -> count."""
    if node.get("type") == "folder":
        name = node.get("name", "Untitled")
        count = 0
        for child in node.get("children", []):
            if child.get("type") == "url":
                count += 1
            elif child.get("type") == "folder":
                count_bookmarks(child, folders)
        folders[name] = folders.get(name, 0) + count
    for child in node.get("children", []):
        if child.get("type") == "folder":
            count_bookmarks(child, folders)


def main():
    bookmarks_path = Path.home() / "Library/Application Support/Google/Chrome/Profile 1/Bookmarks"
    if not bookmarks_path.exists():
        print(f"Bookmarks file not found: {bookmarks_path}")
        print("If you use a different Chrome profile, tell Tara the profile name.")
        return

    data = json.loads(bookmarks_path.read_text())
    folders = {}
    roots = data.get("roots", {})
    for root_name in ["bookmark_bar", "other", "synced"]:
        root = roots.get(root_name)
        if root:
            count_bookmarks(root, folders)

    print("Chrome bookmark folders:")
    for name, count in sorted(folders.items(), key=lambda x: -x[1]):
        print(f"  - {name}: {count} bookmarks")
    print(f"\nTotal folders: {len(folders)}, total bookmarks: {sum(folders.values())}")


if __name__ == "__main__":
    main()