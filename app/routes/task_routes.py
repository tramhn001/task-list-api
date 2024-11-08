from flask import Blueprint, abort, make_response, request, Response, current_app
from ..models.task import Task
from ..db import db
from sqlalchemy import asc, desc
from datetime import datetime
from .route_utilities import validate_model, create_model
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    # Use the create_model function to handle task creation
    response_body, status_code = create_model(Task, request_body)

    # Format the response to match the expected structure
    response = {
        "task": response_body  # create_model already returns a dictionary representation of the task
    }

    return response, status_code

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    sort_column = Task.title    
    
    sort_param = request.args.get("sort", "asc").lower()
    if sort_param not in ["asc", "desc"]:
        return {"message": "Invalid sort order. Use 'asc' or 'desc"}
    
    query = query.order_by(asc(sort_column) if sort_param == "asc" 
                           else desc(sort_column))
    
    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    task_dict = task.to_dict()
    
    if task.goal_id is not None:
        task_dict["goal_id"] = task.goal_id

    return {"task": task_dict}
   
@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")
    
    db.session.commit()

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
    }

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }

    return response

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_completed(task_id):
    task = validate_model(Task, task_id)
   
    task.completed_at = datetime.now()
    db.session.add(task)
    db.session.commit()

    slack_message = f"Someone just completed the task {task.title}"
    send_slack_notification(slack_message)

    response = {
        "task": task.to_dict()
    }

    return response, 200

def send_slack_notification(message):
    slack_url = current_app.config["SLACK_WEBHOOK_URL"]
    headers = {"Content-Type": "application/json"}
    payload = {
        "text": message,
        "channel": "task-notifications"
    }

    try:
        response = requests.post(slack_url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Slack notification failed: {e}")

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None
   
    db.session.commit()

    response = {
        "task": task.to_dict()
    }

    return response, 200
