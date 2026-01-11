from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.database import Base
from datetime import datetime, timezone

class OrderDAO(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    product_barcode = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="ISSUED")
    issue_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))