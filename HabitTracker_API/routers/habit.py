from typing import List
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

import models
import schemas
import auth
from database import get_db

router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)

@router.post("/", response_model=schemas.HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_habit = models.Habit(**habit.model_dump(), user_id=current_user.id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.get("/", response_model=List[schemas.HabitResponse])
def read_habits(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    habits = db.query(models.Habit).filter(models.Habit.user_id == current_user.id).all()
    return habits

@router.get("/{habit_id}", response_model=schemas.HabitResponse)
def read_habit(habit_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.patch("/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(habit_id: str, habit_update: schemas.HabitUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    update_data = habit_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_habit, key, value)
    
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db.delete(db_habit)
    db.commit()
    return None
