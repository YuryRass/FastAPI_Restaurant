from pydantic import UUID4, BaseModel, Field


class SSubMenu(BaseModel):
    """Схема подменю."""
    title: str = Field(..., description='Название подменю', example='Новое подменю')
    description: str = Field(..., description='Описание подменю', example='Описание нового подменю')


class OutSSubMenu(BaseModel):
    """Схема для вывода подменю."""
    id: UUID4 = Field(..., description='ID подменю', example='52777d1c-04b3-4a5a-9f1f-43e212ed0c2a')
    title: str = Field(..., description='Название подменю', example='Новое подменю')
    description: str = Field(..., description='Описание подменю', example='Описание нового подменю')
    dishes_count: int = Field(..., description='Количество блюд в подменю', example=0)
