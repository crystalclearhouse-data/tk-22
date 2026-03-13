import os
import json
import requests
from pathlib import Path

def fetch_tasks():
    token = os.getenv("CLICKUP_API_TOKEN")
    list_id = os.getenv("CLICKUP_LIST_ID")

    if not token or not list_id:
        raise RuntimeError("Missing ClickUp env vars")

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["tasks"]

def normalize_task(task):
    return {
        "id": task["id"],
        "name": task["name"],
        "status": task["status"]["status"],
        "tags": [t["name"] for t in task.get("tags", [])],
        "description": task.get("description")
    }

if __name__ == "__main__":
    tasks = fetch_tasks()
    intake = [normalize_task(t) for t in tasks]

    out = Path("control/memory/clickup_intake.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(intake, indent=2))
    print(f"Saved {len(intake)} tasks to {out}")
