# app/models.py
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class ShiftTime(str, enum.Enum):
    morning = "0-8"
    afternoon = "8-16"
    night = "16-24"

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)

    # Define any relationships if necessary
    shifts = relationship("Shift", back_populates="worker")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    date = Column(Date)
    shift_time = Column(Enum(ShiftTime))

    worker = relationship("Worker", back_populates="shifts")
