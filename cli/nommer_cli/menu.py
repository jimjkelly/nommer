import typing
import click
import requests
from termcolor import colored
from PyInquirer import prompt
from .utils import get_objects, get_object, get_data


def cmd(url: str) -> None:
    """
    Main command for interacting with our items menu
    """
    # Get our menu items
    data = get_data(requests.get(f"{url}/items/"))

    if data:
        list(get_objects(data), url)


def list(items: typing.List[dict], url) -> None:
    answer = prompt(
        {
            "type": "list",
            "name": "menu",
            "message": "Select a Menu Item:",
            "choices": [*[item["name"] for item in items], "Return to Previous Menu"],
        }
    )

    item = next((i for i in items if i["name"] == answer["menu"]), None)

    if item:
        selected_item(item, url)


def selected_item(item: typing.Dict[str, str], url) -> None:
    click.echo(colored(f"Description: {item.get('description')}", "blue"))
    click.echo(colored(f"Price: {item.get('price')}", "blue"))

    answer = prompt({"type": "confirm", "name": "add", "message": "Add to order?"})

    if answer["add"]:
        data = get_data(requests.get(f"{url}/orders/?status=CART"))

        if not data:
            cart_id = get_object(get_data(requests.post(f"{url}/orders/")))["id"]
        else:
            cart_id = get_objects(data)[0]["id"]
        
        requests.post(f"{url}/orders/{cart_id}/items/", json={"id": item["id"]})
