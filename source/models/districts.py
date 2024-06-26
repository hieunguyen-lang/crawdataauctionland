from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from db import Base


class Districts(Base):
    __tablename__ = 'Districts'
    DistrictID = Column(Integer, primary_key=True, autoincrement=True)
    ProvinceID = Column(Integer, ForeignKey('Provinces.ProvinceID'))
    DistrictName = Column(String(50), unique=True, nullable=False)