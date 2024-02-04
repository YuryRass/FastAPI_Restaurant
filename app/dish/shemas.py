from pydantic import UUID4, BaseModel, Field, field_validator


class SDish(BaseModel):
    """Схема блюда."""
    title: str = Field(..., description='Название блюда', example='Цезарь')
    description: str = Field(..., description='Описание блюда', example='Классический салат Цезарь с курицей')
    price: float = Field(..., description='Цена блюда в USD', example=7.99)


class SUUId(BaseModel):
    """Схема идентификатора блюда."""
    id: UUID4 = Field(..., description='Уникальный идентификатор блюда', example='52777d1c-04b3-4a5a-9f1f-43e212ed0c2a')


class OutSDish(SDish, SUUId):
    """Схема для вывода информации о блюде."""

    @field_validator('price')
    @classmethod
    def to_str(cls, value) -> str:
        """Округление до двух знаков после запятой и преобразование в строку."""
        if isinstance(value, float):
            value = str(round(value, 2))
        return value
