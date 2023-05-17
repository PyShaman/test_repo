import requests

from resources.config import URL
from resources.helpers import generate_random_string


def test_001_get_brands():
    response = requests.get(f"{URL}/brands")

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert len(response.json()) > 0, "Brands list is empty"


def test_002_post_brand():
    brand = generate_random_string(6)
    payload = {
        "name": f"new brand {brand}",
        "slug": f"new-brand-{brand}"
    }

    response = requests.post(f"{URL}/brands", json=payload)

    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert response.json()["name"] == payload["name"], f"Unexpected response payload name: {response.json()['name']}"
    assert response.json()["slug"] == payload["slug"], f"Unexpected response payload slug: {response.json()['slug']}"


def test_003_put_brand():
    brand = generate_random_string(6)
    payload = {
        "name": f"new brand {brand}",
        "slug": f"new-brand-{brand}"
    }

    response_post = requests.post(f"{URL}/brands", json=payload)
    brand_id = response_post.json()["id"]
    payload_update = {
        "name": f"new brand {brand} upd",
        "slug": f"new-brand-{brand}-upd"
    }
    response_update = requests.put(f"{URL}/brands/{brand_id}", json=payload_update)

    assert response_update.status_code == 200, f"Unexpected status code: {response_update.status_code}"
    assert response_update.json()["success"] is True


def test_004_delete_brand():
    login_payload = {
        "email": "admin@practicesoftwaretesting.com",
        "password": "welcome01"
    }
    login_response = requests.post(f"{URL}/users/login", json=login_payload)
    access_token = login_response.json()["access_token"]

    brand = generate_random_string(6)
    payload = {
        "name": f"new brand {brand}",
        "slug": f"new-brand-{brand}"
    }

    response_post = requests.post(f"{URL}/brands", json=payload)
    brand_id = response_post.json()["id"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response_delete = requests.delete(f"{URL}/brands/{brand_id}", headers=headers)
    assert response_delete.status_code == 204, f"Unexpected status code: {response_delete.status_code}"
