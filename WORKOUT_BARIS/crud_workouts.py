# crud_workouts.py

from sqlalchemy.orm import Session
from . import models_workouts, schemas_workouts
from typing import List

# CRUD = Create, Read, Update, Delete

# --- Workout CRUD Funktionen ---

def create_workout(db: Session, workout: schemas_workouts.WorkoutCreate):
    # Erstellt ein neues Workout in der Datenbank
    db_workout = models_workouts.Workout(**workout.dict())
    db.add(db_workout) # Fügt es zur Session hinzu
    db.commit() # Speichert es in der Datenbank
    db.refresh(db_workout) # Holt die DB-Daten (inkl. ID) zurück
    return db_workout

def get_workout(db: Session, workout_id: int):
    # Liest ein einzelnes Workout anhand der ID
    return db.query(models_workouts.Workout).filter(models_workouts.Workout.id == workout_id).first()

def list_workouts(db: Session, skip: int = 0, limit: int = 100) -> List[models_workouts.Workout]:
    # Liest eine Liste aller Workouts (mit Paginierung/Grenzen)
    return db.query(models_workouts.Workout).offset(skip).limit(limit).all()

def delete_workout(db: Session, workout_id: int):
    # Löscht ein Workout anhand der ID
    db_workout = get_workout(db, workout_id=workout_id) # Zuerst suchen
    if db_workout:
        db.delete(db_workout) # Löscht es
        db.commit() # Speichert die Änderung
        return db_workout
    return None # Falls nicht gefunden

# --- WorkoutExercise CRUD Funktionen ---

def create_workout_exercise(db: Session, exercise: schemas_workouts.WorkoutExerciseCreate, workout_id: int):
    # Erstellt eine neue Übung für ein bestimmtes Workout
    db_exercise = models_workouts.WorkoutExercise(**exercise.dict(), workout_id=workout_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def get_workout_exercises(db: Session, workout_id: int) -> List[models_workouts.WorkoutExercise]:
    # Liest alle Übungen, die zu einer bestimmten Workout-ID gehören
    return db.query(models_workouts.WorkoutExercise).filter(models_workouts.WorkoutExercise.workout_id == workout_id).all()

def delete_workout_exercise(db: Session, exercise_id: int):
    # Löscht eine einzelne Übung anhand ihrer eigenen ID
    db_exercise = db.query(models_workouts.WorkoutExercise).filter(models_workouts.WorkoutExercise.id == exercise_id).first()
    if db_exercise:
        db.delete(db_exercise)
        db.commit()
        return db_exercise
    return None