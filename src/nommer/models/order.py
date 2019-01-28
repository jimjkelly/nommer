import uuid
from enum import Enum
from peewee import ManyToManyField
from playhouse.postgres_ext import UUIDField
from peewee_extra_fields import EnumField
from . import BaseModel
from .item import Item


class OrderStatus(Enum):
    CART = 0
    OPEN = 1
    CANCELLED = 2
    COMPLETED = 3


class FixedEnumField(EnumField):
    """
    Fix a bug in the upstream EnumField
    """

    def get_enum(self) -> OrderStatus:
        return self.enum


class Order(BaseModel):
    id = UUIDField(default=uuid.uuid4, primary_key=True)
    items = ManyToManyField(Item, backref="orders")
    status = FixedEnumField(OrderStatus, default=OrderStatus.CART)
