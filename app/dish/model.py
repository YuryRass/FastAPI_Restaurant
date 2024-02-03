import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.submenu.model import Submenu


class Dish(Base):
    """Таблица, описывающая блюда ресторана."""
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[float]

    submenu_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('submenu.id', ondelete='CASCADE'),
    )

    submenu: Mapped['Submenu'] = relationship(back_populates='dishes')

    DISHES_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes'
    DISH_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
