from flask import Blueprint, abort, make_response, request, Response
from ..models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at")

    is_complete = bool(completed_at)

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = new_task.to_dict()
    response["is_complete"] = is_complete
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
                "completed_at": task.completed_at,
                "is_complete": task.completed_at is not None
            }
            for task in tasks
    ]

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)    


def validate_task(task_id):
    try: 
        task_id = int(task_id)
    except:
        response = {"message": f"task {task_id} invalid"}
