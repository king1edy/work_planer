from fastapi import FastAPI
from app.api import workers, shifts
from app.database import engine, Base
import uvicorn
app = FastAPI()

app.include_router(workers.router, prefix="/workers", tags=["workers"])
app.include_router(shifts.router, prefix="/shifts", tags=["shifts"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
