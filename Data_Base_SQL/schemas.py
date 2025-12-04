from pydantic import BaseModel, ConfigDict


# ---------------- USER ----------------
class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------- EXERCISE ----------------
class ExerciseBase(BaseModel):
    title: str
    muscle_group: str


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(BaseModel):
    id: int
    title: str
    muscle_group: str
    user_id: int | None

    class Config:
        orm_mode = True

