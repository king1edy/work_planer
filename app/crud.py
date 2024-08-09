# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from datetime import date


# Worker CRUD operations
async def get_worker(db: AsyncSession, worker_id: int):
    result = await db.execute(select(models.Worker).filter(models.Worker.id == worker_id))
    worker = result.scalar_one_or_none()   # Use scalar_one_or_none() for single result
    return worker


async def get_workers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Worker).offset(skip).limit(limit))
    return result.scalars().all()


async def create_worker(db: AsyncSession, worker: schemas.WorkerCreate):
    try:
        db_worker = models.Worker(name=worker.name)
        db.add(db_worker)
        await db.commit()  # Commit the transaction
        await db.refresh(db_worker)  # Refresh instance state from the database
        return db_worker
    except IntegrityError:
        await db.rollback()
        return None


async def update_worker(db: AsyncSession, worker_id: int, worker: schemas.WorkerUpdate):
    db_worker = await get_worker(db, worker_id)
    if db_worker:
        for key, value in worker.dict(exclude_unset=True).items():
            setattr(db_worker, key, value)
        await db.commit()
        await db.refresh(db_worker)
    return db_worker


async def delete_worker(db: AsyncSession, worker_id: int):
    db_worker = await get_worker(db, worker_id)
    if db_worker:
        await db.delete(db_worker)
        await db.commit()
    return db_worker


# Shift CRUD operations
async def get_shift(db: AsyncSession, shift_id: int):
    result = await db.execute(select(models.Shift).filter(models.Shift.id == shift_id))
    shift = result.scalar_one_or_none()  # Use scalar_one_or_none() for single result
    return shift

async def get_shifts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Shift).offset(skip).limit(limit))
    return result.scalars().all()


async def create_shift(db: AsyncSession, shift: schemas.ShiftCreate):
    db_shift = models.Shift(**shift.dict())
    db.add(db_shift)
    try:
        await db.commit()
        await db.refresh(db_shift)
        return db_shift
    except IntegrityError:
        await db.rollback()
        return None


async def get_worker_shifts(db: AsyncSession, worker_id: int, skip: int = 0, limit: int = 10):
    # Using select with offset and limit for pagination
    result = await db.execute(select(models.Shift).where(models.Shift.worker_id == worker_id).offset(skip).limit(limit))
    shifts = result.scalars().all()  # Get all results as a list
    return shifts


async def update_shift(db: AsyncSession, shift_id: int, shift: schemas.ShiftUpdate):
    db_shift = await get_shift(db, shift_id)
    if db_shift:
        for key, value in shift.dict(exclude_unset=True).items():
            setattr(db_shift, key, value)
        await db.commit()
        await db.refresh(db_shift)
    return db_shift

async def delete_shift(db: AsyncSession, shift_id: int):
    db_shift = await get_shift(db, shift_id)
    if db_shift:
        await db.delete(db_shift)
        await db.commit()
    return db_shift

async def is_worker_available(db: AsyncSession, worker_id: int, date: date, shift_time: models.ShiftTime):
    result = await db.execute(
        select(models.Shift)
        .where(
            and_(
                models.Shift.worker_id == worker_id,
                models.Shift.date == date,
                models.Shift.shift_time == shift_time
            )
        )
    )
    return result.scalars().first() is None
