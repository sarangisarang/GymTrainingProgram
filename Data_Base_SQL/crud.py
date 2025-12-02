from sqlalchemy.orm import Session
from . import models, schemas


# -------------------- USER CRUD --------------------
def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.
    """
    db_user = models.User(
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    """
    Return all users.
    """
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    """
    Return a single user by ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


# -------------------- EXERCISE CRUD --------------------
def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    """
    Create a new exercise in the database.
    """
    db_ex = models.Exercise(
        title=exercise.title,
        muscle_group=exercise.muscle_group
    )
    db.add(db_ex)
    db.commit()
    db.refresh(db_ex)
    return db_ex


def get_exercises(db: Session):
    """
    Return all exercises.
    """
    return db.query(models.Exercise).all()


def get_exercise_by_id(db: Session, exercise_id: int):
    """
    Return a single exercise by ID.
    """
    return db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
