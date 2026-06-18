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
