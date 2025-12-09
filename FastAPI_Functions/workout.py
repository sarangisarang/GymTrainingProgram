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
# WORKOUT ERSTELLEN (CREATE)
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
# ALLE WORKOUTS ANZEIGEN (READ)
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
# EINZELNES WORKOUT ANZEIGEN (READ)
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
# WORKOUTS EINES BENUTZERS ANZEIGEN (READ)
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


# -----------------------------
# WORKOUT AKTUALISIEREN (UPDATE)
# -----------------------------
@router.put("/{workout_id}", response_model=schemas.WorkoutRead)
def update_workout(
        workout_id: int,
        workout: schemas.WorkoutCreate,
        db: Session = Depends(get_db)
):
    """
    Aktualisiert ein bestehendes Workout.
    """
    db_workout = crud.get_workout_by_id(db, workout_id)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout nicht gefunden"
        )

    # Prüfe, ob der neue Benutzer existiert (falls user_id geändert wird)
    db_user = crud.get_user_by_id(db, user_id=workout.user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benutzer mit ID {workout.user_id} wurde nicht gefunden"
        )

    updated_workout = crud.update_workout(db, workout_id, workout)
    return updated_workout


# -----------------------------
# WORKOUT LÖSCHEN (DELETE)
# -----------------------------
@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    """
    Löscht ein Workout aus der Datenbank.
    """
    db_workout = crud.get_workout_by_id(db, workout_id)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout nicht gefunden"
        )

    crud.delete_workout(db, workout_id)
    return {"message": "Workout wurde erfolgreich gelöscht"}