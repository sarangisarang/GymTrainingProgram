from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Data_Base_SQL import crud, schemas
from Data_Base_SQL.database import get_db

# Router-Objekt für Exercise-Endpoints
router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)


# -----------------------------
# ÜBUNG ERSTELLEN
# -----------------------------
@router.post("/", response_model=schemas.ExerciseRead, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    """
    Erstellt eine neue Übung.
    Prüft, ob die Übung bereits existiert.
    """
    # Prüfe, ob Übung schon existiert
    existing = crud.get_exercises(db)
    for ex in existing:
        if ex.title.lower() == exercise.title.lower() and ex.muscle_group.lower() == exercise.muscle_group.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Diese Übung existiert bereits"
            )

    return crud.create_exercise(db=db, exercise=exercise)


# -----------------------------
# ALLE ÜBUNGEN ANZEIGEN
# -----------------------------
@router.get("/", response_model=list[schemas.ExerciseRead])
def read_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Gibt alle Übungen zurück (mit Pagination).
    """
    exercises = crud.get_exercises(db, skip=skip, limit=limit)

    if not exercises:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keine Übungen gefunden"
        )

    return exercises


# -----------------------------
# EINZELNE ÜBUNG ANZEIGEN
# -----------------------------
@router.get("/{exercise_id}", response_model=schemas.ExerciseRead)
def read_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Gibt eine einzelne Übung anhand der ID zurück.
    """
    db_exercise = crud.get_exercise_by_id(db, exercise_id=exercise_id)

    if db_exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Übung nicht gefunden"
        )

    return db_exercise


# -----------------------------
# ÜBUNGEN EINES BENUTZERS ANZEIGEN
# -----------------------------
@router.get("/user/{user_id}", response_model=list[schemas.ExerciseRead])
def get_user_exercises(user_id: int, db: Session = Depends(get_db)):
    """
    Gibt alle Übungen eines bestimmten Benutzers zurück.
    """
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benutzer nicht gefunden"
        )

    return crud.get_exercises_by_user(db, user_id)


# -----------------------------
# ÜBUNG AKTUALISIEREN
# -----------------------------
@router.put("/{exercise_id}", response_model=schemas.ExerciseRead)
def update_exercise(
        exercise_id: int,
        exercise: schemas.ExerciseCreate,
        db: Session = Depends(get_db)
):
    """
    Aktualisiert eine bestehende Übung.
    """
    db_ex = crud.get_exercise_by_id(db, exercise_id)
    if not db_ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Übung nicht gefunden"
        )

    updated_ex = crud.update_exercise(db, exercise_id, exercise)
    return updated_ex


# -----------------------------
# ÜBUNG LÖSCHEN
# -----------------------------
@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Löscht eine Übung aus der Datenbank.
    """
    db_ex = crud.get_exercise_by_id(db, exercise_id)
    if not db_ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Übung nicht gefunden"
        )

    crud.delete_exercise(db, exercise_id)
    return {"message": "Übung wurde erfolgreich gelöscht"}