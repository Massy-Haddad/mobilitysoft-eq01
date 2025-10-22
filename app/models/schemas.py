# app/models/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field

class EntreePrediction(BaseModel):
    # Caractéristiques temporelles / conditions
    heure: int = Field(ge=0, le=23, description="Heure (0-23)")
    jour_semaine: int = Field(ge=0, le=6, description="0=Lun … 6=Dim")
    meteo: int = Field(ge=0, le=2, description="0=Clair, 1=Pluie, 2=Neige")
    incidents: int = Field(ge=0, le=1, description="Incident (0/1)")
    # Caractéristiques de trafic
    vitesse_moyenne: float = Field(gt=0, description="Vitesse moyenne (km/h)")
    debit_vehicules: float = Field(gt=0, description="Débit (véh./min)")
    # Géolocalisation (optionnel)
    lat_a: Optional[float] = Field(default=None, description="Latitude point A")
    lon_a: Optional[float] = Field(default=None, description="Longitude point A")
    lat_b: Optional[float] = Field(default=None, description="Latitude point B")
    lon_b: Optional[float] = Field(default=None, description="Longitude point B")
    distance_km: Optional[float] = Field(default=None, description="Distance A–B (km)")

class SortiePrediction(BaseModel):
    risque: str
    proba: float
    recommandations: List[str]
