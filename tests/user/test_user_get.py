from src.user_utils import User
from src.models.user_models import UserResponse
import pytest

@pytest.mark.smoke
def test_get_existing_user(user: User, generate_id, init_user, new_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    get_user_response = user.get_user(new_user.username)
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
def test_get_non_existing_user(user: User, generate_id, new_user):
    user_id = generate_id()
    new_user.id = user_id

    get_user_pre_delete = user.get_user(new_user.username)

    if get_user_pre_delete.status != 404:
        user.delete_user(new_user.username)

    get_user_post_delete = user.get_user(new_user.username)
    get_user_post_delete_response = get_user_post_delete.json()

    assert get_user_post_delete.status == 404
    assert get_user_post_delete_response["type"] == "error"
    assert get_user_post_delete_response["message"] == "User not found"

@pytest.mark.parametrize("invalid_username", [0, True, False, "", "  "])
def test_invalid_username(user: User, invalid_username):
    with pytest.raises(ValueError, match="Incorrect username"):
        user.get_user(invalid_username)
