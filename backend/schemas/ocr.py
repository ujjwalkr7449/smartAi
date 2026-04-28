from pydantic import BaseModel


class InvoiceItem(BaseModel):
    name: str
    quantity: int
    unit_price: float


class InvoiceParseResponse(BaseModel):
    supplier: str
    items: list[InvoiceItem]
    total: float
