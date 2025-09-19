from fastapi import FastAPI, Depends
from app.api.routers import auth
from app.schemas.habit import Habit
from app.crud.habit import create_habit
from app.core.security import get_current_user

app = FastAPI()

app.include_router(auth.router)



@app.get('/ping')
def health_check():
    return {'status': 'ok'}

@app.post('/create-habit')
def create_habit_route(data: Habit, user: dict = Depends(get_current_user)):
    return create_habit(data, user)




