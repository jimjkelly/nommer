from flask.testing import FlaskClient


def test_orders_empty(client: FlaskClient) -> None:
    result = client.get("/orders/")
    assert result.json == {
        "data": {"data": [], "links": {"self": "/orders/"}},
        "errors": {},
    }


def test_create_order(client: FlaskClient) -> None:
    result = client.post("/orders/")
    assert result.json.get("data").get("data").get("attributes").get("status") == "CART"


def test_add_item_to_order(client: FlaskClient) -> None:
    item_id = client.get("/items/").json["data"]["data"][0]["id"]
    order_id = client.post("/orders/").json["data"]["data"]["id"]
    result = client.post(f"/orders/{order_id}/items/", json={"id": item_id}).json

    assert len(result["data"]["data"]) == 1
    assert result["data"]["data"][0]["id"] == item_id


def test_get_items_from_order(client: FlaskClient) -> None:
    item_id = client.get("/items/").json["data"]["data"][0]["id"]
    order_id = client.post("/orders/").json["data"]["data"]["id"]
    client.post(f"/orders/{order_id}/items/", json={"id": item_id}).json

    result = client.get(f"/orders/{order_id}/items/").json

    assert len(result["data"]["data"]) == 1
    assert result["data"]["data"][0]["id"] == item_id


def test_get_orders(client: FlaskClient) -> None:
    order_id_one = client.post("/orders/").json["data"]["data"]["id"]
    order_id_two = client.post("/orders/").json["data"]["data"]["id"]

    result = client.get(f"/orders/").json

    assert len(result["data"]["data"]) == 2
    order_ids = [o["id"] for o in result["data"]["data"]]
    assert order_id_one in order_ids
    assert order_id_two in order_ids
