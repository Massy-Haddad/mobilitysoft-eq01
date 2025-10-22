# app/api/v1/endpoints.py
from fastapi import APIRouter, Request
import numpy as np
import math

from app.core.config import settings
from app.core.rate_limit import limiter
from app.models.schemas import EntreePrediction, SortiePrediction
from app.services.model import ModeleTrafic

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
async def predire(request: Request, entree: EntreePrediction):
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
    return SortiePrediction(risque=niveau, proba=round(p, 3), recommandations=recos)


@router.post("/reentrainer")
async def reentrainer(request: Request, seed: int | None = None):
    limiter.check(request)
    MODELE.reentrainer(seed or settings.MODEL_SEED)
    return {"ok": True}
