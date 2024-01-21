import uuid

from sqlalchemy import UUID, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Dish(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[float]

    submenu_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("submenu.id", ondelete="CASCADE"),
    )
