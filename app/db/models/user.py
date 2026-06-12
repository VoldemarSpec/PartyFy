from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), index=True)
    hashed_password: Mapped[str] = mapped_column(String(60))
    parties: Mapped[list["Party"]] = relationship("Party", back_populates="owner", uselist=True)
