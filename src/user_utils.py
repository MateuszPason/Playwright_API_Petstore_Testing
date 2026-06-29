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

    