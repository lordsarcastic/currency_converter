from starlette.testclient import TestClient

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

payload = {
    'from_currency': 'usd',
    'to_currency': 'ngn',
    "amount": 30
}

payload2 = {
    'from_currency': 'usd',
    'to_currency': 'jpy',
    "amount": 33
}

@temp_db
def test_authenticated_user_can_get_list_of_currencies():
    response = client.get(
        '/api/v1/currencies/list',
    )

    assert response.status_code == 200
    assert "currencies" in response.json()
    assert bool(response.json()['currencies']) == True

@temp_db
def test_unauthenticated_user_can_get_list_of_currencies():
    response = client.get(
        '/api/v1/currencies/list',
    )

    assert response.status_code == 200
    assert "currencies" in response.json()
    assert bool(response.json()['currencies']) == True

@temp_db
def test_authenticated_user_can_convert_currency():
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

    access_token = response.json()['access_token']
    response = client.post(
        "/api/v1/currencies/convert",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert "to_currency" in response.json()
    assert "from_currency" in response.json()
    assert "amount" in response.json()
    assert "rate" in response.json()
    assert "result" in response.json()

@temp_db
def test_unauthenticated_user_cannot_convert_currency():
    access_token = 'access_token'
    response = client.post(
        "/api/v1/currencies/convert",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403
    assert "detail" in response.json()

@temp_db
def test_history_can_be_seen_by_authenticated_user():
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

    access_token = response.json()['access_token']
    response = client.post(
        "/api/v1/currencies/convert",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert "to_currency" in response.json()
    assert "from_currency" in response.json()
    assert "amount" in response.json()
    assert "rate" in response.json()
    assert "result" in response.json()

    response = client.get(
        "/api/v1/currencies/history",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) == 1

@temp_db
def test_history_cannot_be_seen_by_unauthenticated_user():
    access_token = 'access_token'
    response = client.get(
        "/api/v1/currencies/history",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403
    assert "detail" in response.json()
    assert response.json()['detail'] == "Could not validate credentials"

@temp_db
def test_history_can_be_filtered_by_from_currency():
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

    access_token = response.json()['access_token']
    response = client.post(
        "/api/v1/currencies/convert",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert "to_currency" in response.json()
    assert "from_currency" in response.json()
    assert "amount" in response.json()
    assert "rate" in response.json()
    assert "result" in response.json()

    response = client.post(
        "/api/v1/currencies/convert",
        json=payload2,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert "to_currency" in response.json()
    assert "from_currency" in response.json()
    assert "amount" in response.json()
    assert "rate" in response.json()
    assert "result" in response.json()

    response = client.post(
        "/api/v1/currencies/convert",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert "to_currency" in response.json()
    assert "from_currency" in response.json()
    assert "amount" in response.json()
    assert "rate" in response.json()
    assert "result" in response.json()

    response = client.get(
        "/api/v1/currencies/history?from_currency=usd",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) == 3

@temp_db
def test_history_can_be_filtered_by_to_currency():
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

    access_token = response.json()['access_token']
    response = client.post(
        "/api/v1/currencies/convert",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert "to_currency" in response.json()
    assert "from_currency" in response.json()
    assert "amount" in response.json()
    assert "rate" in response.json()
    assert "result" in response.json()

    response = client.post(
        "/api/v1/currencies/convert",
        json=payload2,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert "to_currency" in response.json()
    assert "from_currency" in response.json()
    assert "amount" in response.json()
    assert "rate" in response.json()
    assert "result" in response.json()

    response = client.post(
        "/api/v1/currencies/convert",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert "to_currency" in response.json()
    assert "from_currency" in response.json()
    assert "amount" in response.json()
    assert "rate" in response.json()
    assert "result" in response.json()

    response = client.get(
        "/api/v1/currencies/history?to_currency=ngn",
        json=payload,
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) == 2
