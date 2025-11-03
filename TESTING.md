# Guide des Tests et Pre-commit pour MobilitySoft

## Installation des dépendances de développement

Installez toutes les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

## Configuration de Pre-commit

### Installation initiale

Installez les hooks pre-commit dans votre dépôt Git :

```bash
pre-commit install
```

Cette commande configure Git pour exécuter automatiquement les hooks avant chaque commit.

### Exécution manuelle

Pour exécuter tous les hooks sur tous les fichiers :

```bash
pre-commit run --all-files
```

Pour exécuter un hook spécifique :

```bash
pre-commit run black --all-files
pre-commit run pylint --all-files
pre-commit run pytest-check --all-files
```

## Hooks Pre-commit configurés

### 1. Black (Formatage du code)
- Formate automatiquement le code Python selon les standards PEP 8
- Longueur de ligne maximale : 100 caractères
- S'exécute automatiquement avant chaque commit

### 2. Pylint (Analyse statique / Linting)
- Vérifie la qualité du code Python
- Configuration personnalisée dans `.pylintrc`
- Détecte les erreurs potentielles et les problèmes de style

### 3. Pytest (Tests unitaires)
- Exécute tous les tests unitaires avant chaque commit
- Les tests doivent tous passer pour que le commit soit accepté
- Configuration dans `pytest.ini`

### 4. Hooks généraux
- `trailing-whitespace` : Supprime les espaces en fin de ligne
- `end-of-file-fixer` : Assure une ligne vide à la fin des fichiers
- `check-yaml` : Valide la syntaxe des fichiers YAML
- `check-json` : Valide la syntaxe des fichiers JSON
- `check-added-large-files` : Empêche l'ajout de fichiers trop volumineux
- `check-merge-conflict` : Détecte les marqueurs de conflit de merge

## Exécution des tests

### Lancer tous les tests

```bash
pytest
```

### Lancer les tests avec plus de détails

```bash
pytest -v
```

### Lancer les tests avec couverture de code

```bash
pytest --cov=app --cov-report=html
```

### Lancer des tests spécifiques

```bash
# Un fichier de test spécifique
pytest tests/test_predictions.py

# Une classe de test spécifique
pytest tests/test_predictions.py::TestClass

# Une fonction de test spécifique
pytest tests/test_predictions.py::test_predire_avec_donnees_valides
```

## Structure des tests

```
tests/
├── __init__.py
├── conftest.py                 # Configuration et fixtures pytest
├── test_api_base.py           # Tests des endpoints de base
├── test_predictions.py        # Tests de l'API de prédiction
├── test_consultation_api.py   # Tests de l'API de consultation
├── test_model.py              # Tests du modèle de trafic
└── test_utils.py              # Tests des fonctions utilitaires
```

## Résolution des problèmes

### Pre-commit échoue

Si pre-commit échoue, lisez attentivement les messages d'erreur :

1. **Black** : Les fichiers seront automatiquement formatés. Ajoutez-les et recommitez.
2. **Pylint** : Corrigez les erreurs de code signalées.
3. **Pytest** : Assurez-vous que tous les tests passent. Corrigez les tests ou le code en conséquence.

### Désactiver temporairement pre-commit

Si vous avez besoin de commiter sans exécuter les hooks (non recommandé) :

```bash
git commit --no-verify
```

### Mettre à jour les hooks

Pour mettre à jour les hooks vers leurs dernières versions :

```bash
pre-commit autoupdate
```

## Bonnes pratiques

1. **Exécutez les tests localement** avant de pousser votre code
2. **Corrigez les erreurs de Pylint** au lieu de les désactiver
3. **Écrivez des tests** pour toutes les nouvelles fonctionnalités
4. **Maintenez une couverture de tests élevée** (> 80%)
5. **Respectez le formatage Black** pour la cohérence du code

## Configuration personnalisée

### Modifier la configuration Pylint

Éditez `.pylintrc` pour ajuster les règles de linting.

### Modifier la longueur de ligne Black

Dans `.pre-commit-config.yaml`, modifiez l'argument `--line-length`.

### Ajouter des tests à ignorer

Utilisez les marqueurs pytest dans `pytest.ini` ou ajoutez `@pytest.mark.skip`.
