from fastapi import FastAPI

from app.dish.router import router as dish_router
from app.menu.router import router as menu_router
from app.submenu.router import router as submenu_router

app: FastAPI = FastAPI(
    root_path="/api/v1",
)

app.include_router(dish_router)
app.include_router(submenu_router)
app.include_router(menu_router)
