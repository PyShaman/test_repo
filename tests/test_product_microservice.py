import allure
import requests

from datetime import timedelta

from assertpy import assert_that, soft_assertions

from resources.config import URL


@allure.description("""
Test type: Positive and Negative

Test microservice: Products

Test description: Suite is responsible for verifying proper functionality for /products microservice.

Endpoint: GET /products Description: This endpoint allows you to retrieve a list of products from the system. The 
response contains detailed information about each product, such as name, identifier (ID), price and other data 
related to the product. This is useful for displaying the list of products in the user interface or other operations 
that require access to product information.

Endpoint: POST /products Description: This endpoint allows you to add a new product to the system. It requires you to 
submit product data such as name, price, description and other related information. When the product is successfully 
created, the response contains the identifier (ID) of the created product and other details.

Endpoint: GET /products/{id} Description: This endpoint allows you to retrieve detailed information about a specific 
product based on its identifier (ID). It returns all available product data, such as name, price, description, 
ID and other related information.

Endpoint: PUT /products/{id} Description: This endpoint allows you to update the data of a specific product based on 
its identifier (ID). It requires the updated product data to be submitted, which will be applied to the existing 
product information. After a successful update, the response contains the updated product details.

Endpoint: DELETE /products/{id} Description: This endpoint allows you to delete a specific product based on its 
identifier (ID). After successful deletion, the response confirms the deletion operation.
""")
class TestProductMicroservice:

    def test_001_positive_get_products(self):
        response = requests.get(f"{URL}/products", params={"sort": "name,asc"}, timeout=5)
        response_2 = requests.get(f"{URL}/products", params={"sort": "name,asc"}, timeout=5)
        response_data = [data["name"] for data in response.json()["data"]]
        with soft_assertions():
            # status code verification
            assert_that(response.status_code).is_equal_to(200)
            # response payload verification
            assert_that(response.json()).is_instance_of(dict)
            assert_that(response.json()["data"][0]["id"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["name"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["description"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["stock"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["price"]).is_instance_of(float)
            assert_that(response.json()["data"][0]["is_location_offer"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["is_rental"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["brand_id"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["category_id"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["product_image_id"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["product_image"]).is_instance_of(dict)
            assert_that(response.json()["data"][0]["product_image"]["id"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["product_image"]["by_name"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["product_image"]["by_url"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["product_image"]["source_name"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["product_image"]["source_url"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["product_image"]["file_name"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["product_image"]["title"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["category"]).is_instance_of(dict)
            assert_that(response.json()["data"][0]["category"]["id"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["category"]["parent_id"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["category"]["name"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["category"]["slug"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["brand"]).is_instance_of(dict)
            assert_that(response.json()["data"][0]["brand"]["id"]).is_instance_of(int)
            assert_that(response.json()["data"][0]["brand"]["name"]).is_instance_of(str)
            assert_that(response.json()["data"][0]["brand"]["slug"]).is_instance_of(str)
            assert_that(response_data).is_equal_to(sorted(response_data))
            # response headers verification
            assert_that(response.headers["cache-control"]).is_equal_to("no-cache, private")
            assert_that(response.headers["content-type"]).is_equal_to("application/json;charset=UTF-8")
            # response performance verification
            assert_that(response.elapsed).is_less_than_or_equal_to(timedelta(milliseconds=800))
            # state validation
            assert_that(response.json()).is_equal_to(response_2.json())
