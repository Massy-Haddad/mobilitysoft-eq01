# app/services/model.py
import numpy as np
from typing import Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from threading import Lock

class ModeleTrafic:
    def __init__(self, seed: int = 42):
        self.lock = Lock()
        self.pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=200)),
        ])
        self.reentrainer(seed)

    def generer(self, n=3000, seed=42) -> Tuple[np.ndarray, np.ndarray]:
        rng = np.random.default_rng(seed)
        heure = rng.integers(0, 24, size=n)
        jour = rng.integers(0, 7, size=n)
        meteo = rng.integers(0, 3, size=n)
        incidents = rng.integers(0, 2, size=n)

        is_pointe = ((7 <= heure) & (heure <= 9)) | ((16 <= heure) & (heure <= 18))
        debit = rng.normal(20 + 30*is_pointe + 10*(meteo>0) + 25*incidents, 5, size=n).clip(5, 120)
        vitesse = rng.normal(60 - 20*is_pointe - 10*(meteo>0) - 25*incidents, 8, size=n).clip(5, 130)

        # Distance simulée (km), corrélée faiblement aux conditions
        distance = rng.gamma(shape=2.0, scale=2.0, size=n).clip(0.1, 50.0)  # 0.1 à 50 km

        # Score logistique synthétique (parenthèses corrigées)
        z = (
            0.08*debit
            - 0.04*vitesse
            + 0.6*incidents
            + 0.3*(meteo==1)
            + 0.6*(meteo==2)
            + 0.15*((jour>=1)&(jour<=5))
            + 0.25*is_pointe
            + 0.02*np.maximum(distance-3.0, 0.0)  # distances plus longues => léger sur-risque
        )
        proba = 1/(1+np.exp(-z))
        y = (proba > 0.5).astype(int)
        X = np.column_stack([heure, jour, meteo, incidents, vitesse, debit, distance])
        return X, y

    def reentrainer(self, seed: int = 42):
        X, y = self.generer(seed=seed)
        with self.lock:
            self.pipe.fit(X, y)

    def predire(self, X: np.ndarray):
        with self.lock:
            proba = self.pipe.predict_proba(X)[:, 1]
        y = (proba >= 0.5).astype(int)
        return y, proba
