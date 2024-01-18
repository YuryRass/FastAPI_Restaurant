from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.dish.model import Dish
    from app.menu.model import Menu


class Submenu(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]

    dish_id: Mapped[int] = mapped_column(ForeignKey("dish.id"))
    dishes: Mapped[list["Dish"]] = relationship(back_populates="submenu")
    menu: Mapped["Menu"] = relationship(back_populates="submenus")
