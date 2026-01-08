from pydantic import BaseModel, Field
from typing import Optional

BARCODE_REGEX = r"^\d{12,14}$"  

class ProductCreateDTO(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    barcode: str = Field(..., pattern=BARCODE_REGEX)
    price_per_unit: float = Field(..., gt=0)
    note: Optional[str] = Field(default=None, max_length=500)
    quantity: int = Field(0, ge=0)
    position: Optional[str] = Field(default=None, max_length=50)

class ProductUpdateDTO(BaseModel):
    description: Optional[str] = Field(default=None, min_length=1, max_length=255)
    barcode: Optional[str] = Field(default=None, pattern=BARCODE_REGEX)
    price_per_unit: Optional[float] = Field(default=None, gt=0)
    note: Optional[str] = Field(default=None, max_length=500)
    quantity: Optional[int] = Field(default=None, ge=0)
    position: Optional[str] = Field(default=None, max_length=50)

class ProductResponseDTO(BaseModel):
    id: int
    description: str
    barcode: str
    price_per_unit: float
    note: Optional[str] = None
    quantity: int
    position: Optional[str] = None

class ProductPositionUpdateDTO(BaseModel):

    position: Optional[str] = Field(default=None, max_length=50)  

class ProductSearchDTO(BaseModel):

    description: str = Field(..., min_length=1)