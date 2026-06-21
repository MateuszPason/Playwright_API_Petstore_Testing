import mimetypes
import os

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

    def upload_image(self, endpoint, file_path=None, additional_metadata=None, **kwargs):
        multipart = {}
        if file_path is not None:
            with open(file_path, "rb") as f:
                multipart["file"] = {
                    "name": os.path.basename(file_path),
                    "mimeType": mimetypes.guess_type(file_path)[0] or "application/octet-stream",
                    "buffer": f.read(),
                }
        if additional_metadata is not None:
            multipart["additionalMetadata"] = additional_metadata
        return self._request.post(endpoint, multipart=multipart, **kwargs)
