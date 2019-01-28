import click
import requests
from termcolor import colored
from PyInquirer import prompt
from .utils import get_data, get_objects



def cmd(url):
    orders = get_objects(get_data(requests.get(f"{url}/orders/?status=CART")))
    cart_id = orders[0].get("id") if len(orders) else None

    if cart_id:
        items = get_objects(get_data(requests.get(f"{url}/orders/{cart_id}/items/")))

        click.echo(colored(f"Total: {len(items)} items at {sum([i['price'] for i in items])}", "green"))
        answer = prompt({"type": "confirm", "name": "checkout", "message": "Would you like to purchase the items in your cart?"})

        if answer["checkout"]:
            requests.put(f"{url}/orders/{cart_id}/status/", json="OPEN")
    else:
        click.echo(colored("Nothing in your cart!", "green"))
