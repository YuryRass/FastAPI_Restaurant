from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Menu(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
