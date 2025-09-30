from fastapi import FastAPI, Depends
from app.api.routers import auth, user
from app.core.security import get_current_user
from app.schemas.habit import Habit, HabitUpdate, HabitBase
from app.crud.habit import create_habit, edit_habit, delete_habit, complete_habit, get_all_habits
from app.crud.habit_completions import get_completion
from app.utils.habit_frequency import habit_checker
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def safe_checker():
        while True:
            try:
                await habit_checker()
            except Exception as e:
                print(f"[Habit Checker Error]: {e}")
                await asyncio.sleep(5)

    task = asyncio.create_task(safe_checker())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(user.router)

# CREATE


@app.post('/create')
def create_habit_route(data: Habit, user: dict = Depends(get_current_user)):
    return create_habit(data, user)

# READ


@app.get('/completion-history/{habit_id}')
def get_completion_history_route(habit_id, user: dict = Depends(get_current_user)):
    return get_completion(habit_id)


@app.get('/habits')
def get_all_habits_route(user: dict = Depends(get_current_user)):
    return get_all_habits(user)

# UPDATE


@app.patch('/edit')
def edit_habit_route(data: HabitUpdate, user: dict = Depends(get_current_user)):
    return edit_habit(data)


@app.post('/complete')
def complete_habit_route(data: HabitBase, user: dict = Depends(get_current_user)):
    return complete_habit(data)

# DELETE


@app.delete('/habit')
def delete_habit_route(data: HabitBase, user: dict = Depends(get_current_user)):
    return delete_habit(data)
