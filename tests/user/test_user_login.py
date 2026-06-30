from src.user_utils import User
import pytest
from datetime import datetime, timezone

@pytest.mark.smoke
def test_successful_user_login(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    login_response = user.login_user(new_user.username, new_user.password)
    login_response_body = login_response.json()

    assert login_response.ok
    assert login_response_body["code"] == 200
    assert "logged in user session" in login_response_body["message"]

@pytest.mark.regression
def test_response_body_contains_required_fields(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    login_response = user.login_user(new_user.username, new_user.password)
    login_response_body = login_response.json()

    assert "code" in login_response_body
    assert "type" in login_response_body
    assert "message" in login_response_body

@pytest.mark.regression
def test_response_has_x_rate_limit_header(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id
    
    init_user(new_user)
    user_cleanup(new_user.username)
    
    login_response = user.login_user(new_user.username, new_user.password)
    login_response_headers = login_response.headers

    assert "x-rate-limit" in login_response_headers.keys()
    assert int(login_response_headers["x-rate-limit"]) > 1000

@pytest.mark.regression
def test_response_has_x_expires_after_header(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    login_response = user.login_user(new_user.username, new_user.password)
    login_response_headers = login_response.headers

    assert "x-expires-after" in login_response_headers

    date_format = "%a %b %d %H:%M:%S UTC %Y"
    now_utc = datetime.now(timezone.utc)
    now_str = now_utc.strftime(date_format)
    assert now_str < login_response_headers["x-expires-after"]

@pytest.mark.regression
def test_session_token_is_unique_per_login(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    first_login_response_body = user.login_user(new_user.username, new_user.password).json()
    second_login_response_body = user.login_user(new_user.username, new_user.password).json()

    first_login_message, first_login_token = first_login_response_body["message"].split(":")
    second_login_message, second_login_token = second_login_response_body["message"].split(":")

    assert first_login_token != second_login_token

@pytest.mark.parametrize("invalid_username", [1, True, False, "", "  "])
def test_incorrect_username(user: User, invalid_username):
    with pytest.raises(ValueError, match="Incorrect username"):
        user.login_user(invalid_username, "Test1234")

@pytest.mark.parametrize("invalid_password", [1, True, False, "", "  "])
def test_incorrect_password(user: User, invalid_password):
    with pytest.raises(ValueError, match="Incorrect password"):
        user.login_user("Test", invalid_password)

@pytest.mark.xfail(reason="Endpoint is broken: invalid credentials return 200", strict=True)
def test_invalid_password_returns_400(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    login_response = user.login_user(new_user.username, "IncorrectPassword")

    assert login_response.status == 400

@pytest.mark.xfail(reason="Endpoint is broken: invalid credentials return 200", strict=True)
def test_invalid_username_returns_400(user: User, generate_id, new_user, init_user, user_cleanup):
    user_id = generate_id()
    new_user.id = user_id

    init_user(new_user)
    user_cleanup(new_user.username)

    login_response = user.login_user("InvalidUsername", new_user.password)

    assert login_response.status == 400