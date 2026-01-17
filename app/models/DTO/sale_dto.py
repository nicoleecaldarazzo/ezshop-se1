from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.models.sale_status import SaleStatus
from app.models.DTO.sale_line_dto import SaleLineDTO

class SaleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    lines: List[SaleLineDTO] = [] 
    status: SaleStatus
    datetime: Optional[datetime] = None