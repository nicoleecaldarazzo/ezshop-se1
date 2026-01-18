from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.models.sale_status import SaleStatus
from app.models.DTO.sale_line_dto import SaleLineDTO

class SaleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: SaleStatus
    # FIX: Ensure this is named 'lines', not 'items'
    lines: List[SaleLineDTO] = [] 
    discount_rate: float = 0.0
    closed_at: Optional[datetime] = None