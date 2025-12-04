from sqlalchemy.orm import Session
from Data_Base_SQL import models, schemas


# ---------------------------------------------------------
# BENUTZER-CRUD-FUNKTIONEN
# ---------------------------------------------------------

def create_user(db: Session, user: schemas.UserCreate):
    """
    Erstellt einen neuen Benutzer in der Datenbank.

    Parameter:
        db (Session): Aktive Datenbank-Session.
        user (UserCreate): Eingabedaten für den neuen Benutzer.

    Rückgabe:
        User: Das neu erstellte Benutzerobjekt.
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
    Gibt eine Liste aller Benutzer zurück.

    Rückgabe:
        List[User]: Alle registrierten Benutzer.
    """
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    """
    Gibt einen einzelnen Benutzer anhand seiner ID zurück.

    Parameter:
        user_id (int): Eindeutige ID des Benutzers.

    Rückgabe:
        User | None: Der gefundene Benutzer oder None, falls nicht vorhanden.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------------------------------------------------------
# ÜBUNGS-CRUD-FUNKTIONEN
# ---------------------------------------------------------

def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    """
    Erstellt eine neue Übung ohne Benutzerzuordnung.

    Parameter:
        exercise (ExerciseCreate): Titel und Muskelgruppe der Übung.

    Rückgabe:
        Exercise: Die neu erstellte Übung.
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
    Gibt alle vorhandenen Übungen zurück.

    Rückgabe:
        List[Exercise]: Liste aller Übungen im System.
    """
    return db.query(models.Exercise).all()


def get_exercise_by_id(db: Session, exercise_id: int):
    """
    Gibt eine Übung anhand ihrer ID zurück.

    Parameter:
        exercise_id (int): Eindeutige ID der Übung.

    Rückgabe:
        Exercise | None
    """
    return db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()


def create_exercise_for_user(db: Session, user_id: int, exercise: schemas.ExerciseCreate):
    """
    Erstellt eine neue Übung und ordnet sie einem bestimmten Benutzer zu.

    Parameter:
        user_id (int): ID des Benutzers.
        exercise (ExerciseCreate): Übungsdaten.

    Rückgabe:
        Exercise: Die erstellte Übung mit Benutzerzuordnung.
    """
    db_ex = models.Exercise(
        title=exercise.title,
        muscle_group=exercise.muscle_group,
        user_id=user_id
    )
    db.add(db_ex)
    db.commit()
    db.refresh(db_ex)
    return db_ex


def get_exercises_by_user(db: Session, user_id: int):
    """
    Gibt alle Übungen zurück, die zu einem bestimmten Benutzer gehören.

    Parameter:
        user_id (int): ID des Benutzers.

    Rückgabe:
        List[Exercise]
    """
    return db.query(models.Exercise).filter(models.Exercise.user_id == user_id).all()


def delete_exercise(db: Session, exercise_id: int):
    """
    Löscht eine Übung aus der Datenbank.

    Parameter:
        exercise_id (int): ID der zu löschenden Übung.

    Rückgabe:
        None
    """
    db_ex = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if db_ex:
        db.delete(db_ex)
        db.commit()


def update_exercise(db: Session, exercise_id: int, exercise: schemas.ExerciseCreate):
    """
    Aktualisiert eine bestehende Übung.

    Parameter:
        exercise_id (int): ID der zu aktualisierenden Übung.
        exercise (ExerciseCreate): Neue Übungsdaten.

    Rückgabe:
        Exercise | None: Die aktualisierte Übung oder None, falls sie nicht existiert.
    """
    db_ex = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not db_ex:
        return None

    db_ex.title = exercise.title
    db_ex.muscle_group = exercise.muscle_group

    db.commit()
    db.refresh(db_ex)
    return db_ex
