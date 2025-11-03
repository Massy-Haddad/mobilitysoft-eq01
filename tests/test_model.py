"""
Tests pour le modèle de prédiction de trafic
"""
# pylint: disable=import-error
import numpy as np
import pytest

from app.services.model import ModeleTrafic


@pytest.mark.unit
def test_modele_creation():
    """Test de la création du modèle"""
    modele = ModeleTrafic(seed=42)
    assert modele is not None


@pytest.mark.unit
def test_modele_prediction_shape():
    """Test que la prédiction retourne la forme correcte"""
    modele = ModeleTrafic(seed=42)
    X = np.array([[8, 1, 0, 0, 60.0, 50.0, 10.0]])
    y, proba = modele.predire(X)
    assert y.shape == (1,)
    assert proba.shape == (1,)


@pytest.mark.unit
def test_modele_prediction_values():
    """Test que la prédiction retourne des valeurs valides"""
    modele = ModeleTrafic(seed=42)
    X = np.array([[8, 1, 0, 0, 60.0, 50.0, 10.0]])
    y, proba = modele.predire(X)
    assert y[0] in [0, 1]  # Binaire
    assert 0.0 <= proba[0] <= 1.0  # Probabilité entre 0 et 1


@pytest.mark.unit
def test_modele_reentrainement():
    """Test du ré-entraînement du modèle"""
    modele = ModeleTrafic(seed=42)
    # Faire une prédiction initiale
    X = np.array([[8, 1, 0, 0, 60.0, 50.0, 10.0]])
    _, _ = modele.predire(X)

    # Ré-entraîner avec un seed différent
    modele.reentrainer(seed=123)
    y2, proba2 = modele.predire(X)

    # Les résultats peuvent être différents (ou non) selon le modèle
    # On vérifie juste que le ré-entraînement ne cause pas d'erreur
    assert y2[0] in [0, 1]
    assert 0.0 <= proba2[0] <= 1.0


@pytest.mark.unit
def test_modele_predictions_multiples():
    """Test de prédictions multiples"""
    modele = ModeleTrafic(seed=42)
    X = np.array(
        [
            [8, 1, 0, 0, 60.0, 50.0, 10.0],
            [17, 4, 1, 1, 40.0, 80.0, 15.0],
            [12, 6, 0, 0, 80.0, 30.0, 5.0],
        ]
    )
    y, proba = modele.predire(X)
    assert y.shape == (3,)
    assert proba.shape == (3,)
    assert all(yi in [0, 1] for yi in y)
    assert all(0.0 <= p <= 1.0 for p in proba)
