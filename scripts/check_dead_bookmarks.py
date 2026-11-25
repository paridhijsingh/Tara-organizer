# check_dead_bookmarks.py — Check which bookmark URLs no longer load.
# Usage: python3 scripts/check_dead_bookmarks.py
# Read-only. Deletes nothing. Paridhi approves any delete first.
# Takes a few minutes for 336 URLs — it prints progress as it goes.

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import json
import urllib.request
import urllib.error
from pathlib import Path


def collect(node, folder, links):
    for child in node.get("children", []):
        if child.get("type") == "url":
            links.append((folder, child.get("name", ""), child.get("url", "")))
        elif child.get("type") == "folder":
            collect(child, child.get("name", ""), links)


def main():
    bookmarks_path = Path.home() / "Library/Application Support/Google/Chrome/Profile 1/Bookmarks"
    data = json.loads(bookmarks_path.read_text())
    links = []
    for root in data.get("roots", {}).values():
        if isinstance(root, dict):
            collect(root, root.get("name", ""), links)

    print(f"Checking {len(links)} bookmarks...")
    dead = []
    for i, (folder, name, url) in enumerate(links, 1):
        if i % 50 == 0:
            print(f"  ... {i}/{len(links)} checked, {len(dead)} dead so far")
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status >= 400:
                    dead.append((folder, name, url, resp.status))
        except urllib.error.HTTPError as e:
            dead.append((folder, name, url, e.code))
        except Exception as e:
            dead.append((folder, name, url, str(e)[:60]))

    print(f"\nDead / failing bookmarks: {len(dead)} of {len(links)}")
    for folder, name, url, error in dead:
        print(f"  - [{folder}] {name} — {url} — {error}")


if __name__ == "__main__":
    main()