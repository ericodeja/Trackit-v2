from app.db.base import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status


class Db_connection:

    @classmethod
    def open_connection(cls):
        with Session(engine) as session:
            return session

    def __init__(self):
        self.session = Db_connection.open_connection()

    def get_all(self, model):

        stmt = select(model)
        result = self.session.execute(stmt).scalars().all()

        return result

    def get_one(self, model, x, y):

        stmt = select(model).where(x == y)
        result = self.session.execute(stmt).scalar_one_or_none()

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Required model not found')

        return result

    def add(self, new_model):
        self.session.add(new_model)
        self.session.commit()

    def delete(self, model):
        self.session.delete(model)
        self.session.commit()


db_connection = Db_connection()
