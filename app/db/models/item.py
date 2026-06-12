from sqlalchemy import String, ForeignKey
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base.base import Base



class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String(100))
    artist_name: Mapped[str] = mapped_column(String(255))
    provided_link: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(30))
    s3_name: Mapped[str] = mapped_column(String(255))
    added_user: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    added_by_user: Mapped[Optional["User"]] = relationship("User")
    added_by_name: Mapped[str] = mapped_column(String(50))
    party_id: Mapped[int] = mapped_column(ForeignKey("parties.id"))
    party: Mapped["Party"] = relationship("Party", back_populates="items", uselist=False)

