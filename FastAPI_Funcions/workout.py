from fastapi import APIRouter
from Class_Funcions.Workout_Generator import WorkoutGenerator

app = APIRouter(prefix="/workout", tags=["Workout"])

@app.get("/{days}")
def generate_workout(days: int):
    generator = WorkoutGenerator()
    return generator.generate_plan(days)
