from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.return_status import ReturnStatus
from datetime import datetime, timezone

class ReturnDAO(Base):
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, nullable=False)
    status = Column(Enum(ReturnStatus), default=ReturnStatus.OPEN, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    closed_at = Column(DateTime, nullable=True)

    lines = relationship("ReturnLineDAO", back_populates="return_transaction", cascade="all, delete-orphan", lazy="selectin")

class ReturnLineDAO(Base):
    __tablename__ = "return_lines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    return_id = Column(Integer, ForeignKey("returns.id"), nullable=False)
    product_barcode = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)

    return_transaction = relationship("ReturnDAO", back_populates="lines")