from fastapi import FastAPI

from app.menu.router import router as menu_router

app = FastAPI(root_path="/api/v1")

app.include_router(menu_router)
