from playwright.sync_api import APIRequestContext


class Store:
    def __init__(self, api_request_context: APIRequestContext):
        self._request = api_request_context

    def get_pet_inventories_in_store(self, endpoint):
        return self._request.get(endpoint)