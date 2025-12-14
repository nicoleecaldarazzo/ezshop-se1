from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.return_status import ReturnStatus

class ReturnLineDTO(BaseModel):
    id: Optional[int] = None
    product_barcode: str
    quantity: int
    price_per_unit: float

class ReturnDTO(BaseModel):
    id: int
    sale_id: int
    status: ReturnStatus
    lines: List[ReturnLineDTO] = []
    created_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None