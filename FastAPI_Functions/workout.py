from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session

from Class_Functions.Workout_Generator import WorkoutGenerator
from Data_Base_SQL.crud import create_workout
from Data_Base_SQL.database import get_db
from Data_Base_SQL.schemas import WorkoutCreate, WorkoutRead

app = APIRouter(prefix="/workout", tags=["Workout"])


# -----------------------------------
# GENERATE WORKOUT PLAN (no database)
# -----------------------------------
@app.get("/{days}")
def generate_workout(days: int):
    generator = WorkoutGenerator()
    return generator.generate_plan(days)


# -----------------------------------
# CREATE WORKOUT (UUID-compatible)
# -----------------------------------
@app.post("/workouts", response_model=WorkoutRead)
def create_workout_endpoint(payload: WorkoutCreate, db: Session = Depends(get_db)):
    workout = create_workout(db, payload)

    if not workout:
        raise HTTPException(status_code=400, detail="Workout konnte nicht erstellt werden")

    return workout