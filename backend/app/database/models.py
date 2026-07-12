from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    surface = Column(Float, nullable=False)
    rooms = Column(Integer)
    bedrooms = Column(Integer)
    city = Column(String(100))
    postal_code = Column(String(20))
    has_garage = Column(Boolean, default=False)
    has_balcony = Column(Boolean, default=False)
    has_garden = Column(Boolean, default=False)
    construction_year = Column(Integer)
    property_condition = Column(String(50))
    real_price = Column(Float)
    source = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())


class HomePrediction(Base):
    __tablename__ = "home_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    surface = Column(Float, nullable=False)
    rooms = Column(Integer)
    bedrooms = Column(Integer)
    city = Column(String(100))
    postal_code = Column(String(20))
    has_garage = Column(Boolean, default=False)
    has_balcony = Column(Boolean, default=False)
    has_garden = Column(Boolean, default=False)
    construction_year = Column(Integer)
    predicted_price = Column(Float)
    confidence_score = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))
    created_at = Column(DateTime, server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    language = Column(String(20), nullable=False, default="en")
    app_version = Column(String(30), nullable=True)
    platform = Column(String(30), nullable=False, default="android")
    current_screen = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
