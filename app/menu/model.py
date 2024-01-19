import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.submenu.model import Submenu


class Menu(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    submenu_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID,
        ForeignKey("submenu.id", ondelete="CASCADE"),
    )

    # submenus: Mapped[list["Submenu"]] = relationship(
    #     back_populates="menu",
    #     cascade="all, delete-orphan",
    # )
