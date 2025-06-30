import os, requests, datetime as dt

TODOIST_TOKEN = os.getenv("TODOIST_TOKEN")
GOOGLE_TOKEN  = os.getenv("GOOGLE_TASKS_TOKEN")  # service‑account or OAuth copy‑paste

def send_to_todoist(tasks):
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {"Authorization": f"Bearer {TODOIST_TOKEN}"}
    for t in tasks:
        requests.post(url, headers=headers, json={"content": t["text"], "due_string": t.get("due")})

def send_to_google_tasks(tasks):
    # minimal call using token in header
    url = "https://tasks.googleapis.com/tasks/v1/lists/@default/tasks"
    headers = {"Authorization": f"Bearer {GOOGLE_TOKEN}"}
    for t in tasks:
        requests.post(url, headers=headers, json={"title": t["text"], "due": t.get("due")})
