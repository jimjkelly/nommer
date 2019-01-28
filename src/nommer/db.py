import click
from flask import Flask
from flask.cli import with_appcontext
from playhouse.flask_utils import FlaskDB


database = FlaskDB()


def init_db() -> None:
    """
    Clear existing data and create new tables.
    """
    from nommer.models.item import Item, seed as seed_items
    from nommer.models.order import Order

    database.database.create_tables(
        [Item, Order, Order.items.get_through_model()], safe=True
    )
    seed_items()

    if not database.database.is_closed():
        database.database.close()


def drop_db() -> None:
    """
    Drop all tables from the database.
    """
    from nommer.models.item import Item
    from nommer.models.order import Order

    database.database.drop_tables(
        [Item, Order, Order.items.get_through_model()], safe=True
    )


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """
    Clear existing data and create new tables.
    """
    init_db()
    click.echo("Initialized the database.")


@click.command("drop-db")
@with_appcontext
def drop_db_command() -> None:
    """
    Drop all data
    """
    drop_db()
    click.echo("Dropped the database.")


def init_app(app: Flask) -> None:
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    database.init_app(app)
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
