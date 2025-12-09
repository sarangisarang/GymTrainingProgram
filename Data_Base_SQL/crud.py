from uuid import UUID
from sqlalchemy.orm import Session
from Data_Base_SQL import models, schemas
from Data_Base_SQL.models import Workout
from Data_Base_SQL.schemas import WorkoutCreate


# ---------------- USER CRUD ----------------

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------------- EXERCISE CRUD ----------------

def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    db_ex = models.Exercise(
        title=exercise.title,
        muscle_group=exercise.muscle_group
    )
    db.add(db_ex)
    db.commit()
    db.refresh(db_ex)
    return db_ex


def get_exercises(db: Session):
    return db.query(models.Exercise).all()


def get_exercise_by_id(db: Session, exercise_id: UUID):
    return db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()


def create_exercise_for_user(db: Session, user_id: UUID, exercise: schemas.ExerciseCreate):
    db_ex = models.Exercise(
        title=exercise.title,
        muscle_group=exercise.muscle_group,
        user_id=user_id
    )
    db.add(db_ex)
    db.commit()
    db.refresh(db_ex)
    return db_ex


def get_exercises_by_user(db: Session, user_id: UUID):
    return db.query(models.Exercise).filter(models.Exercise.user_id == user_id).all()


def delete_exercise(db: Session, exercise_id: UUID):
    db_ex = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if db_ex:
        db.delete(db_ex)
        db.commit()


def update_exercise(db: Session, exercise_id: UUID, exercise: schemas.ExerciseCreate):
    db_ex = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not db_ex:
        return None

    db_ex.title = exercise.title
    db_ex.muscle_group = exercise.muscle_group

    db.commit()
    db.refresh(db_ex)
    return db_ex


# ---------------- WORKOUT CRUD ----------------

def create_workout(db: Session, data: WorkoutCreate):
    workout = Workout(
        user_id=data.user_id,
        date=data.date,
        notes=data.notes
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout
