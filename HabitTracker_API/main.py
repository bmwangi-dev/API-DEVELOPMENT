# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from database import engine
import models
from routers import user, habit

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")

app.include_router(user.router)
app.include_router(habit.router)