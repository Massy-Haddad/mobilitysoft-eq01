# Exemple d'intégration avec l'application Metrics
# À ajouter dans le workflow GitHub Actions ou comme script séparé

import os
import json
import requests
from datetime import datetime

def send_ci_metrics_to_metrics_app():
    """
    Envoie les métriques CI/CD vers l'application Metrics.
    
    Variables d'environnement requises :
    - METRICS_API_URL : URL de l'endpoint Metrics
    - METRICS_API_KEY : Clé d'authentification
    - GITHUB_REPOSITORY : Nom du repository (fourni par GitHub Actions)
    - GITHUB_REF_NAME : Nom de la branche (fourni par GitHub Actions)
    - GITHUB_SHA : Hash du commit (fourni par GitHub Actions)
    - TEST_RESULTS : Résultats des tests au format JSON
    - BUILD_RESULTS : Résultats du build au format JSON
    """
    
    # Configuration
    metrics_api_url = os.getenv('METRICS_API_URL')
    metrics_api_key = os.getenv('METRICS_API_KEY')
    
    if not metrics_api_url or not metrics_api_key:
        print("⚠️ Variables METRICS_API_URL ou METRICS_API_KEY non configurées")
        print("Les métriques ne seront pas envoyées")
        return
    
    # Données du contexte GitHub Actions
    repository = os.getenv('GITHUB_REPOSITORY', 'unknown/unknown')
    branch = os.getenv('GITHUB_REF_NAME', 'unknown')
    commit_sha = os.getenv('GITHUB_SHA', 'unknown')
    commit_message = os.getenv('COMMIT_MESSAGE', '')
    author = os.getenv('GITHUB_ACTOR', 'unknown')
    
    # Résultats des tests (à parser depuis les outputs précédents)
    test_results = json.loads(os.getenv('TEST_RESULTS', '{}'))
    build_results = json.loads(os.getenv('BUILD_RESULTS', '{}'))
    
    # Construire le payload
    payload = {
        "project": "mobilitysoft",
        "team": repository.split('/')[-1].replace('mobilitysoft-', ''),
        "branch": branch,
        "commit_sha": commit_sha[:8],
        "commit_message": commit_message,
        "author": author,
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "metrics": {
            "tests": {
                "total": test_results.get('total', 0),
                "passed": test_results.get('passed', 0),
                "failed": test_results.get('failed', 0),
                "skipped": test_results.get('skipped', 0),
                "duration_seconds": test_results.get('duration', 0),
                "coverage_percent": test_results.get('coverage', 0)
            },
            "build": {
                "success": build_results.get('success', False),
                "duration_seconds": build_results.get('duration', 0),
                "docker_image_size_mb": build_results.get('image_size_mb', 0),
                "tags": build_results.get('tags', [])
            },
            "deployment": {
                "dockerhub_push": build_results.get('dockerhub_push', False),
                "push_duration_seconds": build_results.get('push_duration', 0)
            },
            "quality": {
                "pylint_score": test_results.get('pylint_score', 0),
                "black_formatted": test_results.get('black_formatted', True),
                "pre_commit_passed": test_results.get('pre_commit_passed', True)
            }
        }
    }
    
    # Envoi à l'API Metrics
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {metrics_api_key}'
    }
    
    try:
        print(f"📊 Envoi des métriques CI/CD vers {metrics_api_url}...")
        response = requests.post(
            metrics_api_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        print(f"✅ Métriques envoyées avec succès ! (Status: {response.status_code})")
        print(f"📈 Réponse: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de l'envoi des métriques: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Détails: {e.response.text}")

if __name__ == "__main__":
    send_ci_metrics_to_metrics_app()
