from sqlalchemy import Column, Integer, String
from app.database.database import Base
from sqlalchemy.orm import relationship

class CustomerDAO(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    loyalty_card = relationship(
        "LoyaltyCardDAO",   
        back_populates="customer",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin"
    )
