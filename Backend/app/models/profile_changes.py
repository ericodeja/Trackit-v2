from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from sqlalchemy import ForeignKey, String, DateTime, func
from datetime import datetime
import app.models.user

class ProfileChange(Base):
    __tablename__ = 'profile_changes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    field_name: Mapped[str] = mapped_column(String(100))
    old_value: Mapped[str] = mapped_column(nullable=True)
    new_value: Mapped[str] = mapped_column(nullable=True)
    changed_by: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped['app.models.user.User'] = relationship('User',foreign_keys=[user_id], back_populates='profile_change')
    changer: Mapped['app.models.user.User'] = relationship('User', foreign_keys=[changed_by])
