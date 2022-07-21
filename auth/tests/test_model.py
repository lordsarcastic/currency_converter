from starlette.testclient import TestClient

from conftest import temp_db
from main import app
from auth.models import User

client = TestClient(app)

@temp_db
def test_to_dict_method_will_return_instance_details():
    user = User(
        email="mail@email.com",
        first_name="ahoj",
        last_name="lkjin",
        password="23456"
    )

    dict_details = User.to_dict(user)

    assert "email" in dict_details
    assert "first_name" in dict_details
    assert "last_name" in dict_details
    assert "password" in dict_details
    assert "created_at" in dict_details
    assert "id" in dict_details