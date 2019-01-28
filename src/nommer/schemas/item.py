from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class ItemSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    price = fields.Decimal(places=2)

    class Meta:
        type_ = "items"
        self_view = "items.items"
        self_view_kwargs = {"item_id": "<id>"}
        self_view_many = "items.items"
        strict = True
