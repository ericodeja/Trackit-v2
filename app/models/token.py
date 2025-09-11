from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import app.models.user 

class Token(Base):
    __tablename__ = 'tokens'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]  = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    token: Mapped[str]
    expires: Mapped[int]

    user: Mapped['app.models.user.User'] = relationship('User', back_populates='token')

