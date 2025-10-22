from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Importer la configuration
from app.core.config import settings
import os

# Obtenir l'URL de la base de données depuis les paramètres
DATABASE_URL = settings.DATABASE_URL
print(f"INFO: Connexion à la base de données : {DATABASE_URL}")

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer la base déclarative pour les modèles SQLAlchemy
Base = declarative_base()

# Modèle pour stocker les prédictions
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    lat_depart = Column(Float)
    lon_depart = Column(Float)
    lat_arrivee = Column(Float)
    lon_arrivee = Column(Float)
    distance_km = Column(Float)
    heure = Column(Integer)
    jour_semaine = Column(String)
    meteo = Column(String)
    incidents = Column(Integer)
    vitesse_moyenne = Column(Float)
    debit_vehicules = Column(Integer)
    vitesse_prevue = Column(Float)
    temps_trajet_prevu = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)

# Fonction pour initialiser la base de données (création des tables)
def init_db():
    Base.metadata.create_all(bind=engine)

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()