from uuid import uuid4

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base.base import Base



class Party(Base):
    __tablename__ = "parties"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, index=True, default=lambda: str(uuid4()))
    party_name: Mapped[str] = mapped_column(String(50))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="parties", uselist=False)
    items: Mapped[list["Item"]] = relationship("Item",back_populates="party", uselist=True)
    