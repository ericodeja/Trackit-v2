from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email:Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def __repr__(self) -> str:
        return f'User(id{self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})'

