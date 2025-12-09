from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# ---------------- BENUTZER (USER) ----------------
class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------- ÜBUNG (EXERCISE) ----------------
class ExerciseBase(BaseModel):
    title: str
    muscle_group: str


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------- TRAINING (WORKOUT) ----------------
class WorkoutBase(BaseModel):
    title: str
    # Das Beschreibungsfeld ist optional (kein Muss!), also mit Optional[str]
    description: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    # Falls beim Erstellen des Workouts noch andere Daten nötig sind, kommen sie hier rein
    pass


class WorkoutRead(WorkoutBase):
    # Das sind die Felder, die wir brauchen, wenn wir die Daten aus der Datenbank lesen
    id: int
    # created_at muss als der richtige Python-Typ (datetime) definiert werden
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)