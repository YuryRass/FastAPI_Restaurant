import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UUID
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
        ForeignKey("menu.id", ondelete="CASCADE"),
    )

