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
