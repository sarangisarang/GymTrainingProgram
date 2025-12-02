from fastapi import FastAPI, Depends
from Data_Base_SQL.database import Base, engine, get_db
from Data_Base_SQL import crud, schemas, models
from sqlalchemy.orm import Session

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/exercises")
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    return crud.create_exercise(db, exercise)


@app.get("/exercises")
def list_exercises(db: Session = Depends(get_db)):
    return crud.get_exercises(db)

@app.get("/")
def home():
    return {"message": "Gym API is running!"}
