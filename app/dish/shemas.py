import pickle

from pydantic import UUID4, BaseModel, Field, field_validator, model_validator

from app.database.sync_redis import redis_cacher


class SDish(BaseModel):
    """Схема блюда для создания/изменения."""

    id: UUID4 | None = Field(
        None,
        description='Уникальный идентификатор блюда',
        example='52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
    )
    title: str | None = Field(None, description='Название блюда', example='Цезарь')
    description: str | None = Field(
        None,
        description='Описание блюда',
        example='Классический салат Цезарь с курицей',
    )
    price: float | None = Field(None, description='Цена блюда в USD', example=7.99)


class OutSDish(SDish):
    """Схема для вывода информации о блюде."""

    @field_validator('price')
    @classmethod
    def to_str(cls, value) -> str:
        """Округление до двух знаков после запятой и преобразование в строку."""
        if isinstance(value, float):
            value = str(round(value, 2))
        return value

    @model_validator(mode='after')
    def validate_atts(self):
        res = redis_cacher.get(str(self.id))
        if res:
            self.price = pickle.loads(res)
        self.price = str(self.price)
        return self
