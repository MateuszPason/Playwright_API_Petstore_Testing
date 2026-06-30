from playwright.sync_api import APIRequestContext


class User:
    def __init__(self, api_request_context: APIRequestContext):
        self._request = api_request_context

    def create_user(self, **kwargs):
        return self._request.post("/v2/user", **kwargs)

    def delete_user(self, username, **kwargs):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Incorrect username | Expected a non empty string")
        return self._request.delete(f"/v2/user/{username}", **kwargs)

    def get_user(self, username, **kwargs):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Incorrect username | Expected a non empty string")
        return self._request.get(f"/v2/user/{username}", **kwargs)

    def update_user(self, username, **kwargs):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Incorrect username | Expected a non empty string")
        return self._request.put(f"/v2/user/{username}", **kwargs)

    def login_user(self, username, password, **kwargs):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Incorrect username | Expected a non empty string")
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Incorrect password | Expected a non empty string")
        return self._request.get(f"/v2/user/login?username={username}&password={password}", **kwargs)

    def logout_user(self, **kwargs):
        return self._request.get("/v2/user/logout", **kwargs)