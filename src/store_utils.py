from playwright.sync_api import APIRequestContext


class Store:
    def __init__(self, api_request_context: APIRequestContext):
        self._request = api_request_context

    def get_pet_inventories_in_store(self, endpoint, **kwargs):
        return self._request.get(endpoint, **kwargs)

    def get_order_by_id(self, order_id, **kwargs):
        if not isinstance(order_id, int) or isinstance(order_id, bool) or order_id <= 0:
            raise ValueError("Incorrect order_id | Expected int value > 0")
        return self._request.get(f"/v2/store/order/{order_id}", **kwargs)

    def place_an_order(
        self, order_id, pet_id, quantity, ship_date, status, complete, **kwargs
    ):
        if not isinstance(order_id, int) or isinstance(order_id, bool) or order_id <= 0:
            raise ValueError("Incorrect order_id | Expected int value > 0")
        if not isinstance(pet_id, int) or isinstance(pet_id, bool) or pet_id <= 0:
            raise ValueError("Incorrect pet_id | Expected int value > 0")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Incorrect quantity | Expected int value > 0")
        if not isinstance(ship_date, str) or not ship_date:
            raise ValueError("Incorrect ship_date | Expected string value")
        if not isinstance(status, str) or status not in [
            "placed",
            "approved",
            "delivered",
        ]:
            raise ValueError(
                "Incorrect status | Expected string value of 'placed', 'approved' or 'delivered'"
            )
        if not isinstance(complete, bool):
            raise ValueError("Incorrect complete value | Expected true or false")
        return self._request.post(
            "/v2/store/order",
            data={
                "id": order_id,
                "petId": pet_id,
                "quantity": quantity,
                "shipDate": ship_date,
                "status": status,
                "complete": complete,
            },
            **kwargs,
        )

    def delete_an_order(self, order_id):
        if not isinstance(order_id, int) or isinstance(order_id, bool) or order_id <= 0:
            raise ValueError("Incorrect order_id | Expected int value > 0")
        return self._request.delete(f"/v2/store/order/{order_id}")