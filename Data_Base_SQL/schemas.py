from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from uuid import UUID

# ---------------- USER ----------------
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


# ---------------- EXERCISE ----------------
class ExerciseBase(BaseModel):
    title: str
    muscle_group: str

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseRead(BaseModel):
    id: UUID
    title: str
    muscle_group: str
    user_id: UUID | None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


# ---------------- WORKOUT ----------------
class WorkoutCreate(BaseModel):
    user_id: UUID
    date: date
    notes: Optional[str]

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class WorkoutRead(BaseModel):
    id: UUID
    user_id: UUID
    date: datetime
    notes: Optional[str]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )
