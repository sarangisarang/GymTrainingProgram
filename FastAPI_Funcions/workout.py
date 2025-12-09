from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from Class_Funcions.Workout_Generator import WorkoutGenerator
from Data_Base_SQL.database import get_db
from Data_Base_SQL import schemas as schemas_workouts
from Data_Base_SQL import crud as crud_workouts


router = APIRouter(
    prefix="/workout",
    tags=["Workout"]
)

@router.get("/{days}")
def generate_workout(days: int):
    generator = WorkoutGenerator()
    return generator.generate_plan(days)

@router.post("/", response_model=schemas_workouts.WorkoutRead, status_code=status.HTTP_201_CREATED)
def create_new_workout(workout: schemas_workouts.WorkoutCreate, db: Session = Depends(get_db)):
    return crud_workouts.create_workout(db=db, workout=workout)