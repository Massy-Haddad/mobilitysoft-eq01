"""
Tests pour les fonctions utilitaires
"""
# pylint: disable=import-outside-toplevel,import-error
import pytest


@pytest.mark.unit
def test_haversine_distance():
    """Test de la fonction de calcul de distance haversine"""
    from app.api.v1.endpoints import haversine_km

    # Distance entre deux points à Montréal
    # Point A: 45.5017, -73.5673
    # Point B: 45.5088, -73.5540
    distance = haversine_km(45.5017, -73.5673, 45.5088, -73.5540)

    # La distance devrait être d'environ 1.2 km
    assert 1.0 < distance < 1.5


@pytest.mark.unit
def test_haversine_meme_point():
    """Test de la distance haversine entre un point et lui-même"""
    from app.api.v1.endpoints import haversine_km

    distance = haversine_km(45.5017, -73.5673, 45.5017, -73.5673)
    assert distance == pytest.approx(0.0, abs=0.001)


@pytest.mark.unit
def test_haversine_grande_distance():
    """Test de la distance haversine pour une grande distance"""
    from app.api.v1.endpoints import haversine_km

    # Distance entre Montréal et Paris
    # Montréal: 45.5017, -73.5673
    # Paris: 48.8566, 2.3522
    distance = haversine_km(45.5017, -73.5673, 48.8566, 2.3522)

    # La distance devrait être d'environ 5500 km
    assert 5400 < distance < 5600


@pytest.mark.unit
def test_recommandations_risque_eleve():
    """Test des recommandations pour un risque élevé"""
    from app.api.v1.endpoints import recommandations
    from app.models.schemas import EntreePrediction

    entree = EntreePrediction(
        heure=17,
        jour_semaine=4,
        meteo=1,
        incidents=1,
        vitesse_moyenne=40.0,
        debit_vehicules=80.0,
        distance_km=15.0,
    )

    recs = recommandations(entree, proba=0.8, y=1)
    assert isinstance(recs, list)
    assert len(recs) > 0
    # Devrait contenir des recommandations pour risque élevé
    assert any("vitesse" in rec.lower() or "distance" in rec.lower() for rec in recs)


@pytest.mark.unit
def test_recommandations_risque_faible():
    """Test des recommandations pour un risque faible"""
    from app.api.v1.endpoints import recommandations
    from app.models.schemas import EntreePrediction

    entree = EntreePrediction(
        heure=10,
        jour_semaine=2,
        meteo=0,
        incidents=0,
        vitesse_moyenne=70.0,
        debit_vehicules=40.0,
        distance_km=5.0,
    )

    recs = recommandations(entree, proba=0.2, y=0)
    assert isinstance(recs, list)
    assert len(recs) > 0


@pytest.mark.unit
def test_recommandations_heure_pointe():
    """Test que les recommandations mentionnent l'heure de pointe"""
    from app.api.v1.endpoints import recommandations
    from app.models.schemas import EntreePrediction

    entree = EntreePrediction(
        heure=8,  # Heure de pointe
        jour_semaine=2,
        meteo=0,
        incidents=0,
        vitesse_moyenne=60.0,
        debit_vehicules=50.0,
        distance_km=10.0,
    )

    recs = recommandations(entree, proba=0.3, y=0)
    assert any("pointe" in rec.lower() for rec in recs)
