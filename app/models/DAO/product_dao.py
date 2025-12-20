from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class ProductDAO(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    barcode = Column(String, nullable=False, unique=True)
    price_per_unit = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    position = Column(String, nullable=True) 