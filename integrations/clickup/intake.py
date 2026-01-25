import os
import json
import requests
from pathlib import Path

TOKEN = os.getenv("CLICKUP_API_TOKEN")
LIST_ID = os.getenv("CLICKUP_LIST_ID")

if not TOKEN or not LIST_ID:
    raise RuntimeError("Missing ClickUp env vars")

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def fetch_tasks():
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
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
    out.write_text(json.dumps(intake, indent=2))
    print(f"Saved {len(intake)} tasks to {out}")
