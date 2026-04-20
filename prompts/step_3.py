import json
from typing import Any

from schemas.step_3 import Invoice


PROMPT: str = (
    "Extract the invoice information from this image.\n"
    "-Seller and Client information are on top.\n"
    "-Items information are in the middle.\n"
    "-The invoice summary is at the bottom.\n"
    "-Do not wrap the JSON in markdown.\n"
    "-Do not add explanations.\n"
    "-Preserve strings exactly when possible.\n"
    "-Use null for missing values.\n"
    "-Do not return the base schema in your response\n"
    "-Return only valid JSON matching the schema below.\n"
    "-Use the thinking field as a scratchpad to check your answer based on the JSON schema\n"
    f"Schema: {json.dumps(Invoice.model_json_schema(), indent=2)}"
)

RESPONSE_FORMAT: dict[str, Any] = {
    "type": "json_schema",
    "json_schema": {
        "name": "invoice",
        "strict": True,
        "schema": Invoice.model_json_schema(),
    },
}
