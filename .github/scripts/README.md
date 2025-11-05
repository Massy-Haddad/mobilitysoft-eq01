# Scripts GitHub Actions

Ce dossier contient les scripts utilitaires pour les workflows GitHub Actions et la gestion du projet.

## Scripts disponibles

### 📊 `project_stats.py`

Génère des statistiques complètes du projet pour le rapport final.

**Usage :**
```bash
# Afficher les statistiques dans le terminal
python .github/scripts/project_stats.py

# Générer un fichier JSON
python .github/scripts/project_stats.py --json
```

**Statistiques générées :**
- Lignes de code (app + tests)
- Nombre de tests
- Statistiques Git (commits, branches, contributeurs)
- Fichiers par type
- Dépendances
- Taille de l'image Docker
- Documentation disponible

### 📈 `send_metrics.py`

Envoie les métriques CI/CD vers l'application Metrics.

**Usage :**
```bash
# Configuration via variables d'environnement
export METRICS_API_URL="https://..."
export METRICS_API_KEY="..."
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_REF_NAME="main"
export GITHUB_SHA="abc123..."
export TEST_RESULTS='{"total":25,"passed":25,...}'
export BUILD_RESULTS='{"success":true,...}'

python .github/scripts/send_metrics.py
```

**Variables d'environnement requises :**
- `METRICS_API_URL` : URL de l'endpoint Metrics
- `METRICS_API_KEY` : Clé d'authentification
- `GITHUB_REPOSITORY` : Nom du repository
- `GITHUB_REF_NAME` : Nom de la branche
- `GITHUB_SHA` : Hash du commit
- `TEST_RESULTS` : Résultats des tests (JSON)
- `BUILD_RESULTS` : Résultats du build (JSON)

### 📝 `workflow_metrics_example.yml`

Exemple de configuration pour intégrer l'envoi de métriques dans un workflow GitHub Actions.

**Usage :**
Copiez les sections pertinentes dans votre workflow `.github/workflows/ci-cd.yml`.

## Installation des dépendances

Pour exécuter ces scripts localement :

```bash
pip install requests
```

## Intégration dans les workflows

Ces scripts sont conçus pour être utilisés dans les workflows GitHub Actions :

```yaml
- name: Génération des statistiques
  run: python .github/scripts/project_stats.py --json

- name: Envoi des métriques
  env:
    METRICS_API_URL: ${{ secrets.METRICS_API_URL }}
    METRICS_API_KEY: ${{ secrets.METRICS_API_KEY }}
  run: python .github/scripts/send_metrics.py
```

## Développement

Pour ajouter de nouveaux scripts :

1. Créez le script Python dans ce dossier
2. Rendez-le exécutable : `chmod +x script.py`
3. Ajoutez le shebang : `#!/usr/bin/env python3`
4. Documentez-le dans ce README
5. Ajoutez-le dans le workflow approprié

## Sécurité

⚠️ **Important** :
- Ne jamais commiter de secrets ou tokens dans ces scripts
- Toujours utiliser les secrets GitHub pour les données sensibles
- Valider les entrées avant de les utiliser

## Support

Pour toute question sur ces scripts, consultez :
- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [SETUP.md](../../SETUP.md) - Guide de configuration
- [QUICKSTART.md](../../QUICKSTART.md) - Guide de démarrage rapide
