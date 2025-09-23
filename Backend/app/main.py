from fastapi import FastAPI, Depends
from app.api.routers import auth
from app.schemas.habit import Habit, HabitUpdate, HabitDelete
from app.crud.habit import create_habit, edit_habit, delete_habit
from app.core.security import get_current_user

app = FastAPI()

app.include_router(auth.router)



@app.get('/ping')
def health_check():
    return {'status': 'ok'}

@app.post('/create-habit')
def create_habit_route(data: Habit, user: dict = Depends(get_current_user)):
    return create_habit(data, user)


@app.patch('/edit-habit')
def edit_habit_route(data: HabitUpdate, user: dict = Depends(get_current_user)):
    return edit_habit(data)

@app.patch('/delete-habit')
def delete_habit_route(data: HabitDelete, user: dict = Depends(get_current_user)):
    return delete_habit(data)




