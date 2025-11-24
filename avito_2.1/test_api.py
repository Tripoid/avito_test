import requests
import pytest
import random


BASE_URL = "https://qa-internship.avito.com"
POST_ITEM_PATH = "/api/1/item"
GET_ITEM_PATH_TPL = "/api/1/item/{}"
GET_SELLER_ITEMS_PATH_TPL = "/api/1/{}/item"
GET_STATISTIC_PATH_TPL = "/api/1/statistic/{}"

NON_EXISTENT_ID = "00000000-0000-0000-0000-000000000000"
INVALID_FORMAT_ID = "1"
INVALID_SELLER_ID_STR = "abc"


@pytest.fixture(scope="session")
def main_ad_data(base_url, seller_id):
    data = {

        "sellerID": seller_id,
        "name": f"Товар {seller_id} (полные данные)",
        "price": random.randint(100, 100000),

        "statistics": {
            "likes": random.randint(0, 100),
            "viewCount": random.randint(100, 1000),
            "contacts": random.randint(1, 10)
        }
    }
    response = requests.post(base_url + POST_ITEM_PATH, json=data)
    assert response.status_code == 200
    rj = response.json()
    status_msg = rj['status']
    ad_id = status_msg.split(' - ')[1]
    data['id'] = ad_id
    return data


class TestPostItem:

    def test_1_1(self, main_ad_data):

        assert 'id' in main_ad_data
        assert main_ad_data['sellerID'] is not None


    def test_1_2(self, base_url, seller_id):
        data = {"sellerID": seller_id, "name": "Товар (без цены)", "statistics": {"likes": 1, "viewCount": 10, "contacts": 1}}
        response = requests.post(base_url + POST_ITEM_PATH, json=data)
        assert response.status_code == 400

    def test_1_3(self, base_url, seller_id):
        data = {"sellerID": seller_id, "name": "Товар (без статистики)", "price": 100}
        response = requests.post(base_url + POST_ITEM_PATH, json=data)
        assert response.status_code == 400


    def test_1_4(self, base_url, seller_id):
        data = {"sellerID": seller_id, "name": "Товар (цена 0)", "price": 0, "statistics": {"likes": 1, "viewCount": 10, "contacts": 1}}
        response = requests.post(base_url + POST_ITEM_PATH, json=data)

        assert response.status_code == 400

    def test_1_5(self, base_url, seller_id):
        data = {
            "sellerID": seller_id,
            "name": "Товар (лайки 0)",
            "price": 100,
            "statistics": {"likes": 0, "viewCount": 10, "contacts": 1}
        }

        response = requests.post(base_url + POST_ITEM_PATH, json=data)
        assert response.status_code == 400

    @pytest.mark.parametrize("name", [
        "Тест!@#$%^&*()_+", # Тест 1.6
        "Тест Тест 123" # Тест 1.7
    ])

    def test_1_6(self, base_url, seller_id, name):
        data = {"sellerID": seller_id, "name": name, "price": 100, "statistics": {"likes": 1, "viewCount": 10, "contacts": 1}}
        response = requests.post(base_url + POST_ITEM_PATH, json=data)
        assert response.status_code == 200


    def test_1_8(self, base_url, seller_id):
        name = "а" * 1000
        data = {"sellerID": seller_id, "name": name, "price": 1}
        response = requests.post(base_url + POST_ITEM_PATH, json=data)
        assert response.status_code in [200, 400]

    def test_1_9(self, base_url, seller_id):
        data = {"sellerID": seller_id, "name": "Товар (большая цена)", "price": 999999999, "statistics": {"likes": 1, "viewCount": 10, "contacts": 1}}
        response = requests.post(base_url + POST_ITEM_PATH, json=data)

        assert response.status_code == 200

    def test_1_10(self, base_url):
        data = {"sellerID": 111111, "name": "Товар (мин продавец)", "price": 100, "statistics": {"likes": 1, "viewCount": 10, "contacts": 1}}
        response = requests.post(base_url + POST_ITEM_PATH, json=data)

        assert response.status_code == 200

    def test_1_11(self, base_url):
        data = {"sellerID": 999999, "name": "Товар (макс продавец)", "price": 100, "statistics": {"likes": 1, "viewCount": 10, "contacts": 1}}
        response = requests.post(base_url + POST_ITEM_PATH, json=data)
        assert response.status_code == 200



    def test_1_30(self, base_url, seller_id):
        data = {
            "sellerID": seller_id,
            "name": "Товар (лишние поля)",
            "price": 100,
            "statistics": {"likes": 1, "viewCount": 10, "contacts": 1},
            "extra_field": "value"
        }
        response = requests.post(base_url + POST_ITEM_PATH, json=data)
        assert response.status_code == 200



    @pytest.mark.parametrize("payload, case_id", [
        ({}, "Тест 1.12: Пустое тело"),
        ({"name": "Товар", "price": 1}, "Тест 1.13: Нет sellerID"),
        ({"sellerID": 123456, "price": 1}, "Тест 1.14: Нет name"),
        ({"sellerID": None, "name": "Товар"}, "Тест 1.15: sellerID null"),
        ({"sellerID": 123456, "name": None}, "Тест 1.16: name null"),
        ({"sellerID": 123456, "name": ""}, "Тест 1.17: Пустое name"),
        ({"sellerID": "123456", "name": "Товар"}, "Тест 1.18: sellerID строка"),
        ({"sellerID": 123.45, "name": "Товар"}, "Тест 1.19: sellerID дробный"),
        ({"sellerID": -123456, "name": "Товар"}, "Тест 1.20: sellerID отриц"),
        ({"sellerID": 1, "name": "Товар"}, "Тест 1.21: sellerID ниже диапазона"),
        ({"sellerID": 1000000, "name": "Товар"}, "Тест 1.22: sellerID выше диапазона"),
        ({"sellerID": 123456, "name": "Товар", "price": "1000"}, "Тест 1.23: price строка"),
        ({"sellerID": 123456, "name": "Товар", "price": -100}, "Тест 1.24: price отриц"),
        ({"sellerID": 123456, "name": "Товар", "statistics": "stats"}, "Тест 1.25: stats не объект"),
        ({"sellerID": 123456, "name": "Товар", "statistics": {"likes": "10"}}, "Тест 1.26: likes строка"),
        ({"sellerID": 123456, "name": "Товар", "statistics": {"viewCount": -10}}, "Тест 1.27: viewCount отриц"),
    ])


    def test_1_12(self, base_url, payload, case_id):
        response = requests.post(base_url + POST_ITEM_PATH, json=payload)
        assert response.status_code == 400, f"Провал {case_id}"


    def test_1_28(self, base_url):
        headers = {"Content-Type": "application/json"}
        invalid_json = '{"name": "test", "price": 100'
        response = requests.post(base_url + POST_ITEM_PATH, headers=headers, data=invalid_json.encode('utf-8'))
        assert response.status_code == 400

    def test_1_29(self, base_url, seller_id):
        headers = {"Content-Type": "text/plain"}
        data = f"sellerID: {seller_id}, name: 'Test'"
        response = requests.post(base_url + POST_ITEM_PATH, headers=headers, data=data)
        assert response.status_code in [400, 415]


class TestGetItem:
    def test_2_1(self, base_url, main_ad_data):
        ad_id = main_ad_data['id']
        response = requests.get(base_url + GET_ITEM_PATH_TPL.format(ad_id))
        assert response.status_code == 200
        rj = response.json()
        assert isinstance(rj, list)
        assert len(rj) == 1
        ad = rj[0]
        assert ad['id'] == ad_id
        assert ad['name'] == main_ad_data['name']
        assert ad['price'] == main_ad_data['price']
        assert ad['sellerId'] == main_ad_data['sellerID']

    def test_2_3(self, base_url):
        response = requests.get(base_url + GET_ITEM_PATH_TPL.format(NON_EXISTENT_ID))
        assert response.status_code == 404

    def test_2_4(self, base_url):
        response = requests.get(base_url + GET_ITEM_PATH_TPL.format(INVALID_FORMAT_ID))
        assert response.status_code in [400, 404]

    def test_2_5(self, base_url):
        response = requests.get(base_url + "/api/1/item/")
        assert response.status_code in [404, 405]



class TestGetSellerItems:
    def test_3_1(self, base_url, main_ad_data):
        seller_id = main_ad_data['sellerID']
        ad_id = main_ad_data['id']
        response = requests.get(base_url + GET_SELLER_ITEMS_PATH_TPL.format(seller_id))
        assert response.status_code == 200
        rj = response.json()
        assert isinstance(rj, list)
        found_ad = next((item for item in rj if item['id'] == ad_id), None)
        assert found_ad is not None
        assert found_ad['name'] == main_ad_data['name']

    def test_3_3(self, base_url):
        new_seller_id = random.randint(1000000, 2000000)
        response = requests.get(base_url + GET_SELLER_ITEMS_PATH_TPL.format(new_seller_id))
        assert response.status_code == 200
        rj = response.json()
        assert isinstance(rj, list)
        assert len(rj) == 0

    @pytest.mark.parametrize("seller_id, case_id", [
        (INVALID_SELLER_ID_STR, "Тест 3.4: sellerID строка"),
        (-123, "Тест 3.5: sellerID отриц"),
        (123.45, "Тест 3.6: sellerID дробный"),
        (1, "Тест 3.7: sellerID вне диапазона"),
    ])

    def test_3_4(self, base_url, seller_id, case_id):
        response = requests.get(base_url + GET_SELLER_ITEMS_PATH_TPL.format(seller_id))
        assert response.status_code in [200, 400, 404], f"Провал {case_id}"

class TestGetStatistic:

    def test_4_1(self, base_url, main_ad_data):
        ad_id = main_ad_data['id']
        response = requests.get(base_url + GET_STATISTIC_PATH_TPL.format(ad_id))
        assert response.status_code == 200
        rj = response.json()
        assert isinstance(rj, list)
        assert len(rj) == 1
        stats = rj[0]

        assert stats['likes'] == main_ad_data['statistics']['likes']
        assert stats['viewCount'] == main_ad_data['statistics']['viewCount']
        assert stats['contacts'] == main_ad_data['statistics']['contacts']


    def test_4_3(self, base_url):
        response = requests.get(base_url + GET_STATISTIC_PATH_TPL.format(NON_EXISTENT_ID))
        assert response.status_code == 404

    def test_4_4(self, base_url):
        response = requests.get(base_url + GET_STATISTIC_PATH_TPL.format(INVALID_FORMAT_ID))
        assert response.status_code in [400, 404]


    def test_4_5(self, base_url):
        response = requests.get(base_url + "/api/1/statistic/")
        assert response.status_code in [404, 405]