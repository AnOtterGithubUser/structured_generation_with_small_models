from typing import Optional

from pydantic import BaseModel, Field, model_validator


def are_amounts_equal(expected: float, actual: float):
    return abs(expected - actual) <= 0.01  # due to rounding, values may differ up to $0.01


class Address(BaseModel):
    thinking: Optional[str] = Field(description="Use this field as a scratchpad to think about your answer regarding the address")
    street_number: str
    street_name: str = Field(description="This should be only the name of the street without anything else")
    address_line_2: Optional[str] = Field(description="This field should include info about the unit number including unit type like Apt, Suite or Unit. Leave blank if not provided")
    city: str
    state: str
    zip_code: str

class Seller(BaseModel):
    name: str
    address: Address
    tax_id: str
    iban: str


class Client(BaseModel):
    name: str
    address: Address
    tax_id: str


class Item(BaseModel):
    number: int
    description: str
    quantity: str = Field(..., pattern=r"^\d+,\d{2}$")
    unit_of_measure: str
    net_price: str = Field(..., pattern=r"^\d+,\d{2}$")
    net_worth: str = Field(..., pattern=r"^\d+,\d{2}$")
    vat_percentage: float
    gross_worth: str = Field(..., pattern=r"^\d+,\d{2}$")

    @model_validator(mode="after")
    def validate_net_worth(self) -> "Item":
        net_price = float(self.net_price.replace(",", "."))
        quantity = float(self.quantity.replace(",", "."))
        actual_net_worth = float(self.net_worth.replace(",", "."))
        expected_net_worth = net_price * quantity
        if not are_amounts_equal(expected_net_worth, actual_net_worth):  
            raise ValueError("Net worth should be net price multiplied by quantity")
        return self
        
    @model_validator(mode="after")
    def validate_gross_worth(self) -> "Item":
        net_worth = float(self.net_worth.replace(",", "."))
        actual_gross_worth = float(self.gross_worth.replace(",", "."))
        expected_gross_worth = net_worth * (1 + 0.01 * self.vat_percentage)
        if not are_amounts_equal(expected_gross_worth, actual_gross_worth):
            raise ValueError("Gross worth should be net worth with additional VAT")
        return self

class Summary(BaseModel):
    vat_percentage: float
    net_worth: str = Field(..., pattern=r"^\d+,\d{2}$")
    vat_amount: str = Field(..., pattern=r"^\d+,\d{2}$")
    gross_worth: str = Field(..., pattern=r"^\d+,\d{2}$")

class Invoice(BaseModel):
    thinking: Optional[str] = Field(description="Use this field as a scratchpad to check your understanding and fix your answer if needed")
    number: str
    issue_date: str = Field(
        ...,
        pattern=r"^(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    )
    seller: Seller
    client: Client
    items: list[Item]
    summary: Summary

    @model_validator(mode="after")
    def validate_summary_net_worth(self) -> "Invoice":
        expected_summary_net_worth = sum(float(item.net_worth.replace(",", ".")) for item in self.items)
        actual_summary_net_worth = float(self.summary.net_worth.replace(",", "."))
        if not are_amounts_equal(expected_summary_net_worth, actual_summary_net_worth):
            raise ValueError("Summary net worth should be the sum of items net worth")
        return self
    
    @model_validator(mode="after")
    def validate_summary_vat_amount(self) -> "Invoice":
        expected_summary_vat_amount = float(self.summary.net_worth.replace(",", ".")) * (0.01 * self.summary.vat_percentage)
        actual_summary_vat_amount = float(self.summary.vat_amount.replace(",", "."))
        if not are_amounts_equal(expected_summary_vat_amount, actual_summary_vat_amount):
            raise ValueError("VAT amount should be VAT percentage applied to net worth")
        return self
    
    @model_validator(mode="after")
    def validate_summary_gross_worth(self) -> "Invoice":
        expected_summary_gross_worth = float(self.summary.net_worth.replace(",", ".")) + float(self.summary.vat_amount.replace(",", "."))
        actual_summary_gross_worth = float(self.summary.gross_worth.replace(",", "."))
        if not are_amounts_equal(expected_summary_gross_worth, actual_summary_gross_worth):
            raise ValueError("Gross worth should be net worth plus VAT amount")
        return self
