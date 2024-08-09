# app/api/shifts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import crud, schemas, services
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Shift])
async def read_shifts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_shifts(db, skip=skip, limit=limit)


@router.get("/{shift_id}", response_model=schemas.Shift)
async def read_shift(shift_id: int, db: AsyncSession = Depends(get_db)):
    db_shift = await crud.get_shift(db, shift_id)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_shift


@router.post("/", response_model=schemas.Shift)
async def create_shift(shift: schemas.ShiftCreate, db: AsyncSession = Depends(get_db)):
    return await services.create_shift_service(db, shift)


@router.put("/{shift_id}", response_model=schemas.Shift)
async def update_shift(shift_id: int, shift: schemas.ShiftUpdate, db: AsyncSession = Depends(get_db)):
    return await services.update_shift_service(db, shift_id, shift)


@router.delete("/{shift_id}", response_model=schemas.Shift)
async def delete_shift(shift_id: int, db: AsyncSession = Depends(get_db)):
    return await services.delete_shift_service(db, shift_id)
