from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Address(BaseModel):
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
    number: str
    issue_date: str = Field(
        ...,
        pattern=r"^(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    )
    seller: Seller
    client: Client
    items: list[Item]
    summary: Summary
