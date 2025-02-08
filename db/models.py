from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# tables
class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class Expense_Base(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    many: Mapped[int] = mapped_column()
    who: Mapped[str] = mapped_column(String(30))
    reason: Mapped[str] = mapped_column(String(200))


class Income_Base(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(primary_key=True)
    many: Mapped[int] = mapped_column()
    where_from: Mapped[str] = mapped_column(String(200))
    reason: Mapped[str] = mapped_column(String(200))


