from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from db import Base
class LandAuctionCategories(Base):
    __tablename__ = "LandAuctionCategories"
    LandAuctionCategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(50), unique=True, nullable=False)
    Descritption = Column(String(250), unique=True, nullable=True)