# app/api/workers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import crud, schemas, services
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Worker])
async def read_workers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_workers(db, skip=skip, limit=limit)

@router.get("/{worker_id}", response_model=schemas.Worker)
async def read_worker(worker_id: int, db: AsyncSession = Depends(get_db)):
    db_worker = await crud.get_worker(db, worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker

@router.post("/", response_model=schemas.Worker)
async def create_worker(worker: schemas.WorkerCreate, db: AsyncSession = Depends(get_db)):
    return await services.create_worker_service(db, worker)

@router.put("/{worker_id}", response_model=schemas.Worker)
async def update_worker(worker_id: int, worker: schemas.WorkerUpdate, db: AsyncSession = Depends(get_db)):
    return await services.update_worker_service(db, worker_id, worker)

@router.delete("/{worker_id}", response_model=schemas.Worker)
async def delete_worker(worker_id: int, db: AsyncSession = Depends(get_db)):
    return await services.delete_worker_service(db, worker_id)
