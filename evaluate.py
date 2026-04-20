from typing import Any, Mapping
from pathlib import Path
import json
from pydantic import BaseModel

from schemas.step_2 import Invoice as Invoice_step_2
from schemas.step_3 import Invoice as Invoice_step_3
from schemas.step_4 import Invoice as Invoice_step_4


def _field_path(parent: str, field: str | int) -> str:
    if isinstance(field, int):
        return f"{parent}[{field}]"

    return f"{parent}.{field}" if parent else field


def _find_mismatches(expected: Any, actual: Any, path: str = "") -> list[str]:
    if isinstance(expected, dict) and isinstance(actual, dict):
        mismatches = []
        keys = expected.keys() | actual.keys()

        for key in sorted(keys):
            current_path = _field_path(path, key)

            if key not in expected:
                mismatches.append(f"{current_path}: unexpected value {actual[key]!r}")
            elif key not in actual:
                mismatches.append(f"{current_path}: expected {expected[key]!r}, got missing")
            else:
                mismatches.extend(_find_mismatches(expected[key], actual[key], current_path))

        return mismatches

    if isinstance(expected, list) and isinstance(actual, list):
        mismatches = []

        if len(expected) != len(actual):
            mismatches.append(f"{path}: expected {len(expected)} item(s), got {len(actual)}")

        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            mismatches.extend(_find_mismatches(expected_item, actual_item, _field_path(path, index)))

        return mismatches

    if expected != actual:
        return [f"{path}: expected {expected!r}, got {actual!r}"]

    return []


def _assert_invoice_matches(expected: BaseModel, actual: BaseModel, img_path: Path) -> None:
    mismatches = _find_mismatches(
        expected.model_dump(mode="json"),
        actual.model_dump(mode="json"),
    )

    assert not mismatches, (
        f"{img_path} has {len(mismatches)} field mismatch(es):\n"
        + "\n".join(f"- {mismatch}" for mismatch in mismatches)
    )


def evaluate_step_2(invoices: Mapping[str | Path, Invoice_step_2]):

    for img_path, predicted_invoice in invoices.items():

        img_path = Path(img_path)
        gt_json_path = img_path.with_suffix(".json")
        gt = gt_json_path.read_text(encoding="utf-8")
        gt_invoice = Invoice_step_2.model_validate_json(gt)

        _assert_invoice_matches(gt_invoice, predicted_invoice, img_path)

def evaluate_step_3(invoices: Mapping[str | Path, Invoice_step_3]):

    for img_path, predicted_invoice in invoices.items():

        img_path = Path(img_path)
        gt_json_path = img_path.with_suffix(".json")
        gt = gt_json_path.read_text(encoding="utf-8")
        gt_json = json.loads(gt)
        gt_json["thinking"] = None
        gt_json["seller"]["address"]["thinking"] = None
        gt_json["client"]["address"]["thinking"] = None
        gt_invoice = Invoice_step_3.model_validate_json(json.dumps(gt_json))

        predicted_invoice.thinking = None
        predicted_invoice.seller.address.thinking = None
        predicted_invoice.client.address.thinking = None

        _assert_invoice_matches(gt_invoice, predicted_invoice, img_path)

def evaluate_step_4(invoices: Mapping[str | Path, Invoice_step_3]):

    print("-"*20)
    print("EVALUATION")

    for img_path, predicted_invoice in invoices.items():

        print(f"IMG_PATH: {img_path}")

        img_path = Path(img_path)
        gt_json_path = img_path.with_suffix(".json")
        gt = gt_json_path.read_text(encoding="utf-8")
        gt_json = json.loads(gt)
        gt_json["thinking"] = None
        gt_json["seller"]["address"]["thinking"] = None
        gt_json["client"]["address"]["thinking"] = None
        gt_invoice = Invoice_step_4.model_validate_json(json.dumps(gt_json))

        predicted_invoice.thinking = None
        predicted_invoice.seller.address.thinking = None
        predicted_invoice.client.address.thinking = None

        try:
            _assert_invoice_matches(gt_invoice, predicted_invoice, img_path)
        except AssertionError:
            print("Evaluation failed!")

        print("Evaluation succeeded!")

def evaluate_step_5(invoices: Mapping[str | Path, Invoice_step_3]):

    print("-"*20)
    print("EVALUATION")

    for img_path, predicted_invoice in invoices.items():

        print(f"IMG_PATH: {img_path}")

        img_path = Path(img_path)
        gt_json_path = img_path.with_suffix(".json")
        gt = gt_json_path.read_text(encoding="utf-8")
        gt_json = json.loads(gt)
        gt_json["thinking"] = None
        gt_json["seller"]["address"]["thinking"] = None
        gt_json["client"]["address"]["thinking"] = None
        gt_invoice = Invoice_step_4.model_validate_json(json.dumps(gt_json))

        predicted_invoice.thinking = None
        predicted_invoice.seller.address.thinking = None
        predicted_invoice.client.address.thinking = None

        try:
            _assert_invoice_matches(gt_invoice, predicted_invoice, img_path)
            print("Evaluation succeeded!")
        except AssertionError:
            print("Evaluation failed!")
