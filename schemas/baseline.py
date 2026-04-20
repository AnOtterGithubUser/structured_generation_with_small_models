from datetime import date
from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    street_number: str
    street_name: str
    address_line_2: Optional[str] = None
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
    quantity: float
    unit_of_measure: str
    net_price: float
    net_worth: float
    vat_percentage: float
    gross_worth: float

class Summary(BaseModel):
    vat_percentage: float
    net_worth: float
    vat_amount: float
    gross_worth: float


class Invoice(BaseModel):
    number: str
    issue_date: date
    seller: Seller
    client: Client
    items: list[Item]
    summary: Summary
