from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Data_Base_SQL.database import get_db
from Data_Base_SQL import crud, schemas

app = APIRouter(prefix="/users", tags=["Users"])


# -----------------------------
# CREATE USER
# -----------------------------
@app.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Email uniqueness check (optional but recommended)
    existing = crud.get_users(db)
    for u in existing:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db, user)


# -----------------------------
# LIST USERS
# -----------------------------
@app.get("/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)

    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


# -----------------------------
# GET USER BY ID
# -----------------------------
@app.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user