from pydantic import UUID4, BaseModel, field_validator


class SDish(BaseModel):
    title: str
    description: str
    price: float


class SUUId(BaseModel):
    id: UUID4


class OutSDish(SDish, SUUId):
    @field_validator('price')
    @classmethod
    def to_str(cls, value) -> str:
        if isinstance(value, float):
            value = str(round(value, 2))
        return value
