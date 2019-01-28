import os
import typing
from flask import Flask


def create_app(config: typing.Optional[typing.Dict[str, str]] = None) -> Flask:
    """
    Create a fully configured instance of our application.
    """
    app = Flask(__name__)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        # store the database in the instance folder
        DATABASE_URL=os.getenv("DATABASE_URL"),
    )

    if config:
        app.config.update(**config)

    from nommer.utils import UUIDConverter

    app.url_map.converters["uuid"] = UUIDConverter

    # Initialize Database
    from nommer.db import init_app

    init_app(app)

    # Add Blueprints
    from nommer.controllers import orders, items

    app.register_blueprint(orders.orders_app, url_prefix="/orders")
    app.register_blueprint(items.items_app, url_prefix="/items")

    return app
