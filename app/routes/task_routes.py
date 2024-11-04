from flask import Blueprint, abort, make_response, request, Response
from ..models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("description"):
        return {"details": "Invalid data"}, 400
    
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at")

    is_complete = bool(completed_at)

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
        }
    }
    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at is not None
            }
            for task in tasks
    ]

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }   
    }    

def validate_task(task_id):
    try: 
        task_id = int(task_id)
    except:
        response = {"message": f"task {task_id} invalid"}
        abort(make_response(response, 400))
    
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"Task {task_id} not found"}
        abort(make_response(response, 404))
    
    return task

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")
    
    db.session.commit()

    response = {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
    }

    return response, 200

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }

    return response

