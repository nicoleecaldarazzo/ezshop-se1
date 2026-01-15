from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.sale_status import SaleStatus

class SaleDTO(BaseModel):
    id: int
    items: List = []
    status: SaleStatus
    datetime: Optional[datetime] = None
    
    class Config:
        from_attributes = True
