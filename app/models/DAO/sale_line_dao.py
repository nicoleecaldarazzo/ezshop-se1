from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class SaleLineDAO(Base):
    __tablename__ = "sale_lines"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_barcode = Column(String)
    quantity = Column(Integer)
    price_per_unit = Column(Float, default=0.0)
    discount_rate = Column(Float, default=0.0)

    sale = relationship("SaleDAO", back_populates="lines")
