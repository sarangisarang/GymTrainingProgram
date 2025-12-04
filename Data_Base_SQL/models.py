from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """
    Repräsentiert einen Benutzer im System.
    Jeder Benutzer kann mehrere Übungen besitzen (One-to-Many-Beziehung).
    """

    __tablename__ = "users"

    # Primärschlüssel des Benutzers
    id = Column(Integer, primary_key=True)

    # Name des Benutzers
    name = Column(String)

    # E-Mail-Adresse des Benutzers
    email = Column(String)

    # Beziehung zu den Übungen des Benutzers
    # back_populates verknüpft diese Beziehung mit Exercise.owner
    exercises = relationship("Exercise", back_populates="owner")


class Exercise(Base):
    """
    Repräsentiert eine Übung im System.
    Eine Übung gehört genau einem Benutzer (Many-to-One-Beziehung).
    """

    __tablename__ = "exercises"

    # Primärschlüssel der Übung
    id = Column(Integer, primary_key=True, index=True)

    # Titel oder Name der Übung (z. B. "Bankdrücken")
    title = Column(String)

    # Zugehörige Muskelgruppe (z. B. "Brust")
    muscle_group = Column(String)

    # Fremdschlüssel, der auf den Besitzer der Übung verweist
    user_id = Column(Integer, ForeignKey("users.id"))

    # Beziehung zum Benutzer (Besitzer der Übung)
    owner = relationship("User", back_populates="exercises")
