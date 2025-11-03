"""
Tests pour les endpoints de base de l'API MobilitySoft
"""
# pylint: disable=import-error
import pytest


@pytest.mark.integration
def test_sante_endpoint(client):
    """Test de l'endpoint de santé de l'API"""
    response = client.get("/api/v1/sante")
    assert response.status_code == 200
    data = response.json()
    assert "ok" in data
    assert data["ok"] is True
    assert "nom" in data


@pytest.mark.integration
def test_servir_ui(client):
    """Test de l'endpoint principal qui sert l'interface utilisateur"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
