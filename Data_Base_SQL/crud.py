from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from . import models, schemas


# ---------------- USER CRUD ----------------

def create_user(db: Session, user: schemas.UserCreate):
    """Erstellt einen neuen Benutzer."""
    db_user = models.User(
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Gibt alle Benutzer zurück mit ihren Workouts und Exercises."""
    return db.query(models.User) \
        .options(joinedload(models.User.workouts)) \
        .options(joinedload(models.User.exercises)) \
        .offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    """Gibt einen einzelnen Benutzer zurück."""
    return db.query(models.User) \
        .filter(models.User.id == user_id) \
        .options(joinedload(models.User.workouts)) \
        .options(joinedload(models.User.exercises)) \
        .first()


# ---------------- WORKOUT CRUD ----------------

def create_workout(db: Session, workout: schemas.WorkoutCreate):
    """Erstellt ein neues Workout."""
    db_workout = models.Workout(
        title=workout.title,
        description=workout.description,
        user_id=workout.user_id
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def get_workouts(db: Session, skip: int = 0, limit: int = 100):
    """Gibt alle Workouts zurück."""
    return db.query(models.Workout).offset(skip).limit(limit).all()


def get_workout_by_id(db: Session, workout_id: int):
    """Gibt ein einzelnes Workout zurück."""
    return db.query(models.Workout).filter(models.Workout.id == workout_id).first()


# ---------------- EXERCISE CRUD ----------------

def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    """Erstellt eine neue Übung."""
    db_ex = models.Exercise(
        title=exercise.title,
        muscle_group=exercise.muscle_group,
        user_id=exercise.user_id
    )
    db.add(db_ex)
    db.commit()
    db.refresh(db_ex)
    return db_ex


def get_exercises(db: Session, skip: int = 0, limit: int = 100):
    """Gibt alle Übungen zurück."""
    return db.query(models.Exercise).offset(skip).limit(limit).all()


def get_exercise_by_id(db: Session, exercise_id: int):
    """Gibt eine einzelne Übung zurück."""
    return db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()


def get_exercises_by_user(db: Session, user_id: int):
    """Gibt alle Übungen eines Benutzers zurück."""
    return db.query(models.Exercise).filter(models.Exercise.user_id == user_id).all()


def delete_exercise(db: Session, exercise_id: int):
    """Löscht eine Übung."""
    db_ex = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if db_ex:
        db.delete(db_ex)
        db.commit()


def update_exercise(db: Session, exercise_id: int, exercise: schemas.ExerciseCreate):
    """Aktualisiert eine Übung."""
    db_ex = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not db_ex:
        return None

    db_ex.title = exercise.title
    db_ex.muscle_group = exercise.muscle_group

    db.commit()
    db.refresh(db_ex)
    return db_ex


# ---------------- WORKOUT_EXERCISE CRUD ----------------

def create_workout_exercise(db: Session, item: schemas.WorkoutExerciseCreate):
    """Verbindet ein Workout mit einer Übung (mit Sets, Reps, Weight)."""
    db_workout_exercise = models.WorkoutExercise(
        workout_id=item.workout_id,
        exercise_id=item.exercise_id,
        sets=item.sets,
        reps=item.reps,
        weight=item.weight
    )
    db.add(db_workout_exercise)
    db.commit()
    db.refresh(db_workout_exercise)
    return db_workout_exercise