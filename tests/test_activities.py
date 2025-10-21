import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


def test_get_activities_returns_dict():
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    client = TestClient(app)
    test_email = "testuser@example.com"
    activity = "Programming Class"

    # Ensure email not present initially
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_del = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert resp_del.status_code == 200
    assert test_email not in activities[activity]["participants"]


def test_unregister_nonexistent_returns_404():
    client = TestClient(app)
    test_email = "doesnotexist@example.com"
    activity = "Gym Class"

    # Ensure email not present
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    resp = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert resp.status_code == 404
