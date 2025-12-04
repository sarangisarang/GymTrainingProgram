# models_workouts.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base # 'Base' ist die Basis für unsere Datenbank-Modelle

# --- Das Workout-Modell (Die Haupt-Tabelle für alle Trainingspläne) ---
class Workout(Base):
    __tablename__ = "workouts" # Der Name der Datenbanktabelle

    id = Column(Integer, primary_key=True, index=True) # Eindeutige ID (Schlüssel)
    title = Column(String, index=True, nullable=False) # Titel des Trainings, muss ausgefüllt werden
    description = Column(String) # Beschreibung des Trainings
    created_at = Column(DateTime, default=datetime.utcnow) # Wann wurde es erstellt?
    
    # Beziehung: Ein Workout hat viele WorkoutExercises
    exercises = relationship("WorkoutExercise", back_populates="workout")

# --- Das WorkoutExercise-Modell (Die Tabelle für die einzelnen Übungen im Training) ---
class WorkoutExercise(Base):
    __tablename__ = "workout_exercises" # Der Name der Datenbanktabelle

    id = Column(Integer, primary_key=True, index=True)
    # Fremdschlüssel: Verknüpft diese Übung mit der Workout-Tabelle
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    
    exercise_name = Column(String, nullable=False) # Name der Übung (z.B. "Liegestütze")
    sets = Column(Integer) # Anzahl der Sätze
    reps = Column(Integer) # Anzahl der Wiederholungen
    weight = Column(Integer) # Verwendetes Gewicht (optional)
    
    # Beziehung: Diese Übung gehört zu einem bestimmten Workout
    workout = relationship("Workout", back_populates="exercises")