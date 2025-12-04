from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Data_Base_SQL.database import get_db
from Data_Base_SQL import crud, schemas

app = APIRouter(prefix="/exercises", tags=["Exercises"])


# -----------------------------
# CREATE EXERCISE (without user)
# -----------------------------
@app.post("/", response_model=schemas.ExerciseRead)
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    existing = crud.get_exercises(db)

    for ex in existing:
        if ex.title.lower() == exercise.title.lower() and ex.muscle_group.lower() == exercise.muscle_group.lower():
            raise HTTPException(status_code=400, detail="This exercise already exists")

    return crud.create_exercise(db, exercise)


# -----------------------------
# LIST ALL EXERCISES
# -----------------------------
@app.get("/", response_model=list[schemas.ExerciseRead])
def list_exercises(db: Session = Depends(get_db)):
    exercises = crud.get_exercises(db)

    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found")

    return exercises



# -----------------------------
# CREATE EXERCISE FOR SPECIFIC USER
# -----------------------------
@app.post("/user/{user_id}", response_model=schemas.ExerciseRead)
def create_user_exercise(user_id: int, exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_exercise_for_user(db, user_id, exercise)


# -----------------------------
# GET EXERCISES BELONGING TO A USER
# -----------------------------
@app.get("/user/{user_id}", response_model=list[schemas.ExerciseRead])
def get_user_exercises(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_exercises_by_user(db, user_id)