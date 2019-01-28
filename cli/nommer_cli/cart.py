import click
import requests
from termcolor import colored
from .utils import get_data, get_objects


def cmd(url):
    """
    Main command for interacting with our items menu
    """
    orders = get_objects(get_data(requests.get(f"{url}/orders/?status=CART")))
    cart_id = orders[0].get("id") if len(orders) else None

    if cart_id:
        items = get_objects(get_data(requests.get(f"{url}/orders/{cart_id}/items/")))
        click.echo(colored("Your cart contains the following items:", "green"))
        for item in items:
            click.echo(colored(f"{item['name']} - {item['price']}", "blue"))
        click.echo(colored(f"Total: {sum([i['price'] for i in items])}", "green"))
    else:
        click.echo(colored("Nothing in your cart!", "green"))