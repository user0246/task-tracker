import json
import os
import argparse
from datetime import datetime, date

def generate_id():
    if os.path.exists("tasks.json") and os.path.getsize("tasks.json") > 0:
        with open("tasks.json", "r") as f:
            data = json.load(f)
        value = data[-1].get("id")
        return value+1
    else:
        return 1 

def check_up(task):
    if os.path.exists("tasks.json") and os.path.getsize("tasks.json") > 0:
        with open("tasks.json", "r") as f:
            tasks_list = json.load(f)
    else:
        tasks_list = []
    result = tasks_list.copy()
    result.append(task)
    print(result)
    return result 

def task_list():
    with open("tasks.json", "r") as f:
        tasks_list = json.load(f)
    for i in tasks_list:
        print(f"ID: {i['id']}; Description: {i['description']}; Status: {i['status']}")

def task_list_in_progress():
    with open("tasks.json", "r") as f:
        tasks_list = json.load(f)
    for i in tasks_list:
        if i['status'] == 'in_progress':
            print(f"ID: {i['id']}; Description: {i['description']}; Status: {i['status']}")

def task_list_done():
    with open("tasks.json", "r") as f:
        tasks_list = json.load(f)
    for i in tasks_list:
        if i['status'] == 'done':
            print(f"ID: {i['id']}; Description: {i['description']}; Status: {i['status']}")

def add_task(description):
    current_time = datetime.now().isoformat()
    id = generate_id()
    tasks_list = []
    task_data = {
        "id": id,
        "description": description,
        "status": "todo", 
        "createdAt": current_time,
        "updatedAt": current_time 
    }
    
    check_data = check_up(task_data)
    with open("tasks.json", "w") as f:
        json.dump(check_data, f)
    print(f"Task added succussfully (ID: {id})")

def update_task(task_id, description):
    with open("tasks.json", "r") as f:
        tasks_list = json.load(f)
    for i in tasks_list:
        if i['id'] == task_id:
            i['description'] = description
    with open("tasks.json", "w") as f:
        json.dump(tasks_list, f) 
    print(f"Task updated (ID: {task_id})")

def delete_task(task_id):
    with open("tasks.json", "r") as f:
        tasks_list = json.load(f)
    tasks_list = [item for item in tasks_list if item['id'] != task_id]
        
    with open("tasks.json", "w") as f:
        json.dump(tasks_list, f) 
    print(f"Task deleted (ID: {task_id})")
    
def mark_in_progress(task_id):
    with open("tasks.json", "r") as f:
        tasks_list = json.load(f)
    for i in tasks_list:
        if i['id'] == task_id:
            i['status'] = "in_progress" 
    with open("tasks.json", "w") as f:
        json.dump(tasks_list, f) 
    print(f"Task updated (ID: {task_id})")

def mark_done(task_id):
    with open("tasks.json", "r") as f:
        tasks_list = json.load(f)
    for i in tasks_list:
        if i['id'] == task_id:
            i['status'] = "done" 
    with open("tasks.json", "w") as f:
        json.dump(tasks_list, f) 
    print(f"Task updated (ID: {task_id})")

def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Функция add
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("description", type=str)

    #Функция list
    parser_add = subparsers.add_parser("list")
    parser_add.add_argument("status", nargs='?', choices=['done', 'todo', 'in_progress'], default=None)

    #Функция update
    parser_add = subparsers.add_parser("update")
    parser_add.add_argument("task_id", type=int)
    parser_add.add_argument("description", type=str)

    #Функция delete
    parser_add = subparsers.add_parser("delete")
    parser_add.add_argument("task_id", type=int)

    #Функция mark_in_progress
    parser_add = subparsers.add_parser("mark_in_progress")
    parser_add.add_argument("task_id", type=int)

    #Функция mark_done
    parser_add = subparsers.add_parser("mark_done")
    parser_add.add_argument("task_id", type=int)

    #Аргументы
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        if args.status == "done":
            task_list_done()
        elif args.status == "in_progress":
            task_list_in_progress()
        else:
            task_list()
    elif args.command == "update":
        update_task(args.task_id, args.description)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "mark_in_progress":
        mark_in_progress(args.task_id)
    elif args.command == "mark_done":
        mark_done(args.task_id)
    #print(args.command)
    #print(args.title)


if __name__ == '__main__':
    main()