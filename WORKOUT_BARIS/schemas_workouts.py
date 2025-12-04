# schemas_workouts.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Pydantic Schemas definieren, welche Daten wir erwarten oder senden

# --- Schemas für einzelne Übungen (WorkoutExercise) ---
class WorkoutExerciseBase(BaseModel):
    # Basisdaten für eine Übung
    exercise_name: str
    sets: int
    reps: int
    weight: Optional[int] = None # 'Optional' bedeutet, das Feld ist nicht zwingend erforderlich

class WorkoutExerciseCreate(WorkoutExerciseBase):
    # Wird verwendet, wenn wir eine NEUE Übung erstellen. Hier reichen die Basisdaten.
    pass

class WorkoutExerciseRead(WorkoutExerciseBase):
    # Wird verwendet, wenn wir eine Übung aus der DB LESEN und anzeigen
    id: int # Wir zeigen die ID an
    workout_id: int # Wir zeigen an, zu welchem Workout die Übung gehört

    class Config:
        # Erlaubt Pydantic, Daten direkt vom SQLAlchemy ORM-Modell zu lesen
        from_attributes = True

# --- Schemas für das gesamte Training (Workout) ---
class WorkoutBase(BaseModel):
    # Basisdaten für ein Training
    title: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    # Wird verwendet, wenn wir ein NEUES Training erstellen
    pass

class WorkoutRead(WorkoutBase):
    # Wird verwendet, wenn wir ein Training aus der DB LESEN und anzeigen
    id: int
    created_at: datetime
    # Listet alle zugehörigen Übungen auf (Liste von WorkoutExerciseRead)
    exercises: List[WorkoutExerciseRead] = [] 

    class Config:
        from_attributes = True
        