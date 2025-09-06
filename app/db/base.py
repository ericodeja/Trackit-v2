from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from app.core.config import settings

if not settings.DATABASE_URL:
    raise ValueError('Missing DATABASE_URL')
engine = create_engine(settings.DATABASE_URL)


class ReprMixin:
    def __repr__(self):
        cls = self.__class__.__name__
        fields = ', '.join(
            f"{key}={getattr(self, key)!r}"
            for key in self.__dict__.keys()
            if not key.startswith('_')
        )
        return f"{cls}({fields})"


class Base(DeclarativeBase, ReprMixin):
    pass
