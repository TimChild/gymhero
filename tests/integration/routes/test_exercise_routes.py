from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
import pytest
from sqlalchemy.orm import Session

from gymhero.models.exercise import Exercise
from gymhero.security import create_access_token
from scripts.core.utils import _create_first_user


def _create_jwt_for_user(user_id: int):
    token = create_access_token(str(user_id))
    return f"Bearer {token}"


def test_can_get_all_exercises(test_client, seed_test_database):
    response = test_client.get("/exercises/all")
    assert response.status_code == 200

    response = test_client.get("/exercises/all", params={"limit": 1})
    assert response.status_code == 200 and len(response.json()) == 1


def test_can_get_one_exercise(test_client, seed_test_database):
    response = test_client.get("/exercises/1")
    assert response.status_code == 200 and response.json()["id"] == 1
    print(response.json())
    response = test_client.get("/exercises/23423423")
    assert (
        response.status_code == 404
        and response.json()["detail"] == "Exercise with id 23423423 not found"
    )

    response = test_client.get("/exercises/name/abc")
    assert (
        response.status_code == 404
        and response.json()["detail"] == "Exercise with name abc not found"
    )

    # TODO: how to handle spaces in names
    response = test_client.get("/exercises/name/Partner%20plank%20band%20row")
    print(response.json())
    assert (
        response.status_code == 200
        and response.json()["name"] == "Partner plank band row"
    )


def test_can_get_my_exercises(test_client, seed_test_database, valid_jwt_token):
    response = test_client.get("/exercises/my")
    assert (
        response.status_code == 401 and response.json()["detail"] == "Not authenticated"
    )

    response = test_client.get(
        "/exercises/my", headers={"Authorization": valid_jwt_token}
    )
    assert response.status_code == 200 and len(response.json()) > 0


def test_create_exercise(test_client, seed_test_database, valid_jwt_token):
    response = test_client.post(
        "/exercises",
        json={
            "name": "test",
            "description": "test",
            "exercise_type_id": 1,
            "level_id": 1,
            "target_body_part_id": 1,
        },
        headers={"Authorization": valid_jwt_token},
    )
    assert response.status_code == 201 and response.json()["name"] == "test"

    response = test_client.post(
        "/exercises",
        json={"name": "test", "description": "test"},
    )
    assert (
        response.status_code == 401 and response.json()["detail"] == "Not authenticated"
    )

    response = test_client.post(
        "/exercises",
        json={
            "name": "test",
            "description": "test",
            "exercise_type_id": 1,
            "level_id": 1,
            "target_body_part_id": 1,
        },
        headers={"Authorization": valid_jwt_token},
    )
    assert response.status_code == 409


def create_test_user(client: TestClient, valid_jwt_token: str) -> Response:
    response = client.post(
        "/exercises",
        json={
            "name": "test",
            "description": "test",
            "exercise_type_id": 1,
            "level_id": 1,
            "target_body_part_id": 1,
        },
        headers={"Authorization": valid_jwt_token},
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response


def test_can_update_exercise(
    test_client: TestClient,
    seed_test_database: None,
    valid_jwt_token: str,
    get_test_db: Session,
):
    # Create a user 
    response = create_test_user(test_client, valid_jwt_token)
    created_id = response.json()["id"]
    assert created_id is not None

    # Update the exercise
    response = test_client.put(
        f"/exercises/{created_id}",
        json={
            "name": "new name",
            "description": "new description",
            "exercise_type_id": 2,
            "level_id": 2,
            "target_body_part_id": 2,
        },
        headers={"Authorization": valid_jwt_token},
    )
    if not response.status_code == 200:
        pytest.fail(f"Failed to update exercise: {response.json()}")
    assert response.json()["name"] == "new name"
    assert response.json()["description"] == "new description"

    saved = get_test_db.get(Exercise, created_id)
    assert isinstance(saved, Exercise), "Exercise not found in database"
    assert saved.name == "new name", "name not updated in database"



def test_can_delete_exercise(
    test_client, get_test_db, seed_test_database, valid_jwt_token
):
    response = test_client.delete(
        "/exercises/1", headers={"Authorization": valid_jwt_token}
    )
    assert response.status_code == 200

    response = test_client.delete(
        "/exercises/10000", headers={"Authorization": valid_jwt_token}
    )
    assert (
        response.json()["detail"] == "Exercise with id 10000 not found. Cannot delete."
        and response.status_code == 404
    )

    _create_first_user(get_test_db, "admin@admin.com", "admin", "Admin", False, True)
    # update not yours
    second_jwt = _create_jwt_for_user(2)
    response = test_client.delete("/exercises/2", headers={"Authorization": second_jwt})
    assert (
        response.status_code == 403
        and response.json()["detail"] == "Not enough permissions to delete exercise"
    )
