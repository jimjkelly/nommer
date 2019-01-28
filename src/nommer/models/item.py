import uuid
from peewee import CharField, TextField, DecimalField
from playhouse.postgres_ext import UUIDField
from . import BaseModel


class Item(BaseModel):
    """
    A single item available to order
    """

    id = UUIDField(default=uuid.uuid4, primary_key=True)
    name = CharField()
    description = TextField()
    # The values here would normally be agreed upon with the product
    # owner, I'm just providing some sane defaults
    price = DecimalField(max_digits=6, decimal_places=2)


def seed() -> None:
    Item.get_or_create(name="Pizza", description="A delicious pizza.", price=8.99)

    Item.get_or_create(name="Burger", description="A tasty burger.", price=6.44)
