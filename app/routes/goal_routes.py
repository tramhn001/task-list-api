from flask import Blueprint, request
from ..models.goal import Goal
from ..models.task import Task
from ..db import db
from sqlalchemy import asc, desc
from .route_utilities import validate_model, create_model


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    response_body, status_code = create_model(Goal, request_body)

    response = {
        "goal": response_body
    }

    return response, status_code
   
@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    goals_response = [goal.to_dict() for goal in goals]

    return goals_response

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        "goal": goal.to_dict()
    }    

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
   
    db.session.commit()

    return {
        "goal": goal.to_dict()
    }

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }

    return response

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    tasks_list = [
        {
            "id": task.id,
            "goal_id": goal.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
        for task in goal.tasks
    ]
        
    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_list
    }

@goals_bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

    db.session.commit()
    
    response_body = {
        "id": goal.id,
        "task_ids": task_ids
    }

    return response_body
