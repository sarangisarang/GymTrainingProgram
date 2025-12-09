import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, DECIMAL, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from datetime import datetime


# -------------------- BENUTZER (USER) --------------------
class User(Base):
    __tablename__ = "users"

    # ID ist Integer (einfacher für den Anfang)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Spalten
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Beziehungen zu Workouts und Exercises
    workouts = relationship("Workout", back_populates="owner")
    exercises = relationship("Exercise", back_populates="owner")


# -------------------- ÜBUNG (EXERCISE) --------------------
class Exercise(Base):
    __tablename__ = "exercises"

    # ID ist Integer
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Spalten
    title = Column(String, index=True)
    muscle_group = Column(String)
    description = Column(String)

    # Fremdschlüssel zum User
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="exercises")

    # Beziehung zur Verbindungstabelle
    workouts_link = relationship("WorkoutExercise", back_populates="exercise")


# -------------------- TRAINING (WORKOUT) --------------------
class Workout(Base):
    __tablename__ = "workouts"

    # ID ist Integer
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Spalten
    title = Column(String, index=True)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Fremdschlüssel zum User
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="workouts")

    # Beziehung zur Verbindungstabelle
    exercises_link = relationship("WorkoutExercise", back_populates="workout")


# -------------------- VERKNÜPFUNGSTABELLE (WORKOUT_EXERCISES) --------------------
# Verbindungstabelle für Many-to-Many zwischen Workouts und Exercises
class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    # ID ist Integer
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Fremdschlüssel
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))

    # Zusätzliche Spalten für Training-Details
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(DECIMAL)

    # ORM-Beziehungen
    workout = relationship("Workout", back_populates="exercises_link")
    exercise = relationship("Exercise", back_populates="workouts_link")