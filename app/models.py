from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional, List

class Base(DeclarativeBase): pass

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    questions: Mapped[List["Question"]] = relationship(back_populates="category", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "question"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    answer: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id", ondelete="SET NULL"), nullable=True)
    category: Mapped[Optional[Category]] = relationship(back_populates="questions")
