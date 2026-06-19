import pytest
import os
from playwright.sync_api import Playwright
from dotenv import load_dotenv
from src.pet_utils import Pet
import uuid

load_dotenv()

@pytest.fixture(scope='session')
def api_request_context(playwright: Playwright):
    api_context = playwright.request.new_context(
        base_url= os.getenv('BASE_URL')
    )
    yield api_context
    api_context.dispose()

@pytest.fixture
def pet(api_request_context):
    return Pet(api_request_context)

@pytest.fixture
def pet_cleanup(pet: Pet):
    def _cleanup(pet_id: int):
        pet.delete_pet(f'/v2/pet/{pet_id}')
    yield _cleanup

@pytest.fixture
def init_pet(pet: Pet):
    def _init(pet_data):
        response = pet.create_pet('/v2/pet', data=pet_data.__dict__).json()
        return response
    yield _init

@pytest.fixture
def generate_pet_id():
    yield int(uuid.uuid4().int % 10000)