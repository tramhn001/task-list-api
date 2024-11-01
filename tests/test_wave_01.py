from app.models.task import Task
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_no_saved_tasks(client):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_one_saved_tasks(client, one_task):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    ]


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task(client, one_task):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_not_found(client):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": False
        }
    }
    new_task = Task.query.get(1)
    assert new_task
    assert new_task.title == "A Brand New Task"
    assert new_task.description == "Test Description"
    assert new_task.completed_at == None


@pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": False
        }
    }
    task = Task.query.get(1)
    assert task.title == "Updated Task Title"
    assert task.description == "Updated Test Description"
    assert task.completed_at == None


@pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_not_found(client):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task(client, one_task):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    }
    assert Task.query.get(1) == None


@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task_not_found(client):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************

    assert Task.query.all() == []


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_must_contain_title(client):
    # Act
    response = client.post("/tasks", json={
        "description": "Test Description"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Task.query.all() == []


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_must_contain_description(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Task.query.all() == []
