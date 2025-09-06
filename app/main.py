# app/main.py
from fastapi import FastAPI
from .db import engine
from .models import Base
from .routers import categories, questions

app = FastAPI(title="HW6 – FastAPI Questions with Categories")

# создаём таблицы в SQLite
Base.metadata.create_all(bind=engine)

# подключаем роутеры
app.include_router(categories.router)
app.include_router(questions.router)

@app.get("/")
def root():
    return {"status": "ok"}
