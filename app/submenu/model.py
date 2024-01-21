import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Submenu(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]

    menu_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("menu.id", ondelete="CASCADE"),
    )
