from marshmallow_enum import EnumField
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema
from ..models.order import OrderStatus


class OrderSchema(Schema):
    id = fields.UUID(dump_only=True)
    items = Relationship(
        related_view="orders.orders_items",
        related_view_kwargs={"order_id": "<id>"},
        many=True,
        include_resource_linkage=True,
        type_="items",
    )
    status = EnumField(OrderStatus)

    class Meta:
        type_ = "orders"
        self_view = "orders.orders_get"
        self_view_kwargs = {"order_id": "<id>"}
        self_view_many = "orders.orders_all"
        strict = True
