from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite Datenbank URL (lokale Datei)
SQLALCHEMY_DATABASE_URL = "sqlite:///./gym.db"

# Engine erstellen
# check_same_thread=False ist nötig für SQLite mit FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session erstellen
# autocommit=False bedeutet: ich muss selber commit() aufrufen
# autoflush=False bedeutet: keine automatische Synchronisation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basis-Klasse für alle Modelle
Base = declarative_base()


# Dependency für FastAPI
def get_db():
    """
    Diese Funktion gibt eine Datenbank-Session zurück.
    Sie wird in FastAPI mit Depends() benutzt.
    Die Session wird am Ende automatisch geschlossen.

    Beispiel:
        def meine_route(db: Session = Depends(get_db)):
            # hier kann ich mit db arbeiten
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()