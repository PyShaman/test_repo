import random
import string

import allure
import pytest
import requests

from datetime import timedelta

from assertpy import assert_that, soft_assertions

from resources.config import URL, ADMIN, USER1
from resources.helpers import generate_random_string


@allure.description("""
Test type: Positive and Negative

Test microservice: Brands

Test description: Suite is responsible for verifying proper functionality for /brands microservice.

Endpoint: GET /brands
Description: This endpoint allows you to retrieve a list of brands from the system. The response contains detailed
information about each brand, such as name, identifier (ID) and other brand-related data. This is useful for displaying
the list of brands in the user interface or other operations that require access to brand information.

Endpoint: POST /brands Description: This endpoint allows you to add a new brand to the system. It requires the 
submission of brand data, such as name and other related information. Once the brand is successfully created, 
the response contains the identifier (ID) of the created brand and other details.

Endpoint: GET /brands/{id}
Description: This endpoint allows you to retrieve detailed information about a specific brand based on its identifier
(ID). It returns all available brand data, such as name, ID and other related information.

Endpoint: PUT /brands/{id}
Description: This endpoint allows updating the data of a specific brand based on its identifier (ID). It requires the
updated brand data to be passed, which will be applied to the existing brand information. After a successful update,
the response contains the updated brand details.

Endpoint: DELETE /brands/{id}
Description: This endpoint allows you to delete a specific brand based on its identifier (ID). After successful
deletion, the response confirms the deletion operation.
""")
class TestBrandsMicroservice:
    def test_001_positive_get_brands(self):
        response = requests.get(f"{URL}/brands", timeout=5)
        response_2 = requests.get(f"{URL}/brands", timeout=5)
        with soft_assertions():
            # status code verification
            assert_that(response.status_code).is_equal_to(200)
            # response payload verification
            assert_that(response.json()).is_instance_of(list)
            assert_that(response.json()[0]["id"]).is_instance_of(int)
            assert_that(response.json()[0]["name"]).is_instance_of(str)
            assert_that(response.json()[0]["slug"]).is_instance_of(str)
            # response headers verification
            assert_that(response.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response.headers["content-type"]).is_equal_to("application/json;charset=UTF-8")
            # response performance verification
            assert_that(response.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))
            # state validation
            assert_that(response.json()).is_equal_to(response_2.json())

    def test_002_negative_post_brand_with_existing_slug(self):
        name_suffix = generate_random_string(6)
        new_name_suffix = generate_random_string(6)
        slug_suffix = generate_random_string(6)
        payload_1 = {
            "name": f"new brand {name_suffix}",
            "slug": f"new-brand-{slug_suffix}"
        }
        response_1 = requests.post(f"{URL}/brands", json=payload_1, timeout=5)
        assert_that(response_1.status_code).is_equal_to(201)

        payload_2 = {
            "name": f"new brand {new_name_suffix}",
            "slug": f"new-brand-{slug_suffix}"
        }
        response_2 = requests.post(f"{URL}/brands", json=payload_2, timeout=5)

        with soft_assertions():
            assert_that(response_2.status_code).is_equal_to(422)
            assert_that(response_2.json()["slug"][0]).is_equal_to("A brand already exists with this slug.")
            # response headers verification
            assert_that(response_2.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response_2.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response_2.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_003_negative_post_brand_with_existing_name(self, create_brand):
        name_suffix = create_brand["name"]
        new_slug_suffix = generate_random_string(6)

        payload_2 = {
            "name": f"new brand {name_suffix}",
            "slug": f"new-brand-{new_slug_suffix}"
        }
        response_2 = requests.post(f"{URL}/brands", json=payload_2, timeout=5)

        with soft_assertions():
            assert_that(response_2.status_code).is_equal_to(422)
            assert_that(response_2.json()["name"][0]).is_equal_to("A brand already exists with this name.")
            # response headers verification
            assert_that(response_2.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response_2.headers["content-type"]).is_equal_to("application/json;charset=UTF-8")
            # response performance verification
            assert_that(response_2.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_004_negative_post_brand_with_existing_name_and_brand(self, create_brand):
        payload = create_brand
        del payload["id"]

        response_2 = requests.post(f"{URL}/brands", json=payload, timeout=5)

        with soft_assertions():
            assert_that(response_2.status_code).is_equal_to(422)
            assert_that(response_2.json()["slug"][0]).is_equal_to("A brand already exists with this slug.")
            # response headers verification
            assert_that(response_2.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response_2.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response_2.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    @pytest.mark.parametrize("token", [{"email": ADMIN}], indirect=True)
    def test_005_negative_delete_not_existing_brand(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL}/brands/99999999", headers=headers)
        with soft_assertions():
            assert_that(response.status_code).is_equal_to(422)
            assert_that(response.json()["id"][0]).is_equal_to("The selected id is invalid.")
            # response headers verification
            assert_that(response.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_006_negative_update_name_and_slug_to_existing_one(self):
        response_1 = requests.get(f"{URL}/brands", timeout=5)
        assert_that(response_1.status_code).is_equal_to(200)
        existing_brand_payload = response_1.json()[0]
        del existing_brand_payload["id"]

        name_suffix = generate_random_string(6)
        slug_suffix = generate_random_string(6)
        payload = {
            "name": f"new brand {name_suffix}",
            "slug": f"new-brand-{slug_suffix}"
        }

        response_2 = requests.post(f"{URL}/brands", json=payload, timeout=5)
        brand_id = response_2.json()["id"]
        assert_that(response_2.status_code).is_equal_to(201)

        response_3 = requests.put(f"{URL}/brands/{brand_id}", json=existing_brand_payload, timeout=5)
        with soft_assertions():
            assert_that(response_3.status_code).is_equal_to(422)
            assert_that(response_3.json()["message"]).is_equal_to("Duplicate Entry")
            # response headers verification
            assert_that(response_3.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response_3.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response_3.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_007_negative_create_brand_with_missing_data(self):
        payload = {
            "name": None,
            "slug": None
        }

        response = requests.post(f"{URL}/brands", json=payload, timeout=5)
        with soft_assertions():
            assert_that(response.status_code).is_equal_to(422)
            assert_that(response.json()["name"][0]).is_equal_to("The name field is required.")
            assert_that(response.json()["slug"][0]).is_equal_to("The slug field is required.")
            # response headers verification
            assert_that(response.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_009_negative_perform_delete_on_search_endpoint(self):
        response = requests.post(f"{URL}/brands/search", params={"q": "new"}, timeout=5)
        with soft_assertions():
            assert_that(response.status_code).is_equal_to(405)
            assert_that(response.json()).contains_value("Method is not allowed for the requested route")
            # response headers verification
            assert_that(response.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_010_destructive_create_brand_with_incorrect_payload(self):
        name = f"name_{generate_random_string(500)}"
        slug = f"slug_{generate_random_string(500)}"
        payload = {
            "name": name,
            "slug": slug
        }
        response = requests.post(f"{URL}/brands", json=payload, timeout=5)
        with soft_assertions():
            assert_that(response.status_code).is_equal_to(422)
            assert_that(response.json()["name"][0]).is_equal_to(
                "The name may not be greater than 120 characters."
            )
            assert_that(response.json()["slug"][0]).is_equal_to(
                "The slug may not be greater than 120 characters."
            )
            # response headers verification
            assert_that(response.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_011_destructive_create_brand_with_empty_payload(self):
        response = requests.post(f"{URL}/brands", json={}, timeout=5)
        with soft_assertions():
            assert_that(response.status_code).is_equal_to(422)
            assert_that(response.json()["name"][0]).is_equal_to("The name field is required.")
            assert_that(response.json()["slug"][0]).is_equal_to("The slug field is required.")
            # response headers verification
            assert_that(response.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_012_destructive_create_brand_with_invalid_payload(self):
        payload = {
            "name": {f"name_{generate_random_string(8)}": 0},
            "slug": [f"name_{generate_random_string(8)}"],
        }
        response = requests.post(f"{URL}/brands", json=payload, timeout=5)
        with soft_assertions():
            assert_that(response.status_code).is_equal_to(422)
            assert_that(response.json()["name"][0]).is_equal_to("The name must be a string.")
            assert_that(response.json()["slug"][0]).is_equal_to("The slug must be a string.")
            # response headers verification
            assert_that(response.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    @pytest.mark.parametrize("token", [{"email": ADMIN}], indirect=True)
    def test_013_positive_delete_brand_auth_user(self, token, create_brand):
        brand_id = create_brand["id"]
        headers = {"Authorization": f"Bearer {token}"}

        response_del = requests.delete(f"{URL}/brands/{brand_id}", headers=headers, timeout=5)
        with soft_assertions():
            assert_that(response_del.status_code).is_equal_to(204)
            # response headers verification
            assert_that(response_del.headers).does_not_contain_key("Server")  # server information leakage
            assert_that(response_del.headers["Access-Control-Allow-Origin"]).is_equal_to("*")
            assert_that(response_del.headers["Cache-Control"]).is_equal_to("no-cache, private")
            # response performance verification
            assert_that(response_del.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    def test_014_negative_reject_unauthorized_delete(self, create_brand):
        brand_id = create_brand["id"]

        headers = {"Authorization": f"Bearer fake_token"}
        response_del = requests.delete(f"{URL}/brands/{brand_id}", headers=headers, timeout=5)
        with soft_assertions():
            assert_that(response_del.status_code).is_equal_to(401)
            assert_that(response_del.json()["message"]).is_equal_to("Unauthorized")
            # response headers verification
            assert_that(response_del.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response_del.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response_del.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))

    @pytest.mark.parametrize("token", [USER1])
    def test_015_negative_reject_insufficient_permission_delete(self, create_brand, token):
        brand_id = create_brand["id"]
        headers = {"Authorization": f"Bearer {token}"}

        response_del = requests.delete(f"{URL}/brands/{brand_id}", headers=headers, timeout=5)
        with soft_assertions():
            assert_that(response_del.status_code).is_equal_to(401)
            assert_that(response_del.json()["message"]).is_equal_to("Unauthorized")
            # response headers verification
            assert_that(response_del.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response_del.headers["content-type"]).is_equal_to("application/json")
            # response performance verification
            assert_that(response_del.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))
