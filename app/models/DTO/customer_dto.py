from pydantic import BaseModel, Field, model_validator
from typing import Optional

CARD_ID_REGEX = r"^\d{10}$"

class LoyaltyCardDTO(BaseModel):
    card_id: str = Field(..., pattern=CARD_ID_REGEX)  
    points: int = Field(0, ge=0)

class LoyaltyCardUpdateDTO(BaseModel):
    card_id: Optional[str] = Field(default=None, pattern=CARD_ID_REGEX)
    points: Optional[int] = Field(default=None, ge=0)
    
class CustomerCreateDTO(BaseModel):
    name: str = Field(..., min_length=3)
    card: Optional[LoyaltyCardDTO] = None

class CustomerUpdateDTO(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    card: Optional[LoyaltyCardUpdateDTO] = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.name is None and self.card is None:
            raise ValueError("At least one field must be provided")
        return self

class CustomerResponseDTO(BaseModel):
    id: int = Field(..., gt=0)
    name: str 
    card: Optional[LoyaltyCardDTO] = None

class LoyaltyCardCreateDTO(BaseModel):
    card_id: str = Field(..., pattern=CARD_ID_REGEX)
    points: int = Field(0, ge=0)


class LoyaltyCardPointsUpdateDTO(BaseModel):
    points: int = Field(..., ge=0)
