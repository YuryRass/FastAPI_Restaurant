from pydantic import UUID4, BaseModel


class JsonDish(BaseModel):
    id: UUID4
    title: str
    description: str
    price: float


class JsonSubmenu(BaseModel):
    id: UUID4
    title: str
    description: str
    dishes: list[JsonDish]


class JsonMenu(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus: list[JsonSubmenu]
