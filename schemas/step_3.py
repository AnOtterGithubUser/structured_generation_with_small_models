from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


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

class Summary(BaseModel):
    vat_percentage: float
    net_worth: str = Field(..., pattern=r"^\d+,\d{2}$")
    vat_amount: str = Field(..., pattern=r"^\d+,\d{2}$")
    gross_worth: str = Field(..., pattern=r"^\d+,\d{2}$")


class Invoice(BaseModel):
    thinking: Optional[str] = Field(description="Use this field as a scratchpad to check your understanding and fix your answer if needed", exclude=True)
    number: str
    issue_date: str = Field(
        ...,
        pattern=r"^(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    )
    seller: Seller
    client: Client
    items: list[Item]
    summary: Summary
