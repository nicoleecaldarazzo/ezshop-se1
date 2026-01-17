from pydantic import BaseModel, ConfigDict
from typing import Optional

class SaleLineDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_barcode: str
    quantity: int
    price_per_unit: float
    discount_rate: float
