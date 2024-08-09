from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import workers, shifts
from app.database import engine, Base, SessionLocal
import uvicorn

app = FastAPI()

app.include_router(workers.router, prefix="/workers", tags=["workers"])
app.include_router(shifts.router, prefix="/shifts", tags=["shifts"])

# Correcting init_db function to be an async function and await it properly
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# @app.on_event("startup")
# async def on_startup():
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# app = FastAPI(lifespan=lifespan)

# Use the event system to run init_db on startup
@app.on_event("startup")
async def on_startup():
    await init_db()

# Dependency to get DB session
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
