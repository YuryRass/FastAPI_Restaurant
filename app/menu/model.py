from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

if TYPE_CHECKING:
    from app.submenu.model import Submenu


class Menu(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]

    submenus: Mapped[list['Submenu']] = relationship(
        back_populates='menu',
        cascade='all, delete',
    )

    LINK = '/menus'
    LONG_LINK = '/menus/{menu_id}'
