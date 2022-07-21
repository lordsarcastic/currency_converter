from starlette.testclient import TestClient
from auth.services import create_auth_token

from conftest import temp_db
from main import app

client = TestClient(app)


user = {
    "email": "foo@goo.mail",
    "first_name": "Ayodeji",
    "last_name": "Adeoti",
    "password": "11111111"
}

credentials = {
    "username": user["email"],
    "password": user["password"]
}

@temp_db
def test_create_user():
    response = client.post(
        "/api/v1/user/signup",
        json=user
    )
    assert response.status_code == 200
    assert "email" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "created_at" in response.json()

@temp_db
def test_duplicate_user_cannot_be_created():
    response = client.post(
        "/api/v1/user/signup",
        json=user
    )
    assert response.status_code == 200
    assert "email" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "created_at" in response.json()

    response = client.post(
        "/api/v1/user/signup",
        json=user
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()['detail'] == "User with this email already exists"


@temp_db
def test_created_user_can_login():
    response = client.post(
        "/api/v1/user/signup",
        json=user
    )

    assert response.status_code == 200
    assert "email" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "created_at" in response.json()
    
    response = client.post(
        "/api/v1/user/login",
        data=credentials
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@temp_db
def test_user_with_incorrect_details_cannot_login():
    response = client.post(
        "/api/v1/user/signup",
        json=user
    )
    credentials = {
    "username": user["email"],
    "password": "Hallo"
}

    assert response.status_code == 200
    assert "email" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "created_at" in response.json()

    response = client.post(
        "/api/v1/user/login",
        data=credentials
    )

    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()['detail'] == "Email or password is incorrect. Incorrect login credentials"

@temp_db
def test_logged_in_user_can_grab_their_own_details():
    response = client.post(
        "/api/v1/user/signup",
        json=user
    )

    assert response.status_code == 200
    assert "email" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "created_at" in response.json()
    
    response = client.post(
        "/api/v1/user/login",
        data=credentials
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    response = client.get(
        "/api/v1/user/me",
        headers={
            'Authorization': f"Bearer {response.json()['access_token']}"
        }
    )

    assert response.status_code == 200
    assert "email" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "created_at" in response.json()

@temp_db
def test_user_with_wrong_token_cannot_view_details():
    response = client.get(
        "/api/v1/user/me",
        headers={
            'Authorization': f"Bearer wrongtoeknabouttheworkd"
        }
    )
    assert response.status_code == 403
    assert response.json()['detail'] == "Could not validate credentials"

@temp_db
def test_user_with_expired_token_cannot_view_details():
    response = client.post(
        "/api/v1/user/signup",
        json=user
    )

    assert response.status_code == 200
    assert "email" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "created_at" in response.json()

    payload = response.json()
    access_token = create_auth_token(payload, 0)
    response = client.get(
        "/api/v1/user/me",
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )
    assert response.status_code == 401
    assert response.json()['detail'] == "Token expired"