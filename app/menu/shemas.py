from pydantic import UUID4, BaseModel, Field


class SMenu(BaseModel):
    """Схема меню для создания/изменения."""
    id: UUID4 | None = Field(
        None,
        description='Уникальный идентификатор меню',
        example='52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
    )
    title: str | None = Field(
        None, description='Название меню', example='Специальное меню'
    )
    description: str | None = Field(
        None,
        description='Описание меню',
        example='Это меню предлагает разнообразные блюда',
    )


class OutSMenu(BaseModel):
    """Схема меню для вывода."""
    id: UUID4 = Field(
        ...,
        description='Уникальный идентификатор меню',
        example='52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
    )
    title: str = Field(..., description='Название меню', example='Специальное меню')
    description: str = Field(
        ...,
        description='Описание меню',
        example='Это меню предлагает разнообразные блюда',
    )
    submenus_count: int = Field(..., description='Количество подменю в меню', example=2)
    dishes_count: int = Field(..., description='Количество блюд в меню', example=15)
