"""
Tests pour l'API de consultation des prédictions stockées
"""
# pylint: disable=import-error
from datetime import datetime
import pytest

from app.database import Prediction


@pytest.mark.integration
def test_lire_predictions_vide(client):
    """Test de récupération des prédictions quand la base est vide"""
    response = client.get("/api/v1/predictions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.integration
def test_lire_predictions_avec_donnees(client, db_session):
    """Test de récupération des prédictions avec des données"""
    # Ajouter des prédictions de test
    prediction1 = Prediction(
        lat_depart=45.5017,
        lon_depart=-73.5673,
        lat_arrivee=45.5088,
        lon_arrivee=-73.5540,
        distance_km=10.5,
        heure=8,
        jour_semaine=1,
        meteo=0,
        incidents=0,
        vitesse_moyenne=60.0,
        debit_vehicules=50.0,
        vitesse_prevue=55.0,
        temps_trajet_prevu=11.45,
        timestamp=datetime.now(),
    )
    prediction2 = Prediction(
        lat_depart=45.5088,
        lon_depart=-73.5540,
        lat_arrivee=45.5017,
        lon_arrivee=-73.5673,
        distance_km=10.5,
        heure=17,
        jour_semaine=1,
        meteo=1,
        incidents=1,
        vitesse_moyenne=40.0,
        debit_vehicules=80.0,
        vitesse_prevue=32.0,
        temps_trajet_prevu=19.69,
        timestamp=datetime.now(),
    )
    db_session.add(prediction1)
    db_session.add(prediction2)
    db_session.commit()

    response = client.get("/api/v1/predictions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.integration
def test_lire_predictions_avec_pagination(client, db_session):
    """Test de pagination des prédictions"""
    # Ajouter 5 prédictions de test
    for i in range(5):
        prediction = Prediction(
            distance_km=10.0 + i,
            heure=8 + i,
            jour_semaine=i % 7,
            meteo=i % 3,
            incidents=i % 2,
            vitesse_moyenne=60.0,
            debit_vehicules=50.0,
            vitesse_prevue=55.0,
            temps_trajet_prevu=11.45,
            timestamp=datetime.now(),
        )
        db_session.add(prediction)
    db_session.commit()

    # Test avec limite de 2 résultats
    response = client.get("/api/v1/predictions?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Test avec skip et limit
    response = client.get("/api/v1/predictions?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.integration
def test_lire_prediction_par_id_existant(client, db_session):
    """Test de récupération d'une prédiction spécifique par son ID"""
    prediction = Prediction(
        distance_km=15.0,
        heure=10,
        jour_semaine=3,
        meteo=0,
        incidents=0,
        vitesse_moyenne=70.0,
        debit_vehicules=45.0,
        vitesse_prevue=68.0,
        temps_trajet_prevu=13.24,
        timestamp=datetime.now(),
    )
    db_session.add(prediction)
    db_session.commit()
    db_session.refresh(prediction)

    response = client.get(f"/api/v1/predictions/{prediction.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == prediction.id
    assert data["heure"] == 10
    assert data["distance_km"] == 15.0


@pytest.mark.integration
def test_lire_prediction_par_id_inexistant(client):
    """Test de récupération d'une prédiction avec un ID inexistant"""
    response = client.get("/api/v1/predictions/9999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Prédiction non trouvée"


@pytest.mark.integration
def test_lire_predictions_ordre_chronologique(client, db_session):
    """Test que les prédictions sont retournées dans l'ordre chronologique inverse"""
    # pylint: disable=import-outside-toplevel
    from datetime import timedelta

    base_time = datetime.now()

    # Ajouter des prédictions avec des timestamps différents
    for i in range(3):
        prediction = Prediction(
            distance_km=10.0,
            heure=8,
            jour_semaine=1,
            meteo=0,
            incidents=0,
            vitesse_moyenne=60.0,
            debit_vehicules=50.0,
            vitesse_prevue=55.0,
            temps_trajet_prevu=11.0,
            timestamp=base_time - timedelta(hours=i),
        )
        db_session.add(prediction)
    db_session.commit()

    response = client.get("/api/v1/predictions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Vérifier que les prédictions sont dans l'ordre chronologique inverse
    # (plus récentes en premier)
    timestamps = [datetime.fromisoformat(p["timestamp"]) for p in data]
    assert timestamps == sorted(timestamps, reverse=True)
