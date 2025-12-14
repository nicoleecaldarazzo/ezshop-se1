from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship

class LoyaltyCardDAO(Base):
    __tablename__ = "loyalty_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(String, nullable=False, unique=True, index=True)
    points = Column(Integer, nullable=False, default=0)

    customer_id = Column(
        Integer, 
        ForeignKey("customers.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=True
    )
    customer = relationship(
        "CustomerDAO", 
        back_populates="loyalty_card",
        lazy="selectin"
    )
