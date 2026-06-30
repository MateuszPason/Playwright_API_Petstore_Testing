from src.user_utils import User
from src.models.user_models import UserResponse
import pytest

@pytest.mark.smoke
def test_successful_user_create(user: User, generate_id, new_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    user_response = user.create_user(data=new_user.model_dump())
    user_cleanup(new_user.username)

    assert user_response.ok

    user_response_body = user_response.json()

    assert user_response_body["code"] == 200
    assert user_response_body["message"] == str(user_id)

@pytest.mark.regression
def test_create_user_response_schema(user: User, generate_id, new_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    user_response = user.create_user(data=new_user.model_dump())
    user_cleanup(new_user.username)
    user_response_body = user_response.json()

    assert "code" in user_response_body
    assert "type" in user_response_body
    assert "message" in user_response_body

    assert type(user_response_body["code"]) is int
    assert type(user_response_body["type"]) is str
    assert type(user_response_body["message"]) is str

@pytest.mark.regression
def test_create_user_persists(user: User, generate_id, new_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    user.create_user(data=new_user.model_dump())

    get_user_response = user.get_user(new_user.username)
    user_cleanup(new_user.username)
    get_user_response_body = UserResponse.model_validate(get_user_response.json())

    assert get_user_response_body.id == new_user.id
    assert get_user_response_body.username == new_user.username
    assert get_user_response_body.firstName == new_user.firstName
    assert get_user_response_body.lastName == new_user.lastName
    assert get_user_response_body.email == new_user.email
    assert get_user_response_body.password == new_user.password
    assert get_user_response_body.phone == new_user.phone
    assert get_user_response_body.userStatus == new_user.userStatus

@pytest.mark.regression
def test_create_user_with_no_body(user: User):
    user_response = user.create_user()

    assert user_response.status == 415