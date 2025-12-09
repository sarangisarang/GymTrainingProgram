from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Data_Base_SQL import schemas, crud
from Data_Base_SQL.database import get_db

# Router-Objekt für Workout-Exercise-Verknüpfungen
router = APIRouter(
    prefix="/workout-exercises",
    tags=["Workout Exercises"]
)


# -----------------------------
# ÜBUNG ZU WORKOUT HINZUFÜGEN (CREATE)
# -----------------------------
@router.post("/", response_model=schemas.WorkoutExerciseRead, status_code=status.HTTP_201_CREATED)
def create_workout_exercise_link(
        item: schemas.WorkoutExerciseCreate,
        db: Session = Depends(get_db)
):
    """
    Verknüpft eine Übung mit einem Workout.
    Speichert Sets, Reps und Weight.
    """
    # Prüfe, ob Workout existiert
    db_workout = crud.get_workout_by_id(db, workout_id=item.workout_id)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout mit ID {item.workout_id} nicht gefunden"
        )

    # Prüfe, ob Exercise existiert
    db_exercise = crud.get_exercise_by_id(db, exercise_id=item.exercise_id)
    if not db_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise mit ID {item.exercise_id} nicht gefunden"
        )

    # Erstelle die Verknüpfung
    return crud.create_workout_exercise(db=db, item=item)


# -----------------------------
# ALLE WORKOUT-EXERCISE VERKNÜPFUNGEN ANZEIGEN (READ)
# -----------------------------
@router.get("/", response_model=list[schemas.WorkoutExerciseRead])
def get_all_workout_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Gibt alle Workout-Exercise-Verknüpfungen zurück (mit Pagination).
    """
    workout_exercises = crud.get_workout_exercises(db, skip=skip, limit=limit)

    if not workout_exercises:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keine Workout-Exercise-Verknüpfungen gefunden"
        )

    return workout_exercises


# -----------------------------
# EINZELNE VERKNÜPFUNG ANZEIGEN (READ)
# -----------------------------
@router.get("/{workout_exercise_id}", response_model=schemas.WorkoutExerciseRead)
def get_workout_exercise(workout_exercise_id: int, db: Session = Depends(get_db)):
    """
    Gibt eine einzelne Workout-Exercise-Verknüpfung anhand der ID zurück.
    """
    db_link = db.query(crud.models.WorkoutExercise).filter(
        crud.models.WorkoutExercise.id == workout_exercise_id
    ).first()

    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout-Exercise-Verknüpfung nicht gefunden"
        )

    return db_link


# -----------------------------
# ALLE ÜBUNGEN EINES WORKOUTS ANZEIGEN (READ)
# -----------------------------
@router.get("/workout/{workout_id}", response_model=list[schemas.WorkoutExerciseRead])
def get_workout_exercises(workout_id: int, db: Session = Depends(get_db)):
    """
    Gibt alle Übungen eines bestimmten Workouts zurück.
    """
    db_workout = crud.get_workout_by_id(db, workout_id=workout_id)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout nicht gefunden"
        )

    return db_workout.exercises_link


# -----------------------------
# VERKNÜPFUNG AKTUALISIEREN (UPDATE)
# -----------------------------
@router.put("/{workout_exercise_id}", response_model=schemas.WorkoutExerciseRead)
def update_workout_exercise(
        workout_exercise_id: int,
        item: schemas.WorkoutExerciseCreate,
        db: Session = Depends(get_db)
):
    """
    Aktualisiert eine bestehende Workout-Exercise-Verknüpfung.
    Kann Sets, Reps und Weight ändern.
    """
    # Suche die Verknüpfung
    db_link = db.query(crud.models.WorkoutExercise).filter(
        crud.models.WorkoutExercise.id == workout_exercise_id
    ).first()

    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout-Exercise-Verknüpfung nicht gefunden"
        )

    # Prüfe, ob neues Workout existiert (falls geändert)
    db_workout = crud.get_workout_by_id(db, workout_id=item.workout_id)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout mit ID {item.workout_id} nicht gefunden"
        )

    # Prüfe, ob neue Exercise existiert (falls geändert)
    db_exercise = crud.get_exercise_by_id(db, exercise_id=item.exercise_id)
    if not db_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise mit ID {item.exercise_id} nicht gefunden"
        )

    # Aktualisiere die Verknüpfung
    db_link.workout_id = item.workout_id
    db_link.exercise_id = item.exercise_id
    db_link.sets = item.sets
    db_link.reps = item.reps
    db_link.weight = item.weight

    db.commit()
    db.refresh(db_link)

    return db_link


# -----------------------------
# ÜBUNG AUS WORKOUT ENTFERNEN (DELETE)
# -----------------------------
@router.delete("/{workout_exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout_exercise(workout_exercise_id: int, db: Session = Depends(get_db)):
    """
    Löscht eine Workout-Exercise-Verknüpfung.
    """
    # Suche die Verknüpfung
    db_link = db.query(crud.models.WorkoutExercise).filter(
        crud.models.WorkoutExercise.id == workout_exercise_id
    ).first()

    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout-Exercise-Verknüpfung nicht gefunden"
        )

    # Lösche die Verknüpfung
    db.delete(db_link)
    db.commit()

    return {"message": "Verknüpfung erfolgreich gelöscht"}