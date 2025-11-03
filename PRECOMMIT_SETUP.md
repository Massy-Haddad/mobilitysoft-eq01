# Configuration de l'Intégration Continue - Pre-commit Git Hook

## Résumé de l'implémentation

Cette documentation décrit l'implémentation des hooks pre-commit pour le projet MobilitySoft, conformément aux exigences du laboratoire.

## Composants installés

### 1. Pre-commit (https://pre-commit.com/)
- Framework pour gérer les hooks Git
- Configuration dans `.pre-commit-config.yaml`
- Installation via `pip install pre-commit`
- Activation via `pre-commit install`

### 2. Pylint (https://pylint.readthedocs.io/en/stable/)
- Outil de linting pour Python
- Analyse statique du code
- Configuration personnalisée dans `.pylintrc`
- Désactive certaines règles trop strictes pour faciliter le développement

### 3. Black (https://github.com/psf/black)
- Formateur de code Python
- Applique automatiquement le style PEP 8
- Longueur de ligne configurée à 100 caractères
- Formatage automatique avant chaque commit

### 4. Pytest
- Framework de tests unitaires
- Configuration dans `pytest.ini`
- Tests organisés dans le répertoire `tests/`
- Exécution automatique avant chaque commit

## Structure des tests créés

```
tests/
├── __init__.py
├── conftest.py                 # Fixtures et configuration pytest
├── test_api_base.py           # Tests des endpoints de base (santé, UI)
├── test_predictions.py        # Tests de l'API de prédiction de trafic
├── test_consultation_api.py   # Tests de l'API de consultation des prédictions
├── test_model.py              # Tests du modèle de prédiction
└── test_utils.py              # Tests des fonctions utilitaires (haversine, recommandations)
```

## Tests unitaires créés

### test_api_base.py
- `test_sante_endpoint()` : Vérifie le bon fonctionnement de l'endpoint de santé
- `test_servir_ui()` : Teste le service de l'interface utilisateur

### test_predictions.py (8 tests)
- Tests de validation des données d'entrée
- Test de sauvegarde en base de données
- Tests avec différents scénarios (heure de pointe, incidents, météo)
- Tests de validation des contraintes (heure, jour, météo invalides)

### test_consultation_api.py (7 tests)
- Test de consultation avec base vide
- Test de consultation avec données
- Test de pagination
- Test de récupération par ID
- Test de gestion des erreurs (404)
- Test de l'ordre chronologique

### test_model.py (5 tests)
- Test de création du modèle
- Test de forme des prédictions
- Test de validation des valeurs
- Test de ré-entraînement
- Test de prédictions multiples

### test_utils.py (6 tests)
- Tests de la fonction haversine (calcul de distance)
- Tests des recommandations pour différents niveaux de risque
- Test de recommandations pour les heures de pointe

**Total : 28 tests unitaires couvrant toutes les fonctionnalités principales**

## Fonctionnement du Pre-commit

### Workflow automatique
1. Vous faites `git add` pour ajouter des fichiers
2. Vous faites `git commit`
3. Pre-commit s'exécute automatiquement :
   - **Black** formate le code
   - **Pylint** vérifie la qualité du code
   - **Pytest** exécute tous les tests
   - **Hooks généraux** vérifient les fichiers
4. Si tous les hooks passent : le commit est créé
5. Si un hook échoue : le commit est annulé avec des messages d'erreur

### Exécution manuelle
```bash
# Exécuter tous les hooks sur tous les fichiers
pre-commit run --all-files

# Exécuter un hook spécifique
pre-commit run black
pre-commit run pylint
pre-commit run pytest-check

# Exécuter juste les tests
pytest
pytest -v  # mode verbose
```

## Installation et utilisation

### Installation initiale
```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Installer les hooks pre-commit
pre-commit install

# 3. (Optionnel) Tester sur tous les fichiers
pre-commit run --all-files
```

Ou simplement exécuter le script :
```bash
setup_precommit.bat
```

### Utilisation quotidienne
Les hooks s'exécutent automatiquement lors de chaque `git commit`. Aucune action supplémentaire n'est requise.

### Bypass (déconseillé)
Si nécessaire, vous pouvez bypasser les hooks :
```bash
git commit --no-verify
```

## Configuration des hooks

### .pre-commit-config.yaml
Configure les hooks qui s'exécutent avant chaque commit :
- Version de chaque outil
- Arguments de ligne de commande
- Dépendances supplémentaires

### .pylintrc
Configure les règles de linting Pylint :
- Longueur maximale de ligne (100)
- Messages désactivés pour éviter les faux positifs
- Seuils pour la complexité du code

### pytest.ini
Configure le comportement de pytest :
- Répertoire des tests
- Mode async automatique
- Options d'affichage

## Avantages de cette configuration

1. **Qualité du code** : Le linting détecte les erreurs potentielles
2. **Cohérence** : Black assure un style uniforme
3. **Fiabilité** : Les tests empêchent les régressions
4. **Automatisation** : Aucune action manuelle requise
5. **Feedback rapide** : Les erreurs sont détectées avant le push

## Recommandations

1. **Ne pas bypasser les hooks** sauf nécessité absolue
2. **Corriger les erreurs** plutôt que de les ignorer
3. **Écrire des tests** pour chaque nouvelle fonctionnalité
4. **Maintenir une couverture élevée** (objectif : > 80%)
5. **Exécuter les tests localement** avant de pousser

## Dépannage

### Les hooks ne s'exécutent pas
```bash
# Réinstaller les hooks
pre-commit install
```

### Black modifie beaucoup de fichiers
```bash
# C'est normal la première fois
# Ajoutez les fichiers modifiés et recommitez
git add .
git commit
```

### Pylint trouve trop d'erreurs
- Corrigez les erreurs réelles
- Si une règle est trop stricte, ajustez `.pylintrc`
- Ne désactivez pas les règles sans raison valable

### Les tests échouent
- Vérifiez que la base de données est correctement configurée
- Assurez-vous que toutes les dépendances sont installées
- Corrigez le code ou les tests selon le cas

## Conformité avec les exigences du laboratoire

✅ **Linting** : Pylint configuré et intégré
✅ **Formatage** : Black configuré et intégré
✅ **Tests unitaires** : 28 tests couvrant toutes les fonctionnalités
✅ **Pre-commit** : Tous les hooks configurés et fonctionnels
✅ **Automatisation** : Exécution automatique à chaque commit

## Fichiers créés/modifiés

### Nouveaux fichiers
- `.pre-commit-config.yaml` : Configuration pre-commit
- `.pylintrc` : Configuration Pylint
- `pytest.ini` : Configuration Pytest
- `TESTING.md` : Documentation des tests
- `setup_precommit.bat` : Script d'installation
- `tests/` : Répertoire avec tous les tests unitaires

### Fichiers modifiés
- `requirements.txt` : Ajout des dépendances de test et qualité
- `README.md` : Ajout de la section développement
- `.gitignore` : Ajout des fichiers de test à ignorer
