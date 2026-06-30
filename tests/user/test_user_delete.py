from src.user_utils import User
from src.models.user_models import UserResponse
import pytest

@pytest.mark.smoke
def test_successful_user_delete(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    get_existing_user_response = user.get_user(new_user.username)
    get_existing_user_response_body = UserResponse.model_validate(get_existing_user_response.json())
    assert get_existing_user_response.ok
    assert get_existing_user_response_body.id == new_user.id


    user_delete_response = user.delete_user(new_user.username)

    assert user_delete_response.ok

    get_user_response = user.get_user(new_user.username)
    get_user_response_body = get_user_response.json()

    assert get_user_response.status == 404
    assert get_user_response_body["message"] == "User not found"

@pytest.mark.regression
def test_user_delete_response_body(user: User, generate_id, init_user, new_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    delete_user_response = user.delete_user(new_user.username)
    delete_user_response_body = delete_user_response.json()

    assert delete_user_response.ok
    assert delete_user_response_body["message"] == new_user.username

@pytest.mark.parametrize("invalid_username", [0, True, False, "", "  "])
def test_incorrect_username(user: User, invalid_username):
    with pytest.raises(ValueError, match="Incorrect username"):
        user.delete_user(invalid_username)

@pytest.mark.regression
def test_delete_non_existing_user(user: User, generate_id, new_user):
    user_id = generate_id()
    new_user.id = user_id

    get_user_response = user.get_user(new_user.username)

    if get_user_response.status != 404:
        user.delete_user(new_user.username)

    delete_response = user.delete_user(new_user.username)

    assert delete_response.status == 404

