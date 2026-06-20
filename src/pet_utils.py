from playwright.sync_api import APIRequestContext


class Pet:
    def __init__(self, api_request_context: APIRequestContext):
        self._request = api_request_context

    def create_pet(self, endpoint, **kwargs):
        return self._request.post(endpoint, **kwargs)

    def get_pet(self, endpoint, **kwargs):
        return self._request.get(endpoint, **kwargs)

    def update_pet(self, endpoint, **kwargs):
        return self._request.put(endpoint, **kwargs)

    def delete_pet(self, endpoint, **kwargs):
        return self._request.delete(endpoint, **kwargs)

    def get_pet_by_status(self, endpoint, status=None, **kwargs):
        params = kwargs.pop("params", {}) or {}
        if status is not None:
            params["status"] = status
        return self._request.get(endpoint, params=params, **kwargs)
