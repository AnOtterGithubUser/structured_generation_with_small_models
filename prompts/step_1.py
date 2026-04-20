import json
from typing import Any

from schemas.baseline import Invoice


RESPONSE_FORMAT: dict[str, Any] = {
    "type": "json_schema",
    "json_schema": {
        "name": "invoice",
        "strict": True,
        "schema": Invoice.model_json_schema(),
    },
}
