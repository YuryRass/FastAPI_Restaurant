from pydantic import BaseModel, UUID4


class JsonDish(BaseModel):
    id: UUID4
    title: str
    description: str
    price: float
    # discount: int

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