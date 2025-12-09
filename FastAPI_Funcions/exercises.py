from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Data_Base_SQL import crud, schemas, database


# Definiert und exportiert das 'router'-Objekt, das in main.py benötigt wird
router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)


# Dependency, um die Datenbank-Session zu erhalten (Wiederverwendung der Funktion aus database.py)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ExerciseRead, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    # Annahme: 'create_exercise' Funktion ist in crud.py definiert
    return crud.create_exercise(db=db, exercise=exercise)

@router.get("/", response_model=list[schemas.ExerciseRead])
def read_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Annahme: 'get_exercises' Funktion ist in crud.py definiert
    exercises = crud.get_exercises(db, skip=skip, limit=limit)
    return exercises

@router.get("/{exercise_id}", response_model=schemas.ExerciseRead)
def read_exercise(exercise_id: int, db: Session = Depends(get_db)):
    # Annahme: 'get_exercise' Funktion ist in crud.py definiert
    db_exercise = crud.get_exercise(db, exercise_id=exercise_id)
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return db_exercise