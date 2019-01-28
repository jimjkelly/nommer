import click
import requests
from termcolor import colored
from .utils import get_data, get_objects


def cmd(url):
    """
    Main command for interacting with our orders menu
    """
    orders = get_objects(get_data(requests.get(f"{url}/orders/")))

    if orders:
        for order in orders:
            items = get_objects(get_data(requests.get(f"{url}/orders/{order['id']}/items/")))
            click.echo(colored(f"{len(items)} items - {sum(i['price'] for i in items)}: status: {order['status']}", "blue"))
    else:
        click.echo(colored("No orders placed, get nomming!", "green"))