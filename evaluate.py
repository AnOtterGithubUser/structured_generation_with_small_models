from abc import ABC
from typing import Any, Generic, Mapping, TypeVar
from pathlib import Path
import json
from pydantic import BaseModel

from schemas.step_2 import Invoice as Invoice_step_2
from schemas.step_3 import Invoice as Invoice_step_3
from schemas.step_4 import Invoice as Invoice_step_4


T = TypeVar("T", bound=BaseModel)


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


def _add_empty_thinking_fields(invoice_data: dict[str, Any]) -> dict[str, Any]:
    invoice_data["thinking"] = None
    invoice_data["seller"]["address"]["thinking"] = None
    invoice_data["client"]["address"]["thinking"] = None
    return invoice_data


def _clear_thinking_fields(invoice: T) -> T:
    invoice = invoice.model_copy(deep=True)
    invoice.thinking = None
    invoice.seller.address.thinking = None
    invoice.client.address.thinking = None
    return invoice


class InvoiceEvaluator(ABC, Generic[T]):
    invoice_model: type[T]
    print_report = False
    raise_on_failure = True

    def evaluate(self, invoices: Mapping[str | Path, T]) -> None:
        if self.print_report:
            print("-" * 20)
            print("EVALUATION")

        for img_path, predicted_invoice in invoices.items():
            img_path = Path(img_path)

            if self.print_report:
                print(f"IMG_PATH: {img_path}")

            expected_invoice = self.load_expected_invoice(img_path)
            predicted_invoice = self.normalize_predicted_invoice(predicted_invoice)

            try:
                _assert_invoice_matches(expected_invoice, predicted_invoice, img_path)
                self.on_success()
            except AssertionError as e:
                self.on_failure(e)

    def load_expected_invoice(self, img_path: Path) -> T:
        gt_json_path = img_path.with_suffix(".json")
        gt = gt_json_path.read_text(encoding="utf-8")
        gt_json = self.normalize_expected_json(json.loads(gt))
        return self.invoice_model.model_validate_json(json.dumps(gt_json))

    def normalize_expected_json(self, invoice_data: dict[str, Any]) -> dict[str, Any]:
        return invoice_data

    def normalize_predicted_invoice(self, invoice: T) -> T:
        return invoice

    def on_success(self) -> None:
        if self.print_report:
            print("Evaluation succeeded!")

    def on_failure(self, error: AssertionError) -> None:
        if self.print_report:
            print("Evaluation failed!")

        if self.raise_on_failure:
            raise error


class ThinkingAgnosticInvoiceEvaluator(InvoiceEvaluator[T]):
    def normalize_expected_json(self, invoice_data: dict[str, Any]) -> dict[str, Any]:
        return _add_empty_thinking_fields(invoice_data)

    def normalize_predicted_invoice(self, invoice: T) -> T:
        return _clear_thinking_fields(invoice)


class Step2Evaluator(InvoiceEvaluator[Invoice_step_2]):
    invoice_model = Invoice_step_2


class Step3Evaluator(ThinkingAgnosticInvoiceEvaluator[Invoice_step_3]):
    invoice_model = Invoice_step_3


class Step4Evaluator(ThinkingAgnosticInvoiceEvaluator[Invoice_step_4]):
    invoice_model = Invoice_step_4
    print_report = True
    raise_on_failure = False


class Step5Evaluator(Step4Evaluator):
    pass


def evaluate_step_2(invoices: Mapping[str | Path, Invoice_step_2]) -> None:
    Step2Evaluator().evaluate(invoices)


def evaluate_step_3(invoices: Mapping[str | Path, Invoice_step_3]) -> None:
    Step3Evaluator().evaluate(invoices)


def evaluate_step_4(invoices: Mapping[str | Path, Invoice_step_4]) -> None:
    Step4Evaluator().evaluate(invoices)


def evaluate_step_5(invoices: Mapping[str | Path, Invoice_step_4]) -> None:
    Step5Evaluator().evaluate(invoices)
