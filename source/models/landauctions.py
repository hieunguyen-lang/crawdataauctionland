from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from db import Base

class LandAuctions(Base):
    __tablename__ = "LandAuctions"

    LandAuctionID = Column(Integer, primary_key=True, autoincrement=True)
    DistrictID = Column(Integer, ForeignKey("Districts.DistrictID"), nullable=True)
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=True)
    LandAuctionCategoryID = Column(Integer, ForeignKey("LandAuctionCategories.LandAuctionCategoryID"), nullable=True)
    Title = Column(String(1000), nullable=False)
    Description = Column(String(1000), nullable=True)
    OpenPrice = Column(Float, nullable=False)
    DepositPrice = Column(String(50), nullable=True)
    RegistrationStartTime = Column(DateTime, nullable=True)
    RegistrationEndTime = Column(DateTime, nullable=True)
    DepositPaymentStartTime = Column(DateTime, nullable=True)
    DepositPaymentEndTime = Column(DateTime, nullable=True)
    AuctionAddress = Column(String(1000), unique=True, nullable=True)
    Latitude = Column(Float, nullable=True)
    Longitude = Column(Float, nullable=True)
    CreateAt = Column(DateTime, nullable = True)
    AuctionUrl = Column(String(1000), unique=True, nullable=True)
    NamePropertyOwner = Column(String(1000), nullable=True)
    NameProperty = Column(String(1000), nullable=True)
    AddressProperty = Column(String(1000), nullable=True)
    AddressPropertyOwner = Column(String(1000), nullable=True)
    NameAuctionHouse = Column(String(1000), nullable=True)
    AddressAuctionHouse = Column(String(1000), nullable=True)
    PhoneNumberAuctionHouse = Column(String(20), nullable=True)
    EventSchedule = Column(DateTime, nullable=True)
