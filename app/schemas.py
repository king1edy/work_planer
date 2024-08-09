# app/schemas.py

from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from app.models import ShiftTime


class WorkerBase(BaseModel):
    name: str
    email: str
    phone: str


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(WorkerBase):
    pass


class Worker(WorkerBase):
    id: int
    # Add new Config with from_attributes instead of orm_mode
    model_config = ConfigDict(from_attributes=True)


class ShiftBase(BaseModel):
    worker_id: int
    date: date
    shift_time: ShiftTime


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(BaseModel):
    worker_id: Optional[int] = None
    date: Optional[date] = None
    shift_time: Optional[ShiftTime] = None


class Shift(ShiftBase):
    id: int

    # Add new Config with from_attributes instead of orm_mode
    model_config = ConfigDict(from_attributes=True)
