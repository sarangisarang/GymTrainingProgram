from fastapi import FastAPI
from Data_Base_SQL.database import engine
from Data_Base_SQL import models
from FastAPI_Funcions import users, exercises, workout


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers
app.include_router(users.app)
app.include_router(exercises.app)
app.include_router(workout.app)


@app.get("/")
def home():
    return {"message": "Gym API is running!"}
