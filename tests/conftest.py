import typing
import pytest
from flask.testing import FlaskClient
from nommer import create_app, db


@pytest.fixture
def client() -> typing.Iterator[FlaskClient]:
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    db.init_db()

    yield client

    db.drop_db()
