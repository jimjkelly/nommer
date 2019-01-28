from typing import Any
from uuid import UUID
from flask import jsonify, Response
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import BadRequest


class UUIDConverter(BaseConverter):
    def to_python(self, value: str) -> UUID:
        try:
            return UUID(value)
        except ValueError:
            raise BadRequest("Invalid ID")

    def to_url(self, value: UUID) -> str:
        return str(value)


def api_jsonify(*args: Any, **kwargs: Any) -> Response:
    """
    Ensures that the Content-Type is set to the JSON-API
    standard value
    """
    response = jsonify(*args, **kwargs)
    response.mimetype = "application/vnd.api+json"
    return response
