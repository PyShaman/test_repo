import logging

import pytest
import requests

from resources.config import ADMIN, PASSWORD, URL
from resources.helpers import generate_random_string


logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def token(request):
    login_payload = {
        "email": request.param,
        "password": PASSWORD
    }
    logger.info(f"Generating token for {request.param['email']}")
    login_response = requests.post(f"{URL}/users/login", json=login_payload, timeout=5)
    access_token = login_response.json()["access_token"]
    yield access_token


@pytest.fixture
def create_brand():
    payload = {"name": f"name_{generate_random_string(8)}", "slug": f"slug_{generate_random_string(8)}"}
    logger.info(f"Executing POST /brands request with payload: {payload}")
    create_brand = requests.post(f"{URL}/brands", json=payload, timeout=5)
    brand_id = create_brand.json()["id"]
    yield create_brand.json()
    login_payload = {
        "email": ADMIN,
        "password": PASSWORD
    }
    login_response = requests.post(f"{URL}/users/login", json=login_payload, timeout=5)
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    logger.info(f"Deleting brand with id: {brand_id}")
    requests.delete(f"{URL}/brands/{brand_id}", headers=headers, timeout=5)
