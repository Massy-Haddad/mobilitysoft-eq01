"""
Tests pour l'endpoint de prédiction de trafic
"""


def test_predire_avec_donnees_valides(client):
    """Test de prédiction avec des données valides"""
    payload = {
        "heure": 8,
        "jour_semaine": 1,
        "meteo": 0,
        "incidents": 0,
        "vitesse_moyenne": 60.0,
        "debit_vehicules": 50.0,
        "lat_a": 45.5017,
        "lon_a": -73.5673,
        "lat_b": 45.5088,
        "lon_b": -73.5540,
    }
    response = client.post("/api/v1/predire", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risque" in data
    assert "proba" in data
    assert "recommandations" in data
    assert data["risque"] in ["élevé", "faible"]
    assert isinstance(data["proba"], float)
    assert isinstance(data["recommandations"], list)


def test_predire_avec_distance_fournie(client):
    """Test de prédiction avec distance directement fournie"""
    payload = {
        "heure": 17,
        "jour_semaine": 4,
        "meteo": 1,
        "incidents": 1,
        "vitesse_moyenne": 40.0,
        "debit_vehicules": 80.0,
        "distance_km": 15.5,
    }
    response = client.post("/api/v1/predire", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risque" in data
    assert "proba" in data


def test_predire_avec_donnees_invalides_heure(client):
    """Test de prédiction avec une heure invalide"""
    payload = {
        "heure": 25,  # Heure invalide
        "jour_semaine": 1,
        "meteo": 0,
        "incidents": 0,
        "vitesse_moyenne": 60.0,
        "debit_vehicules": 50.0,
    }
    response = client.post("/api/v1/predire", json=payload)
    assert response.status_code == 422  # Validation error


def test_predire_avec_donnees_invalides_jour(client):
    """Test de prédiction avec un jour invalide"""
    payload = {
        "heure": 8,
        "jour_semaine": 7,  # Jour invalide (doit être 0-6)
        "meteo": 0,
        "incidents": 0,
        "vitesse_moyenne": 60.0,
        "debit_vehicules": 50.0,
    }
    response = client.post("/api/v1/predire", json=payload)
    assert response.status_code == 422  # Validation error


def test_predire_avec_meteo_invalide(client):
    """Test de prédiction avec météo invalide"""
    payload = {
        "heure": 8,
        "jour_semaine": 1,
        "meteo": 3,  # Météo invalide (doit être 0-2)
        "incidents": 0,
        "vitesse_moyenne": 60.0,
        "debit_vehicules": 50.0,
    }
    response = client.post("/api/v1/predire", json=payload)
    assert response.status_code == 422  # Validation error


def test_predire_sauvegarde_en_base(client, db_session):
    """Test que la prédiction est bien sauvegardée dans la base de données"""
    # pylint: disable=import-outside-toplevel
    from app.database import Prediction

    # Vérifier qu'il n'y a pas de prédictions au départ
    count_before = db_session.query(Prediction).count()

    payload = {
        "heure": 10,
        "jour_semaine": 2,
        "meteo": 0,
        "incidents": 0,
        "vitesse_moyenne": 70.0,
        "debit_vehicules": 40.0,
        "distance_km": 10.0,
    }
    response = client.post("/api/v1/predire", json=payload)
    assert response.status_code == 200

    # Vérifier qu'une prédiction a été ajoutée
    db_session.commit()
    count_after = db_session.query(Prediction).count()
    assert count_after == count_before + 1

    # Vérifier le contenu de la prédiction
    prediction = db_session.query(Prediction).first()
    assert prediction.heure == 10
    assert prediction.jour_semaine == 2
    assert prediction.vitesse_moyenne == 70.0
