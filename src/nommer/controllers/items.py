import typing
from uuid import UUID
from flask import Blueprint, Response
from ..schemas.item import ItemSchema
from ..models.item import Item
from ..utils import api_jsonify

items_app = Blueprint("items", __name__)


@items_app.route("/", methods=["GET"])
@items_app.route("/<uuid:uuid>", methods=["GET"])
def items(uuid: typing.Optional[UUID] = None) -> Response:
    schema = ItemSchema()

    if uuid:
        return api_jsonify(schema.dump(Item.get(id=uuid)))
    else:
        return api_jsonify(schema.dump(Item.select(), many=True))
