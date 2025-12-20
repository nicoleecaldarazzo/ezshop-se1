from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OrderCreateDTO(BaseModel):
    """DTO per POST /orders - Issue a new order"""
    product_barcode: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    price_per_unit: float = Field(..., gt=0)
    # Status is optional but IGNORED - always set to ISSUED by backend
    status: Optional[str] = Field(default=None, exclude=True)

class OrderPayForDTO(BaseModel):
    """DTO per POST /orders/payfor - Create and pay an order for a product"""
    product_barcode: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    # Status is optional but IGNORED - always set to PAID by backend
    status: Optional[str] = Field(default=None, exclude=True)

class OrderResponseDTO(BaseModel):
    """DTO per le risposte API"""
    id: int
    product_barcode: str
    quantity: int
    price_per_unit: float
    status: str
    issue_date: datetime

class OrderListResponseDTO(BaseModel):
    """DTO per GET /orders - List all orders"""
    orders: list[OrderResponseDTO]

class OrderPaymentDTO(BaseModel):
    """DTO per PATCH /orders/{order_id}/pay - Pay for an existing issued order"""
    # Tipicamente vuoto, o potresti aggiungere info sul pagamento
    pass
    
class OrderArrivalDTO(BaseModel):
    """DTO per PATCH /orders/{order_id}/arrival - Record the arrival of an order"""
    # Tipicamente vuoto, il server registra l'arrivo automaticamente
    pass