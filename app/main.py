from fastapi import FastAPI

from app.dish.router import router as dish_router
from app.menu.router import router as menu_router
from app.submenu.router import router as submenu_router

description = """
    FastAPI Restaurant API предоставляет комплексные решения для управления ресторанным меню,
    включая блюда, меню и подменю. Он позволяет пользователям добавлять, обновлять, удалять и
    просматривать информацию о блюдах, а также управлять структурой меню ресторана.
    """

tags_metadata = [
    {
        'name': 'Dishes',
        'description': 'Операции с блюдами. Позволяют добавлять, изменять и удалять блюда в меню.',
    },
    {
        'name': 'Submenus',
        'description': 'Управление подменю. Включает в себя создание, редактирование и удаление подменю.',
    },
    {
        'name': 'Menus',
        'description': 'Методы для работы с меню. Позволяют создавать и модифицировать меню.',
    },
]


app: FastAPI = FastAPI(
    title='FastAPI Restaurant API',
    description=description,
    version='1.0.0',
    terms_of_service='http://example.com/terms/',
    contact={
        'name': 'Support Team',
        'url': 'http://example.com/contact/',
        'email': 'support@example.com',
    },
    license_info={
        'name': 'Apache 2.0',
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
    },
    openapi_tags=tags_metadata,
    root_path='/api/v1',
)

app.include_router(dish_router)
app.include_router(submenu_router)
app.include_router(menu_router)
