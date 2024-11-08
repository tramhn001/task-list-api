from flask import Blueprint, request
from ..models.goal import Goal
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
        "goal": {
            "id": goal.id,
            "title": goal.title
        }   
    }    

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
   
    db.session.commit()

    response = {
        "goal": {
            "id": goal.id,
            "title": goal.title
        }
    }

    return response, 200

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }

    return response
