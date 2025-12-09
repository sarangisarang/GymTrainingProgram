from fastapi import FastAPI
from Data_Base_SQL.database import engine, Base
from Data_Base_SQL import models
from FastAPI_Functions import users, exercises, workout, workout_exercises

# Erstellt alle Datenbanktabellen basierend auf den Models
models.Base.metadata.create_all(bind=engine)

# Initialisiert die FastAPI-App
app = FastAPI(
    title="TEAM3 Gym API",
    description="API für Gym-Management mit Users, Exercises und Workouts",
    version="1.0.0"
)

# Registriert alle Router (Endpoints) für die API
# Prefix wird NICHT hier hinzugefügt, weil es bereits in den Router-Dateien definiert ist!
app.include_router(users.router)
app.include_router(exercises.router)
app.include_router(workout.router)
app.include_router(workout_exercises.router)


@app.get("/", tags=["Root"])
def home():
    """
    Root-Endpoint: Bestätigt, dass die API läuft.
    """
    return {
        "message": "TEAM3 - Gym API is running! 🏋️",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "exercises": "/exercises",
            "workouts": "/workouts",
            "workout_exercises": "/workout-exercises",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health-Check Endpoint für Monitoring.
    """
    return {"status": "healthy", "database": "connected"}