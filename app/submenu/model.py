import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.dish.model import Dish
    from app.menu.model import Menu


class Submenu(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]

    menu_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('menu.id', ondelete='CASCADE'),
    )

    menu: Mapped['Menu'] = relationship(back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship(
        back_populates='submenu',
        cascade='all, delete',
    )

    SUBMENUS_LINK = '/menus/{menu_id}/submenus'
    SUBMENU_LINK = '/menus/{menu_id}/submenus/{submenu_id}'
