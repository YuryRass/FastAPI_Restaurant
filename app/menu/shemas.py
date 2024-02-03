from pydantic import UUID4, BaseModel


class SMenu(BaseModel):
    """Схема меню."""
    title: str
    description: str


class OutSMenu(BaseModel):
    """Схема меню для вывода."""
    id: UUID4
    title: str
    description: str
    submenus_count: int
    dishes_count: int
