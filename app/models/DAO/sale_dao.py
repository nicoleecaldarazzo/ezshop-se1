from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base
from app.models.sale_status import SaleStatus

class SaleDAO(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default=SaleStatus.OPEN)
    discount_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    lines = relationship(
        "SaleLineDAO",
        back_populates="sale",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
