import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db_creator import create_tables

from app.menu.router import router as menu_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(create_tables())
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan,
    root_path="/api/v1",
)


app.include_router(menu_router)
