from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from app.core.settings import settings
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def init_db():

    if not settings.DATABASE_URL:
        raise ValueError('DATABASE_URL not found')

    engine = create_engine(settings.DATABASE_URL, echo=True)

    if not database_exists(engine.url):
        print("Database does not exist. Creating...")
        create_database(engine.url)
    else:
        print("Database already exists.")

    print("Creating tables (if not exist)...")
    Base.metadata.create_all(engine)
    print("Done")


if __name__ == "__main__":
    init_db()


