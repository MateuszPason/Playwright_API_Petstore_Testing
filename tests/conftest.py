import pytest
import os
from playwright.sync_api import Playwright, APIRequestContext
from dotenv import load_dotenv
from src.pet_utils import Pet
import uuid
from tests.payloads.pet_payloads import PetPayload

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
def pet_cleanup(pet: Pet):
    def _cleanup(pet_id: int):
        return pet.delete_pet(f'/v2/pet/{pet_id}')
    return _cleanup

@pytest.fixture
def init_pet(pet: Pet):
    def _init(pet_data: PetPayload):
        return pet.create_pet('/v2/pet', data=pet_data.__dict__)
    return _init

@pytest.fixture
def generate_pet_id():
    return int(uuid.uuid4().int % 100000)