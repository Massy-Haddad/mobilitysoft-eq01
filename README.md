# MobilitySoft / TrafficSoft — Serveur avec UI + Carte + Heure de départ (FR)

## Points clés
- UI **brandable** (MobilitySoft par défaut, `?brand=TrafficSoft`).
- Carte **Leaflet + OpenStreetMap** pour choisir A/B et calculer `distance_km`.
- **Heure de départ (HH:MM)** côté client; convertie en `heure` (0–23) pour l'API.
- Modèle scikit-learn (LogisticRegression) avec variables simulées + `distance_km`.
- **Stockage des prédictions** dans une base de données PostgreSQL.
- **API de consultation** des prédictions historiques avec filtrage.

## Lancement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données PostgreSQL dans le fichier .env
# DATABASE_URL=postgresql://username:password@localhost:5432/mobilitysoft_db

# Lancer l'application
uvicorn app.main:app --reload
```

## API

- `POST /api/v1/predire` : prend `heure` (int 0–23), `jour_semaine`, `meteo`, `incidents`, `vitesse_moyenne`, `debit_vehicules`, et en option `lat_a/lon_a/lat_b/lon_b` ou `distance_km`.
- `POST /api/v1/reentrainer` : ré-entraîne le modèle synthétique.
- `GET /api/v1/sante` : statut du service.
- `GET /api/v1/predictions` : récupère l'historique des prédictions avec options de filtrage (skip, limit, date_debut, date_fin).
- `GET /api/v1/predictions/{id}` : récupère une prédiction spécifique avec son ID.

## Développement

### Pre-commit hooks

Ce projet utilise pre-commit pour garantir la qualité du code avant chaque commit :

- **Black** : Formatage automatique du code
- **Pylint** : Analyse statique et linting (score minimum requis)
- **Pytest** : Exécution automatique de tous les tests

Installation des hooks :

```bash
# Automatique avec le script
setup_precommit.bat

# Ou manuellement
pre-commit install
```

### Tests

Le projet inclut **25 tests** séparés en deux catégories :

- **Tests unitaires** (11 tests) : Testent les composants isolés (modèle, fonctions utilitaires)
- **Tests d'intégration** (14 tests) : Testent l'API complète avec base de données

Exécution des tests :

```bash
# Tous les tests
tests.bat all

# Tests unitaires uniquement
tests.bat unit

# Tests d'intégration uniquement
tests.bat integration
```

Les tests sont automatiquement exécutés par pre-commit avant chaque commit.

## Conteneurisation avec Docker

### Démarrage rapide avec Docker Compose

```bash
# Lancer l'application avec la base de données
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter l'application
docker-compose down

# Arrêter et supprimer les volumes (données)
docker-compose down -v
```

L'application sera accessible sur `http://localhost:8000`

### Build manuel de l'image Docker

```bash
# Construire l'image
docker build -t mobilitysoft:latest .

# Exécuter le conteneur (avec une base de données existante)
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  mobilitysoft:latest
```

## CI/CD avec GitHub Actions

Le projet utilise GitHub Actions pour l'intégration et le déploiement continus :

### Workflows configurés

1. **Tests d'intégration** (`.github/workflows/tests.yml`)
   - Exécuté sur chaque push et pull request
   - Lance tous les tests avec une base PostgreSQL
   - Vérifie la qualité du code

2. **Build et Push Docker** (`.github/workflows/docker.yml`)
   - Construit l'image Docker
   - Pousse l'image sur DockerHub (branches main et develop)
   - Tags automatiques basés sur les branches et commits

3. **CI/CD Complet** (`.github/workflows/ci-cd.yml`)
   - Combine tests + build Docker
   - Prépare les métriques CI pour l'application Metrics
   - Déploiement automatique si tous les tests passent

### Configuration requise pour DockerHub

Pour activer le push Docker, configurez ces secrets GitHub :
- `DOCKERHUB_USERNAME` : Votre nom d'utilisateur DockerHub
- `DOCKERHUB_TOKEN` : Token d'accès DockerHub

**Comment créer un token DockerHub :**
1. Connectez-vous sur [hub.docker.com](https://hub.docker.com)
2. Account Settings → Security → New Access Token
3. Copiez le token généré
4. Sur GitHub : Settings → Secrets and variables → Actions → New repository secret

## Structure du projet

```text
mobilitysoft-eq01/
├── .github/
│   └── workflows/       # Workflows GitHub Actions (CI/CD)
├── app/
│   ├── api/v1/          # Endpoints de l'API
│   ├── core/            # Configuration et middlewares
│   ├── models/          # Schémas Pydantic
│   ├── services/        # Modèle de prédiction
│   ├── ui/              # Interface utilisateur
│   ├── database.py      # Configuration de la base de données
│   └── main.py          # Point d'entrée de l'application
├── tests/               # Tests unitaires et d'intégration
├── .dockerignore        # Fichiers à ignorer pour Docker
├── .env.example         # Exemple de configuration
├── .pre-commit-config.yaml  # Configuration des hooks pre-commit
├── .pylintrc            # Configuration Pylint
├── docker-compose.yml   # Configuration Docker multi-conteneurs
├── Dockerfile           # Image Docker de l'application
├── pytest.ini           # Configuration Pytest
└── requirements.txt     # Dépendances Python
```
