# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from database import engine
import models
from routers import user, habit, file

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")


@app.get("/")
def read_root():
    return {
        "name": "Habit Tracker API",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "routes": {
            "users": "/users",
            "habits": "/habits",
            "profile_image": "/users/me/profile-image",
        },
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(user.router)
app.include_router(habit.router)
app.include_router(file.router)
