import typing
import operator
import functools
from uuid import UUID
from flask import Blueprint, request, Response, current_app
from playhouse.flask_utils import get_object_or_404
from ..schemas.order import OrderSchema
from ..schemas.item import ItemSchema
from ..models.order import Order, OrderStatus
from ..models.item import Item
from ..utils import api_jsonify

orders_app = Blueprint("orders", __name__)


@orders_app.route("/", methods=["GET"])
def orders_all() -> Response:
    schema = OrderSchema()

    query = Order.select()

    if request.args:
        query = query.where(
            functools.reduce(
                operator.or_,
                [
                    getattr(Order, k) == getattr(OrderStatus, v)
                    for k, v in request.args.items()
                ],
            )
        )

    return api_jsonify(schema.dump(query, many=True))


@orders_app.route("/<uuid:order_id>", methods=["GET"])
def orders_get(order_id: typing.Optional[UUID] = None) -> Response:
    schema = OrderSchema()

    if order_id:
        return api_jsonify(schema.dump(get_object_or_404(Order, id=order_id)))
    elif request.args:
        return api_jsonify(schema.dump(get_object_or_404(Order, **request.args)))


@orders_app.route("/", methods=["POST"])
def orders_create() -> Response:
    schema = OrderSchema()

    order = Order().create()

    return api_jsonify(schema.dump(order))


@orders_app.route("/<uuid:order_id>/items/", methods=["GET", "POST"])
def orders_items(order_id: UUID) -> Response:
    schema = ItemSchema()

    if request.method == "GET":
        order = get_object_or_404(Order, Order.id == order_id)
    elif request.method == "POST":
        input_data = request.get_json() or {}
        order = get_object_or_404(Order, Order.id == order_id)
        item = get_object_or_404(Item, Item.id == input_data.get("id"))
        order.items.add(item)

    return api_jsonify(schema.dump(order.items, many=True))


@orders_app.route("/<uuid:order_id>/status/", methods=["PUT"])
def orders_status(order_id: UUID) -> Response:
    input_data = request.get_json() or ""
    current_app.logger.info(f"afdsfsfs: {input_data}")
    if input_data:
        order = get_object_or_404(Order, Order.id == order_id)
        order.status = getattr(OrderStatus, input_data)
        order.save()

    return api_jsonify({}), 204
