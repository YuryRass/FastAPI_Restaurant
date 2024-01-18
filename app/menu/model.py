from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.submenu.model import Submenu


class Menu(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    submenu_id: Mapped[int] = mapped_column(ForeignKey("submenu.id"))
    
    submenus: Mapped[list["Submenu"]] = relationship(back_populates="menu")