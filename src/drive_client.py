# drive_client.py — Read-only Drive storage check.
# Returns how full Drive is, and the largest files. Deletes nothing.

from googleapiclient.discovery import build

from auth import get_credentials


def get_storage():
    """Return (used_bytes, limit_bytes, used_gb, limit_gb, percent_used)."""
    service = build("drive", "v3", credentials=get_credentials())
    about = service.about().get(fields="storageQuota").execute()
    quota = about.get("storageQuota", {})
    used = int(quota.get("usage", 0))
    limit = int(quota.get("limit", 0))
    used_gb = used / (1024 ** 3)
    limit_gb = limit / (1024 ** 3) if limit else 0
    percent = (used / limit * 100) if limit else 0
    return used, limit, used_gb, limit_gb, percent, quota


def get_largest_files(count=10):
    """Return a list of the largest files: {name, size_mb, modified, mime_type}."""
    service = build("drive", "v3", credentials=get_credentials())
    result = service.files().list(
    q="'me' in owners",
    orderBy="quotaBytesUsed desc",
    pageSize=count,
    fields="files(id,name,mimeType,size,modifiedTime,owners)",
).execute()
    files = []
    for file in result.get("files", []):
        size = int(file.get("size", 0))
        files.append({
            "name": file.get("name", ""),
            "size_mb": round(size / (1024 ** 2), 1),
            "modified": file.get("modifiedTime", "")[:10],
            "mime_type": file.get("mimeType", ""),
            "owner": file.get("owners", [{}])[0].get("displayName", ""),
        })
    return files