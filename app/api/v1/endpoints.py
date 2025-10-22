# app/api/v1/endpoints.py
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import numpy as np
import math
from typing import List, Optional
from datetime import datetime

from app.core.config import settings
from app.core.rate_limit import limiter
from app.models.schemas import EntreePrediction, SortiePrediction
from app.services.model import ModeleTrafic
from app.database import get_db, Prediction

router = APIRouter(prefix=settings.API_V1_STR, tags=["Prédiction de trafic"])

MODELE = ModeleTrafic(seed=settings.MODEL_SEED)


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def recommandations(e: EntreePrediction, proba: float, y: int):
    rec = []
    if y == 1 or proba >= 0.6:
        rec.append("Réduire la vitesse et augmenter la distance de sécurité.")
        rec.append("Privilégier un itinéraire alternatif si possible.")
        if e.incidents == 1:
            rec.append("Éviter la zone d’incident signalée (contournement recommandé).")
        if e.meteo == 1:
            rec.append("Pluie : allonger les distances de freinage.")
        if e.meteo == 2:
            rec.append("Neige : conduite prudente, éviter les manœuvres brusques.")
    else:
        rec.append("Circulation fluide : maintenir une conduite défensive.")
    if e.heure in [7, 8, 9, 16, 17, 18]:
        rec.append("Heure de pointe : attention aux ralentissements soudains.")
    if e.distance_km and e.distance_km > 10:
        rec.append("Trajet long : planifier une pause si nécessaire.")
    return rec


@router.get("/sante")
async def sante(request: Request):
    limiter.check(request)
    return {"ok": True, "nom": settings.APP_NAME}


@router.post("/predire", response_model=SortiePrediction)
async def predire(request: Request, entree: EntreePrediction, db: Session = Depends(get_db)):
    limiter.check(request)
    # Calcul distance si non fournie mais lat/lon présents
    dist = entree.distance_km
    if dist is None and all(v is not None for v in [entree.lat_a, entree.lon_a, entree.lat_b, entree.lon_b]):
        try:
            dist = haversine_km(entree.lat_a, entree.lon_a, entree.lat_b, entree.lon_b)
        except Exception:
            dist = 0.0
    if dist is None:
        dist = 0.0

    X = np.array([[
        float(entree.heure),
        float(entree.jour_semaine),
        float(entree.meteo),
        float(entree.incidents),
        float(entree.vitesse_moyenne),
        float(entree.debit_vehicules),
        float(dist),
    ]], dtype=float)

    y, proba = MODELE.predire(X)
    p = float(proba[0])
    niveau = "élevé" if y[0] == 1 else "faible"
    recos = recommandations(entree, p, y[0])
    
    # Sauvegarder les données de prédiction dans la base de données
    vitesse_prevue = entree.vitesse_moyenne * (1.0 - 0.2 * float(y[0]))  # Estimation simple
    temps_trajet = dist / vitesse_prevue * 60 if vitesse_prevue > 0 else 0  # minutes
    
    nouvelle_prediction = Prediction(
        lat_depart=entree.lat_a,
        lon_depart=entree.lon_a,
        lat_arrivee=entree.lat_b,
        lon_arrivee=entree.lon_b,
        distance_km=dist,
        heure=entree.heure,
        jour_semaine=entree.jour_semaine,
        meteo=entree.meteo,
        incidents=entree.incidents,
        vitesse_moyenne=entree.vitesse_moyenne,
        debit_vehicules=entree.debit_vehicules,
        vitesse_prevue=vitesse_prevue,
        temps_trajet_prevu=temps_trajet,
        timestamp=datetime.now()
    )
    
    db.add(nouvelle_prediction)
    db.commit()
    
    return SortiePrediction(risque=niveau, proba=round(p, 3), recommandations=recos)


@router.post("/reentrainer")
async def reentrainer(request: Request, seed: int | None = None):
    limiter.check(request)
    MODELE.reentrainer(seed or settings.MODEL_SEED)
    return {"ok": True}


# Modèle Pydantic pour la sortie des prédictions stockées
from pydantic import BaseModel

class PredictionOutput(BaseModel):
    id: int
    lat_depart: Optional[float]
    lon_depart: Optional[float]
    lat_arrivee: Optional[float]
    lon_arrivee: Optional[float]
    distance_km: float
    heure: int
    jour_semaine: int
    meteo: int
    incidents: int
    vitesse_moyenne: float
    debit_vehicules: float
    vitesse_prevue: float
    temps_trajet_prevu: float
    timestamp: datetime
    
    class Config:
        orm_mode = True


@router.get("/predictions", response_model=List[PredictionOutput])
async def lire_predictions(
    request: Request,
    skip: int = 0, 
    limit: int = 100,
    date_debut: Optional[datetime] = None,
    date_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère les prédictions sauvegardées dans la base de données.
    Les résultats peuvent être filtrés par date.
    """
    limiter.check(request)
    query = db.query(Prediction)
    
    if date_debut:
        query = query.filter(Prediction.timestamp >= date_debut)
    
    if date_fin:
        query = query.filter(Prediction.timestamp <= date_fin)
    
    return query.order_by(Prediction.timestamp.desc()).offset(skip).limit(limit).all()


@router.get("/predictions/{prediction_id}", response_model=PredictionOutput)
async def lire_prediction(
    request: Request,
    prediction_id: int, 
    db: Session = Depends(get_db)
):
    """
    Récupère une prédiction spécifique par son ID.
    """
    limiter.check(request)
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    return prediction
