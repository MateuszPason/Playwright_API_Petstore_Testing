from src.user_utils import User
import pytest

@pytest.mark.smoke
def test_successful_user_logout(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    user.login_user(new_user.username, new_user.password)

    logout_response = user.logout_user()
    logout_response_body = logout_response.json()

    assert logout_response.ok
    assert logout_response_body["code"] == 200
    assert logout_response_body["type"] == "unknown"
    assert logout_response_body["message"] == "ok"