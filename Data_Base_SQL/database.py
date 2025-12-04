from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------
# Datenbankkonfiguration (SQLite)
# ---------------------------------------------------------

# SQLite-Verbindungs-URL (lokale Datei: gym.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./gym.db"

# Erstellen der Engine
# Für SQLite muss 'check_same_thread' deaktiviert werden,
# da mehrere Threads gleichzeitig auf dieselbe Verbindung zugreifen können.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Erstellen einer SessionFactory:
# autocommit=False  → Änderungen werden erst nach commit() gespeichert
# autoflush=False   → verhindert automatisches Zwischenspeichern
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basisklasse für alle ORM-Modelle
Base = declarative_base()


# ---------------------------------------------------------
# Abhängigkeitsfunktion für FastAPI
# ---------------------------------------------------------
def get_db():
    """
    Liefert eine neue Datenbank-Session zurück.
    Diese Funktion wird als Dependency in FastAPI-Routen genutzt.
    Nach jeder Anfrage wird die Session automatisch geschlossen.

    Beispiel:
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
