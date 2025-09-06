from fastapi import FastAPI
from app.api.routers import auth

app = FastAPI()

app.include_router(auth.router)



@app.get('/ping')
def health_check():
    return {'status': 'ok'}
