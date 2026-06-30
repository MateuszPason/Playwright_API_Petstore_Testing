from src.user_utils import User
import pytest
from src.models.user_models import UserResponse

@pytest.mark.smoke
def test_successful_user_update(user: User, generate_id, new_user, updated_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id
    updated_user.id = user_id

    init_user(new_user)
    user_cleanup(updated_user.username)

    updated_user_response = user.update_user(new_user.username, data=updated_user.model_dump())
    updated_user_response_body = updated_user_response.json()

    assert updated_user_response.ok
    assert updated_user_response_body["code"] == 200
    assert updated_user_response_body["type"] == "unknown"
    assert updated_user_response_body["message"] == str(user_id)

    get_updated_user_body = UserResponse.model_validate(user.get_user(updated_user.username).json())

    assert get_updated_user_body.id == updated_user.id
    assert get_updated_user_body.username == updated_user.username
    assert get_updated_user_body.firstName == updated_user.firstName
    assert get_updated_user_body.lastName == updated_user.lastName
    assert get_updated_user_body.email == updated_user.email
    assert get_updated_user_body.password == updated_user.password
    assert get_updated_user_body.phone == updated_user.phone
    assert get_updated_user_body.userStatus == updated_user.userStatus

@pytest.mark.xfail(reason="Endpoint is broken: Non existing user returns 200 for update", strict=True)
def test_update_non_existing_user(user: User, generate_id, updated_user):
    user_id = generate_id()
    updated_user.id = user_id

    if user.get_user("NonExistingUser").status != 404:
        user.delete_user("NonExistingUser")

    update_response = user.update_user("NonExistingUser", data=updated_user.model_dump())

    assert update_response.status == 404