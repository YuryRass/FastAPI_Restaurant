from pydantic import UUID4, BaseModel


class SMenu(BaseModel):
    title: str
    description: str


class OutSMenu(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int
    dishes_count: int
