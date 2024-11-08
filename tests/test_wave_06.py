from app.models.goal import Goal
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_post_task_ids_to_goal(client, one_goal, three_tasks):
    # Act
    response = client.post("/goals/1/tasks", json={
        "task_ids": [1, 2, 3]
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "task_ids" in response_body
    assert response_body == {
        "id": 1,
        "task_ids": [1, 2, 3]
    }

    # Check that Goal was updated in the db
    assert len(Goal.query.get(1).tasks) == 3


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_post_task_ids_to_goal_already_with_goals(client, one_task_belongs_to_one_goal, three_tasks):
    # Act
    response = client.post("/goals/1/tasks", json={
        "task_ids": [1, 4]
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "task_ids" in response_body
    assert response_body == {
        "id": 1,
        "task_ids": [1, 4]
    }
    assert len(Goal.query.get(1).tasks) == 2


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_for_specific_goal_no_goal(client):
    # Act
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "Goal 1 not found"
    }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_for_specific_goal_no_tasks(client, one_goal):
    # Act
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "tasks" in response_body
    assert len(response_body["tasks"]) == 0
    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily",
        "tasks": []
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_for_specific_goal(client, one_task_belongs_to_one_goal):
    # Act
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "tasks" in response_body
    assert len(response_body["tasks"]) == 1
    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily",
        "tasks": [
            {
                "id": 1,
                "goal_id": 1,
                "title": "Go on my daily walk 🏞",
                "description": "Notice something new every day",
                "is_complete": False
            }
        ]
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_includes_goal_id(client, one_task_belongs_to_one_goal):
    response = client.get("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "task" in response_body
    assert "goal_id" in response_body["task"]
    assert response_body == {
        "task": {
            "id": 1,
            "goal_id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
