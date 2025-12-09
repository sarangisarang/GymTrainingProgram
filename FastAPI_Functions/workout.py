from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from Data_Base_SQL import crud, schemas
from Data_Base_SQL.database import get_db

# Router-Objekt für Workout-Endpoints
router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


# -----------------------------
# WORKOUT ERSTELLEN
# -----------------------------
@router.post("/", response_model=schemas.WorkoutRead, status_code=status.HTTP_201_CREATED)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    """
    Erstellt ein neues Workout für einen Benutzer.
    Prüft, ob der Benutzer existiert.
    """
    # Prüfe, ob Benutzer existiert
    db_user = crud.get_user_by_id(db, user_id=workout.user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benutzer mit ID {workout.user_id} wurde nicht gefunden"
        )

    # Erstelle das Workout
    return crud.create_workout(db=db, workout=workout)


# -----------------------------
# ALLE WORKOUTS ANZEIGEN
# -----------------------------
@router.get("/", response_model=List[schemas.WorkoutRead])
def read_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Gibt alle Workouts zurück (mit Pagination).
    """
    workouts = crud.get_workouts(db, skip=skip, limit=limit)

    if not workouts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keine Workouts gefunden"
        )

    return workouts


# -----------------------------
# EINZELNES WORKOUT ANZEIGEN
# -----------------------------
@router.get("/{workout_id}", response_model=schemas.WorkoutRead)
def read_workout(workout_id: int, db: Session = Depends(get_db)):
    """
    Gibt ein einzelnes Workout anhand der ID zurück.
    """
    db_workout = crud.get_workout_by_id(db, workout_id=workout_id)

    if db_workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout nicht gefunden"
        )

    return db_workout


# -----------------------------
# WORKOUTS EINES BENUTZERS ANZEIGEN
# -----------------------------
@router.get("/user/{user_id}", response_model=List[schemas.WorkoutRead])
def get_user_workouts(user_id: int, db: Session = Depends(get_db)):
    """
    Gibt alle Workouts eines bestimmten Benutzers zurück.
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benutzer nicht gefunden"
        )

    # Gib die Workouts des Benutzers zurück
    return db_user.workouts