import pickle

from pydantic import UUID4, BaseModel, Field, model_validator

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

    @model_validator(mode='after')
    def validate_atts(self):
        res = redis_cacher.get(str(self.id))
        if res:
            self.price = pickle.loads(res)
        self.price = str(round(self.price, 2))
        return self
