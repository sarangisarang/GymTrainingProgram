from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Data_Base_SQL.database import get_db
from Data_Base_SQL import crud, schemas

# Erstellt einen API-Router für alle Endpunkte, die mit Benutzern verknüpft sind
app = APIRouter(prefix="/users", tags=["Benutzer"])


# -----------------------------
# BENUTZER ERSTELLEN
# -----------------------------
@app.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Erstellt einen neuen Benutzer in der Datenbank.
    Überprüft optional, ob die angegebene E-Mail-Adresse bereits existiert,
    um doppelte Benutzer zu vermeiden.
    """
    existing = crud.get_users(db)
    for u in existing:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="E-Mail existiert bereits")

    return crud.create_user(db, user)


# -----------------------------
# ALLE BENUTZER ANZEIGEN
# -----------------------------
@app.get("/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    """
    Gibt eine Liste aller registrierten Benutzer zurück.
    Falls keine Benutzer vorhanden sind, wird ein Fehler 404 ausgelöst.
    """
    users = crud.get_users(db)

    if not users:
        raise HTTPException(status_code=404, detail="Keine Benutzer gefunden")

    return users


# -----------------------------
# BENUTZER NACH ID ABRUFEN
# -----------------------------
@app.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Ruft einen einzelnen Benutzer anhand seiner ID ab.
    Wenn der Benutzer nicht existiert, wird ein Fehler 404 ausgelöst.
    """
    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")

    return user
