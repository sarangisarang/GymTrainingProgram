# workouts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import crud_workouts, schemas_workouts
from database import get_db # Funktion, um eine Datenbank-Session zu bekommen

# Definiert den Router, der alle Endpunkte für Workouts enthält
router = APIRouter(
    prefix="/workouts", # Alle Pfade beginnen mit /workouts
    tags=["Workouts"] # Gruppiert die Endpunkte in der Doku (Swagger UI)
)

# Endpoint: POST /workouts (Neues Training erstellen)
@router.post("/", response_model=schemas_workouts.WorkoutRead, status_code=status.HTTP_201_CREATED)
def create_new_workout(workout: schemas_workouts.WorkoutCreate, db: Session = Depends(get_db)):
    return crud_workouts.create_workout(db=db, workout=workout)

# Endpoint: GET /workouts (Alle Trainings auflisten)
@router.get("/", response_model=List[schemas_workouts.WorkoutRead])
def list_all_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_workouts.list_workouts(db=db, skip=skip, limit=limit)

# Endpoint: GET /workouts/{id} (Ein bestimmtes Training holen)
@router.get("/{id}", response_model=schemas_workouts.WorkoutRead)
def get_single_workout(id: int, db: Session = Depends(get_db)):
    db_workout = crud_workouts.get_workout(db=db, workout_id=id)
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout nicht gefunden") # Fehlermeldung, falls nicht da
    return db_workout

# Endpoint: DELETE /workouts/{id} (Ein bestimmtes Training löschen)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_workout(id: int, db: Session = Depends(get_db)):
    db_workout = crud_workouts.delete_workout(db=db, workout_id=id)
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout nicht gefunden")
    return # 204 hat keinen Rückgabetext

# --- Endpunkte für die Übungen im Training ---

# Endpoint: POST /workouts/{id}/exercises (Übung zu Training hinzufügen)
@router.post("/{id}/exercises", response_model=schemas_workouts.WorkoutExerciseRead, status_code=status.HTTP_201_CREATED)
def add_exercise_to_workout(
    id: int, # Dies ist die ID des Workouts
    exercise: schemas_workouts.WorkoutExerciseCreate, 
    db: Session = Depends(get_db)
):
    # Prüfen, ob das Workout existiert
    db_workout = crud_workouts.get_workout(db=db, workout_id=id)
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout nicht gefunden")
        
    return crud_workouts.create_workout_exercise(db=db, exercise=exercise, workout_id=id)

# Endpoint: GET /workouts/{id}/exercises (Alle Übungen eines Trainings auflisten)
@router.get("/{id}/exercises", response_model=List[schemas_workouts.WorkoutExerciseRead])
def list_workout_exercises(id: int, db: Session = Depends(get_db)):
    # Auch hier prüfen wir, ob das Workout existiert
    db_workout = crud_workouts.get_workout(db=db, workout_id=id)
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout nicht gefunden")

    return crud_workouts.get_workout_exercises(db=db, workout_id=id)

# Endpoint: DELETE /workouts/exercise/{id} (Einzelne Übung löschen)
@router.delete("/exercise/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_workout_exercise(id: int, db: Session = Depends(get_db)):
    db_exercise = crud_workouts.delete_workout_exercise(db=db, exercise_id=id)
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Workout Übung nicht gefunden")
    return