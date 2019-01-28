from flask.testing import FlaskClient


def test_items_seeded(client: FlaskClient) -> None:
    result = client.get("/items/")
    items = [i["attributes"] for i in result.json["data"]["data"]]
    assert items == [
        {"description": "A delicious pizza.", "name": "Pizza", "price": 8.99},
        {"description": "A tasty burger.", "name": "Burger", "price": 6.44},
    ]
