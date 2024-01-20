import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db_creator import create_tables

from app.dish.router import router as dish_router
from app.menu.router import router as menu_router
from app.submenu.router import router as submenu_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(create_tables())
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan,
    root_path="/api/v1",
)

app.include_router(dish_router)
app.include_router(submenu_router)
app.include_router(menu_router)
