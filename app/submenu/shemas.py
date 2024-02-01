from pydantic import UUID4, BaseModel


class SSubMenu(BaseModel):
    title: str
    description: str


class OutSSubMenu(BaseModel):
    id: UUID4
    title: str
    description: str
    dishes_count: int
