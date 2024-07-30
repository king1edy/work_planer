# app/schemas.py

from datetime import date
from pydantic import BaseModel
from typing import Optional
from app.models import ShiftTime

class WorkerBase(BaseModel):
    name: str

class WorkerCreate(WorkerBase):
    pass

class WorkerUpdate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int

    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True
