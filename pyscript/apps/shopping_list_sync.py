import time

import requests
import write_file

todoist_token = pyscript.app_config["todoist_token"]
todoist_project_id = pyscript.app_config["todoist_project_id"]

def get_tasks():
    get_tasks_url =f"https://api.todoist.com/rest/v1/tasks?project_id={todoist_project_id}"
    headers = {"Authorization" : f"Bearer {todoist_token}"}

    status_code = 500

    while status_code is not 200:
        response = task.executor(requests.get, get_tasks_url, headers = headers)
        status_code = response.status_code
        time.sleep(1)
    json = response.json()
    return json

def add_task(item):
    url = "https://api.todoist.com/rest/v1/tasks"
    headers = {"Authorization" : f"Bearer {todoist_token}", "Content-Type" : "application/json"}
    body = {"content" : item, "project_id" : todoist_project_id}
    status_code = 500

    while status_code is not 200:
        response = task.executor(requests.post, url, headers = headers, json=body)
        status_code = response.status_code
        time.sleep(1)
    if status_code == 200:
        return True
    else:
        return False

def update_task(id, content):
    url = f"https://api.todoist.com/rest/v1/tasks/{id}"
    headers = {"Authorization" : f"Bearer {todoist_token}", "Content-Type" : "application/json"}
    body = {"content" : content}
    status_code = 500

    counter = 0
    while status_code is not 204 and counter < 10:
        response = task.executor(requests.post, url, headers = headers, json=body)
        status_code = response.status_code
        time.sleep(1)
        counter += 1
    if status_code == 204:
        return True
    else:
        return False

def complete_task(id):
    url = f"https://api.todoist.com/rest/v1/tasks/{id}/close"
    headers = {"Authorization" : f"Bearer {todoist_token}"}
    status_code = 500

    counter = 0
    while status_code is not 204 and counter < 10:
        response = task.executor(requests.post, url, headers = headers)
        status_code = response.status_code
        time.sleep(1)
        counter += 1
    if status_code == 204:
        return True
    else:
        return False

@service
def sync_shopping_list():
    tasks = []
    json = get_tasks()
    for item in json:
        tasks.append({"name" : item["content"], "id" : str(item["id"]), "complete" : item["completed"]})

    write_file.write_json(filename="/config/.shopping_list.json", content=tasks)
    hass.data["shopping_list"].async_load()

@event_trigger('shopping_list_updated')
def update_shopping_list(action=None, item=None):
    if action == "add":
        add_task(item["name"])
        sync_shopping_list()
    if action == "update" and item["complete"] == False:
        update_task(item["id"],item["name"])
        sync_shopping_list()
    if action == "update" and item["complete"] == True:
        complete_task(item["id"])
        sync_shopping_list()
