from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# -------------------- BENUTZER (USER) --------------------
class UserBase(BaseModel):
    """Basis-Schema für User mit gemeinsamen Feldern."""
    name: str
    email: str


class UserCreate(UserBase):
    """Schema für das Erstellen eines neuen Users."""
    pass


class UserRead(UserBase):
    """Schema für das Lesen eines Users aus der DB."""
    id: int
    # Beziehungen: Exercises und Workouts des Users
    exercises: List['ExerciseRead'] = []
    workouts: List['WorkoutRead'] = []

    model_config = ConfigDict(from_attributes=True)


# -------------------- ÜBUNG (EXERCISE) --------------------
class ExerciseBase(BaseModel):
    """Basis-Schema für Exercise mit gemeinsamen Feldern."""
    title: str
    muscle_group: str
    description: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    """Schema für das Erstellen einer neuen Exercise."""
    user_id: int  # Wem gehört diese Übung?


class ExerciseRead(ExerciseBase):
    """Schema für das Lesen einer Exercise aus der DB."""
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------- TRAINING (WORKOUT) --------------------
class WorkoutBase(BaseModel):
    """Basis-Schema für Workout mit gemeinsamen Feldern."""
    title: str
    description: Optional[str] = None
    user_id: int  # Wem gehört dieses Workout?


class WorkoutCreate(WorkoutBase):
    """Schema für das Erstellen eines neuen Workouts."""
    # Optional: Liste von Übungen direkt beim Erstellen übergeben
    exercises: Optional[List['WorkoutExerciseBase']] = None


class WorkoutRead(WorkoutBase):
    """Schema für das Lesen eines Workouts aus der DB."""
    id: int
    date: datetime
    created_at: datetime
    # Liste der verknüpften Übungen
    exercises_link: List['WorkoutExerciseRead'] = []

    model_config = ConfigDict(from_attributes=True)


# -------------------- VERKNÜPFUNGSTABELLE (WORKOUT_EXERCISE) --------------------
class WorkoutExerciseBase(BaseModel):
    """Basis-Schema für die Verknüpfung zwischen Workout und Exercise."""
    exercise_id: int
    sets: int
    reps: int
    weight: float


class WorkoutExerciseCreate(BaseModel):
    """Schema für das Erstellen einer neuen Workout-Exercise-Verknüpfung."""
    workout_id: int
    exercise_id: int
    sets: int
    reps: int
    weight: float


class WorkoutExerciseRead(WorkoutExerciseBase):
    """Schema für das Lesen einer Workout-Exercise-Verknüpfung aus der DB."""
    id: int
    workout_id: int
    # Referenz zur verknüpften Exercise
    exercise: Optional[ExerciseRead] = None

    model_config = ConfigDict(from_attributes=True)


# WICHTIG: Forward references auflösen (wegen zirkulärer Abhängigkeiten)
UserRead.model_rebuild()
WorkoutRead.model_rebuild()
WorkoutExerciseRead.model_rebuild()