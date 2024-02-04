from pydantic import UUID4, BaseModel


class SSubMenu(BaseModel):
    """Схмеа подменю."""
    title: str
    description: str


class OutSSubMenu(BaseModel):
    """Схема для вывода подменю."""
    id: UUID4
    title: str
    description: str
    dishes_count: int
