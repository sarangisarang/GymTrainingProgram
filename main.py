from fastapi import FastAPI
from Data_Base_SQL.database import engine
from Data_Base_SQL import models
from FastAPI_Funcions import users, exercises, workout


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inkludiert die Router-Objekte aus den Funktionsmodulen.
app.include_router(users.router)
app.include_router(exercises.router)
app.include_router(workout.router)


@app.get("/")
def home():
    return {"message": "Gym API is running!"}