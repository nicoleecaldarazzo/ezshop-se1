from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OrderCreateDTO(BaseModel):

    product_barcode: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    price_per_unit: float = Field(..., gt=0)

    status: Optional[str] = Field(default=None, exclude=True)

class OrderPayForDTO(BaseModel):

    product_barcode: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)

    status: Optional[str] = Field(default=None, exclude=True)

class OrderResponseDTO(BaseModel):

    id: int
    product_barcode: str
    quantity: int
    price_per_unit: float
    status: str
    issue_date: datetime

class OrderListResponseDTO(BaseModel):

    orders: list[OrderResponseDTO]

class OrderPaymentDTO(BaseModel):

    pass
    
class OrderArrivalDTO(BaseModel):

    pass