import sys
import click
from colorama import init
from termcolor import colored
from PyInquirer import prompt
from .menu import cmd as menu
from .cart import cmd as cart
from .orders import cmd as orders
from .checkout import cmd as checkout


@click.command()
@click.option("--url", help="URL of server", envvar="NOMMER_URL")
def run(url):
    init()
    click.echo(colored("Welcome to Nommer, your source for tasty noms!", "green"))

    choices = {"View Menu": menu, "View Cart": cart, "View Orders": orders, "Checkout": checkout, "Quit": quit}

    while True:
        answer = prompt(
            [
                {
                    "type": "list",
                    "name": "what",
                    "message": "What'll it be?",
                    "choices": choices.keys(),
                }
            ]
        )

        choices[answer["what"]](url)


def quit(url):
    click.echo("bye!")
    sys.exit(0)
