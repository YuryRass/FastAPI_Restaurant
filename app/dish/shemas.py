from pydantic import UUID4, BaseModel, field_validator


class SDish(BaseModel):
    """Схема блюда."""
    title: str
    description: str
    price: float


class SUUId(BaseModel):
    """Схема идентификатора блюда."""
    id: UUID4


class OutSDish(SDish, SUUId):
    """Схема для вывода информации о блюде."""

    @field_validator('price')
    @classmethod
    def to_str(cls, value) -> str:
        """Округление до двух знаков после запятой и преобразование в строку."""
        if isinstance(value, float):
            value = str(round(value, 2))
        return value
