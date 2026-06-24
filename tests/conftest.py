import pytest
import os
from playwright.sync_api import Playwright, APIRequestContext
from dotenv import load_dotenv
from src.pet_utils import Pet
from src.store_utils import Store
import uuid
from tests.payloads.pet_payloads import PetPayload
import secrets
import string
from datetime import datetime, timezone

load_dotenv()

@pytest.fixture(scope='session')
def api_request_context(playwright: Playwright):
    api_context = playwright.request.new_context(
        base_url= os.getenv('BASE_URL')
    )
    yield api_context
    api_context.dispose()

@pytest.fixture
def pet(api_request_context: APIRequestContext):
    return Pet(api_request_context)

@pytest.fixture
def store(api_request_context: APIRequestContext):
    return Store(api_request_context)

@pytest.fixture
def pet_cleanup(pet: Pet):
    def _cleanup(pet_id: int):
        return pet.delete_pet(pet_id)
    return _cleanup

@pytest.fixture
def init_pet(pet: Pet):
    def _init(pet_data: PetPayload):
        return pet.create_pet(data=pet_data.__dict__)
    return _init

@pytest.fixture
def generate_pet_id():
    def _generate():
        return int(uuid.uuid4().int % 100000)
    return _generate

@pytest.fixture
def generate_random_string(length=8):
    def _generate():
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))
    return _generate

@pytest.fixture
def generate_order_id():
    def _generate():
        return int(uuid.uuid4().int % 990) + 11
    return _generate

@pytest.fixture
def ship_date():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "+0000")

@pytest.fixture
def create_order(store: Store):
    def _init(order_id, pet_id, quantity, ship_date, status, complete):
        return store.place_an_order(order_id, pet_id, quantity, ship_date, status, complete)
    return _init

@pytest.fixture
def order_cleanup(store: Store):
    def _cleanup(order_id):
        return store.delete_an_order(order_id)
    return _cleanup