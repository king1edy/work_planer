# app/services.py

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import date
from app import crud, models, schemas

# Worker services
async def create_worker_service(db: AsyncSession, worker: schemas.WorkerCreate):
    return await crud.create_worker(db, worker)

async def update_worker_service(db: AsyncSession, worker_id: int, worker: schemas.WorkerUpdate):
    db_worker = await crud.get_worker(db, worker_id)
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return await crud.update_worker(db, worker_id, worker)

async def delete_worker_service(db: AsyncSession, worker_id: int):
    db_worker = await crud.get_worker(db, worker_id)
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return await crud.delete_worker(db, worker_id)

# Shift services
async def create_shift_service(db: AsyncSession, shift: schemas.ShiftCreate):
    db_worker = await crud.get_worker(db, shift.worker_id)
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    if not await crud.is_worker_available(db, shift.worker_id, shift.date, shift.shift_time):
        raise HTTPException(status_code=400, detail="Worker is not available for the shift")

    db_shift = await crud.create_shift(db, shift)
    if not db_shift:
        raise HTTPException(status_code=400, detail="Worker already has a shift at this time")
    return db_shift

async def update_shift_service(db: AsyncSession, shift_id: int, shift: schemas.ShiftUpdate):
    db_shift = await crud.get_shift(db, shift_id)
    if not db_shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    if shift.worker_id and not await crud.get_worker(db, shift.worker_id):
        raise HTTPException(status_code=404, detail="Worker not found")

    if shift.worker_id and shift.date and shift.shift_time:
        if not await crud.is_worker_available(db, shift.worker_id, shift.date, shift.shift_time):
            raise HTTPException(status_code=400, detail="Worker is not available for the shift")

    return await crud.update_shift(db, shift_id, shift)

async def delete_shift_service(db: AsyncSession, shift_id: int):
    db_shift = await crud.get_shift(db, shift_id)
    if not db_shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return await crud.delete_shift(db, shift_id)
