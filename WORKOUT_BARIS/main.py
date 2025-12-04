# main.py

from fastapi import FastAPI
import database
from . import workouts

# Erstellt alle Tabellen in der Datenbank, falls sie noch nicht existieren
database.Base.metadata.create_all(bind=database.engine) 

app = FastAPI()

# Fügt unseren Router (die Endpunkte aus workouts.py) zur Haupt-App hinzu
app.include_router(workouts.router)

# Der einfachste Endpunkt (Startseite)
@app.get("/")
def read_root():
    return {"message": "Willkommen bei der Workouts API"}