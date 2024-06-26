from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Date, Time, SmallInteger, Boolean, LargeBinary
from db import Base

class Users(Base):
    __tablename__ = "Users"
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(50), nullable=False)
    Username = Column(String(50), unique=True, nullable=True)
    Password = Column(String(255), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Phone = Column(String(20))
    Gender = Column(Enum("Nam", "Nữ", "Đồng tính nữ", "Đồng tính nam"))
    BirthDate = Column(Date)
    BirthTime = Column(Time)
    ProvinceID = Column(Integer, ForeignKey("Provinces.ProvinceID"))
    IsAnonymous = Column(SmallInteger, nullable=True)
    RegistrationIP = Column(String(45))
    LastLoginIP = Column(String(45))
    LastActivityTime = Column(DateTime)
    IsLoggedIn = Column(Boolean, default=False)
    Role = Column(Boolean, nullable=False)
    avatarLink = Column(LargeBinary, nullable=True)
    Bio = Column(String(255), nullable=True)
    CurrentAdd = Column(String(255), nullable=True)
    BirthPlace = Column(String(255), nullable=True)
    Confirmed = Column(Boolean, default=False)
    Blocked = Column(Boolean, default=False)
    Create_at = Column(DateTime)