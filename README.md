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

Ce projet utilise pre-commit pour garantir la qualité du code. Les hooks configurés incluent :

- **Black** : Formatage automatique du code
- **Pylint** : Analyse statique et linting
- **Pytest** : Exécution des tests unitaires

Pour installer les hooks pre-commit :

```bash
pre-commit install
```

Pour exécuter manuellement tous les hooks :

```bash
pre-commit run --all-files
```

### Tests

Pour exécuter les tests unitaires :

```bash
pytest
```

Pour plus de détails sur les tests et le pre-commit, consultez [TESTING.md](TESTING.md).

## Structure du projet

```
mobilitysoft-eq01/
├── app/
│   ├── api/v1/          # Endpoints de l'API
│   ├── core/            # Configuration et middlewares
│   ├── models/          # Schémas Pydantic
│   ├── services/        # Modèle de prédiction
│   ├── ui/              # Interface utilisateur
│   ├── database.py      # Configuration de la base de données
│   └── main.py          # Point d'entrée de l'application
├── tests/               # Tests unitaires
├── .pre-commit-config.yaml  # Configuration des hooks pre-commit
├── .pylintrc            # Configuration Pylint
├── pytest.ini           # Configuration Pytest
└── requirements.txt     # Dépendances Python
```
