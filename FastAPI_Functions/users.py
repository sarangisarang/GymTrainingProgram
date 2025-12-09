from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from Data_Base_SQL import crud, schemas
from Data_Base_SQL.database import get_db

# Router-Objekt für User-Endpoints
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# -----------------------------
# BENUTZER ERSTELLEN
# -----------------------------
@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Erstellt einen neuen Benutzer.
    Prüft, ob die E-Mail bereits existiert.
    """
    # Prüfe, ob E-Mail schon existiert
    existing_users = crud.get_users(db)
    for u in existing_users:
        if u.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-Mail existiert bereits"
            )

    return crud.create_user(db=db, user=user)


# -----------------------------
# ALLE BENUTZER ANZEIGEN
# -----------------------------
@router.get("/", response_model=List[schemas.UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Gibt alle Benutzer zurück (mit Pagination).
    Lädt automatisch ihre Workouts und Exercises (Eager Loading).
    """
    users = crud.get_users(db, skip=skip, limit=limit)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keine Benutzer gefunden"
        )

    return users


# -----------------------------
# EINZELNEN BENUTZER ANZEIGEN
# -----------------------------
@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Gibt einen einzelnen Benutzer anhand der ID zurück.
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benutzer nicht gefunden"
        )

    return db_user