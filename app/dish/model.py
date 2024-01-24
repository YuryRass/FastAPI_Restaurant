from typing import TYPE_CHECKING
import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.submenu.model import Submenu


class Dish(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[float]

    submenu_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("submenu.id", ondelete="CASCADE"),
    )

    submenu: Mapped["Submenu"] = relationship(back_populates="dishes")
