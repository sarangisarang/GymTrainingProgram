from sqlalchemy import Column, Integer, String, ForeignKey, DateTime # Fügen Sie HIER 'DateTime' hinzu
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from fastapi import APIRouter

router = APIRouter()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    exercises = relationship("Exercise", back_populates="owner")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    muscle_group = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="exercises")

class Workout(Base):
    __tablename__ = "workouts"  # Der Name der Datenbanktabelle

    id = Column(Integer, primary_key=True, index=True)  # Eindeutige ID (Schlüssel)
    title = Column(String, index=True, nullable=False)  # Titel des Trainings, muss ausgefüllt werden
    description = Column(String)  # Beschreibung des Trainings
    created_at = Column(DateTime, default=datetime.utcnow)  # Wann wurde es erstellt?

    # Beziehung: Ein Workout hat viele WorkoutExercises
    exercises = relationship("WorkoutExercise", back_populates="workout")

