import json
from schemas.baseline import Invoice

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
    f"Schema: {json.dumps(Invoice.model_json_schema(), indent=2)}"
)
