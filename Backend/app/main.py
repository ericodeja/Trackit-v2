from fastapi import FastAPI, Depends
from app.api.routers import auth
from app.core.security import get_current_user
from app.schemas.habit import Habit, HabitUpdate, HabitBase
from app.crud.habit import create_habit, edit_habit, delete_habit, complete_habit
from app.crud.habit_completions import get_completion

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

@app.delete('/delete-habit')
def delete_habit_route(data: HabitBase, user: dict = Depends(get_current_user)):
    return delete_habit(data)

@app.post('/complete-habit')
def complete_habit_route(data: HabitBase, user: dict = Depends(get_current_user)):
    return complete_habit(data)

@app.get('/completion-history/{habit_id}')
def get_completion_history_route(habit_id, user: dict = Depends(get_current_user)):
    return get_completion(habit_id)