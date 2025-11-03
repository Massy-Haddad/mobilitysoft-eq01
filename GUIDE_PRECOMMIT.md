# 🎯 Guide Simple : Comment utiliser Pre-commit

## C'est quoi Pre-commit ?

Pre-commit est comme un **gardien automatique** qui vérifie votre code avant de l'enregistrer dans Git.

## ✅ C'est déjà installé !

Vous avez exécuté `setup_precommit.bat` avec succès. Tout est prêt !

## 📝 Comment ça marche maintenant ?

### AVANT (sans pre-commit) :
```bash
git add mon_fichier.py
git commit -m "Mon changement"
# ✅ Commit créé immédiatement
```

### MAINTENANT (avec pre-commit) :
```bash
git add mon_fichier.py
git commit -m "Mon changement"
# ⚙️ Pre-commit vérifie automatiquement :
#   - Formatage du code (Black)
#   - Qualité du code (Pylint)
#   - Tests (Pytest - 25 tests)
# ✅ Si tout passe → Commit créé
# ❌ Si erreur → Commit annulé, vous devez corriger
```

## 🚀 Utilisation quotidienne

### Scénario 1 : Tout fonctionne parfaitement

```bash
# 1. Vous modifiez des fichiers
code app/main.py

# 2. Vous ajoutez vos modifications
git add app/main.py

# 3. Vous faites un commit
git commit -m "Ajout d'une nouvelle fonctionnalité"

# Pre-commit s'exécute automatiquement...
[INFO] black....Passed
[INFO] pylint...Passed
[INFO] pytest...Passed (25/25 tests)

# ✅ Commit créé avec succès !
```

### Scénario 2 : Black corrige votre formatage

```bash
git add app/main.py
git commit -m "Mon changement"

# Pre-commit s'exécute...
[INFO] black....Failed - fichiers reformatés

# ⚠️ Black a automatiquement corrigé le formatage
# Vous devez juste re-ajouter les fichiers :

git add app/main.py
git commit -m "Mon changement"

# ✅ Cette fois ça passe !
```

### Scénario 3 : Un test échoue

```bash
git add app/main.py
git commit -m "Mon changement"

# Pre-commit s'exécute...
[INFO] black....Passed
[INFO] pylint...Passed
[INFO] pytest...Failed (24/25 tests)
FAILED tests/test_predictions.py::test_ma_fonction

# ❌ Le commit est annulé
# Vous devez :
# 1. Corriger le test ou le code
# 2. Vérifier : pytest
# 3. Re-essayer le commit
```

## 🔍 Commandes utiles

### Tester AVANT de commiter (recommandé !)

```bash
# Tester tous les hooks manuellement
pre-commit run --all-files

# Exécuter juste les tests
pytest

# Exécuter les tests avec détails
pytest -v
```

### Voir l'état de vos fichiers

```bash
git status          # Voir quels fichiers sont modifiés
git diff           # Voir les modifications
git diff --staged  # Voir ce qui sera commité
```

## 💡 Conseils pratiques

### ✅ À FAIRE :

1. **Testez localement d'abord**
   ```bash
   pytest  # Avant de commiter
   ```

2. **Faites des petits commits fréquents**
   - Plus facile à déboguer si quelque chose échoue

3. **Lisez les messages d'erreur**
   - Ils vous disent exactement quoi corriger

### ❌ À ÉVITER :

1. **Ne pas bypass pre-commit** (sauf urgence)
   ```bash
   git commit --no-verify  # ⚠️ Déconseillé !
   ```

2. **Ne pas ignorer les erreurs Pylint**
   - Elles sont là pour vous aider

3. **Ne pas supprimer les tests**
   - Ils protègent votre code

## 🆘 En cas de problème

### "Pre-commit ne s'exécute pas"

```bash
pre-commit install  # Réinstaller
```

### "Trop de fichiers modifiés par Black"

```bash
# C'est normal la première fois !
git add .
git commit -m "Formatage automatique par Black"
```

### "Je suis bloqué, je ne peux pas commiter"

1. Regardez les messages d'erreur
2. Corrigez les problèmes indiqués
3. Testez : `pytest` ou `pre-commit run --all-files`
4. Réessayez le commit

### "Urgent : je dois commiter maintenant !"

```bash
# En dernier recours seulement :
git commit --no-verify -m "Message"
```

## 📊 Vos résultats actuels

Après la correction que j'ai faite :

- ✅ **25/25 tests passent** (100%)
- ✅ **Black** : Formatage OK
- ✅ **Pylint** : Qualité du code OK
- ✅ **Pre-commit** : Complètement fonctionnel

## 🎓 Exemple complet

Vous voulez ajouter une nouvelle API :

```python
# 1. Créez votre code
# app/api/v1/endpoints.py
@router.get("/nouvelle-api")
async def ma_nouvelle_api():
    return {"message": "Bonjour"}

# 2. Créez un test
# tests/test_nouvelle_api.py
def test_ma_nouvelle_api(client):
    response = client.get("/api/v1/nouvelle-api")
    assert response.status_code == 200
    assert response.json()["message"] == "Bonjour"

# 3. Testez localement
pytest tests/test_nouvelle_api.py  # ✅ Passe

# 4. Commitez
git add app/api/v1/endpoints.py tests/test_nouvelle_api.py
git commit -m "Ajout nouvelle API"

# Pre-commit vérifie tout automatiquement
# ✅ Commit créé !

# 5. Poussez vers GitHub
git push origin ma-branche
```

## 🎯 En résumé

### Vous n'avez RIEN à faire de spécial !

Pre-commit fonctionne **automatiquement** à chaque commit. C'est tout !

### Si pre-commit bloque votre commit :

1. 📖 Lisez le message d'erreur
2. 🔧 Corrigez le problème
3. ✅ Recommitez

### Questions ?

Consultez :
- `TESTING.md` - Documentation complète des tests
- `PRECOMMIT_SETUP.md` - Documentation technique détaillée

---

**Bonne programmation ! 🚀**
