#!/bin/bash

# Script de validation pré-démo pour MobilitySoft
# Vérifie que tous les composants sont prêts

set +e  # Ne pas arrêter en cas d'erreur (on veut voir tous les problèmes)

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Compteurs
PASSED=0
FAILED=0
WARNINGS=0

# Fonction pour afficher un check
check_passed() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_failed() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

check_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "🔍 VALIDATION PRÉ-DÉMO - MOBILITYSOFT"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. Vérification des fichiers essentiels
echo "📁 FICHIERS ESSENTIELS"
echo "───────────────────────────────────────────────────────────"

files=(
    "Dockerfile"
    "docker-compose.yml"
    "requirements.txt"
    "README.md"
    "SETUP.md"
    "QUICKSTART.md"
    ".env.example"
    ".dockerignore"
    ".pre-commit-config.yaml"
    "pytest.ini"
    ".github/workflows/tests.yml"
    ".github/workflows/docker.yml"
    ".github/workflows/ci-cd.yml"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        check_passed "$file existe"
    else
        check_failed "$file est manquant"
    fi
done

echo ""

# 2. Vérification de la structure du projet
echo "📂 STRUCTURE DU PROJET"
echo "───────────────────────────────────────────────────────────"

dirs=(
    "app"
    "app/api/v1"
    "app/core"
    "app/models"
    "app/services"
    "app/ui"
    "tests"
    ".github"
    ".github/workflows"
    ".github/scripts"
)

for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        check_passed "$dir/ existe"
    else
        check_failed "$dir/ est manquant"
    fi
done

echo ""

# 3. Vérification de Docker
echo "🐳 DOCKER"
echo "───────────────────────────────────────────────────────────"

if command -v docker &> /dev/null; then
    check_passed "Docker est installé"
    docker_version=$(docker --version)
    check_info "Version: $docker_version"
else
    check_failed "Docker n'est pas installé"
fi

if command -v docker-compose &> /dev/null; then
    check_passed "docker-compose est installé"
    compose_version=$(docker-compose --version)
    check_info "Version: $compose_version"
else
    check_failed "docker-compose n'est pas installé"
fi

# Vérifier si l'image existe
if docker images | grep -q "mobilitysoft"; then
    check_passed "Image Docker mobilitysoft existe"
    image_size=$(docker images mobilitysoft:latest --format "{{.Size}}")
    check_info "Taille: $image_size"
else
    check_warning "Image Docker mobilitysoft n'existe pas encore (à builder)"
fi

echo ""

# 4. Vérification des conteneurs
echo "🔧 CONTENEURS DOCKER"
echo "───────────────────────────────────────────────────────────"

if docker ps | grep -q "mobilitysoft_app"; then
    check_passed "Container mobilitysoft_app est en cours d'exécution"
else
    check_warning "Container mobilitysoft_app n'est pas en cours d'exécution"
fi

if docker ps | grep -q "mobilitysoft_db"; then
    check_passed "Container mobilitysoft_db est en cours d'exécution"
else
    check_warning "Container mobilitysoft_db n'est pas en cours d'exécution"
fi

echo ""

# 5. Vérification de l'application
echo "🌐 APPLICATION"
echo "───────────────────────────────────────────────────────────"

if curl -s http://localhost:8000/api/v1/sante > /dev/null 2>&1; then
    check_passed "Application répond sur http://localhost:8000"
    health_status=$(curl -s http://localhost:8000/api/v1/sante | grep -o '"status":"[^"]*"')
    check_info "Statut: $health_status"
else
    check_warning "Application ne répond pas sur http://localhost:8000"
    check_info "Lancez 'docker-compose up -d' pour démarrer l'application"
fi

echo ""

# 6. Vérification de Python et des dépendances
echo "🐍 PYTHON ET DÉPENDANCES"
echo "───────────────────────────────────────────────────────────"

if command -v python3 &> /dev/null; then
    check_passed "Python3 est installé"
    python_version=$(python3 --version)
    check_info "Version: $python_version"
else
    check_failed "Python3 n'est pas installé"
fi

if [ -d ".venv" ]; then
    check_passed "Environnement virtuel .venv existe"
else
    check_warning "Environnement virtuel .venv n'existe pas"
    check_info "Créez-le avec: python3 -m venv .venv"
fi

if [ -f "requirements.txt" ]; then
    dep_count=$(grep -c . requirements.txt)
    check_passed "requirements.txt contient $dep_count dépendances"
fi

echo ""

# 7. Vérification des tests
echo "🧪 TESTS"
echo "───────────────────────────────────────────────────────────"

test_files=$(find tests -name "test_*.py" 2>/dev/null | wc -l)
if [ "$test_files" -gt 0 ]; then
    check_passed "$test_files fichiers de tests trouvés"
else
    check_failed "Aucun fichier de test trouvé"
fi

if [ -f "pytest.ini" ]; then
    check_passed "pytest.ini configuré"
fi

if [ -f ".pre-commit-config.yaml" ]; then
    check_passed ".pre-commit-config.yaml configuré"
fi

echo ""

# 8. Vérification de Git
echo "📝 GIT"
echo "───────────────────────────────────────────────────────────"

if git rev-parse --git-dir > /dev/null 2>&1; then
    check_passed "Repository Git initialisé"
    
    current_branch=$(git branch --show-current)
    check_info "Branche actuelle: $current_branch"
    
    commit_count=$(git rev-list --count HEAD)
    check_info "Nombre de commits: $commit_count"
    
    if git diff-index --quiet HEAD --; then
        check_passed "Aucun changement non commité"
    else
        check_warning "Des changements non commités sont présents"
        check_info "Exécutez 'git status' pour voir les détails"
    fi
else
    check_failed "Pas de repository Git"
fi

echo ""

# 9. Vérification de GitHub (remote)
echo "🌍 GITHUB"
echo "───────────────────────────────────────────────────────────"

if git remote -v | grep -q "github.com"; then
    check_passed "Remote GitHub configuré"
    remote_url=$(git remote get-url origin)
    check_info "URL: $remote_url"
else
    check_warning "Aucun remote GitHub configuré"
fi

echo ""

# 10. Vérification des secrets (simulation)
echo "🔐 CONFIGURATION CI/CD"
echo "───────────────────────────────────────────────────────────"

check_info "Secrets GitHub à vérifier manuellement :"
echo "   - DOCKERHUB_USERNAME"
echo "   - DOCKERHUB_TOKEN"
echo "   - METRICS_API_URL (optionnel)"
echo "   - METRICS_API_KEY (optionnel)"

echo ""

# 11. Vérification DockerHub (information)
echo "🐋 DOCKERHUB"
echo "───────────────────────────────────────────────────────────"

check_info "À vérifier manuellement sur hub.docker.com :"
echo "   - Repository 'mobilitysoft' créé"
echo "   - Token d'accès généré"
echo "   - Au moins une image poussée"

echo ""

# 12. Documentation
echo "📚 DOCUMENTATION"
echo "───────────────────────────────────────────────────────────"

docs=(
    "README.md:Documentation principale"
    "SETUP.md:Guide de configuration"
    "QUICKSTART.md:Guide de démarrage rapide"
    "RECAP.md:Récapitulatif du projet"
    "RAPPORT_LABO2.md:Rapport final"
)

for doc in "${docs[@]}"; do
    IFS=':' read -r file desc <<< "$doc"
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file")
        check_passed "$desc ($file) - $lines lignes"
    else
        check_warning "$desc ($file) manquant"
    fi
done

echo ""

# Résumé final
echo "═══════════════════════════════════════════════════════════"
echo "📊 RÉSUMÉ DE LA VALIDATION"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}✓ Tests réussis  : $PASSED${NC}"
echo -e "${YELLOW}⚠ Avertissements : $WARNINGS${NC}"
echo -e "${RED}✗ Tests échoués  : $FAILED${NC}"
echo ""

# Score de préparation
total=$((PASSED + WARNINGS + FAILED))
if [ $total -gt 0 ]; then
    score=$((PASSED * 100 / total))
    echo "Score de préparation : $score%"
    echo ""
    
    if [ $score -ge 90 ]; then
        echo -e "${GREEN}🎉 EXCELLENT ! Vous êtes prêt pour la démo !${NC}"
    elif [ $score -ge 75 ]; then
        echo -e "${YELLOW}👍 BIEN ! Quelques ajustements mineurs et vous serez prêt.${NC}"
    elif [ $score -ge 50 ]; then
        echo -e "${YELLOW}⚠️  ATTENTION ! Plusieurs éléments nécessitent votre attention.${NC}"
    else
        echo -e "${RED}❌ CRITIQUE ! Plusieurs problèmes doivent être résolus.${NC}"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Instructions finales
if [ $FAILED -gt 0 ] || [ $WARNINGS -gt 5 ]; then
    echo "📋 ACTIONS RECOMMANDÉES :"
    echo ""
    
    if ! command -v docker &> /dev/null; then
        echo "1. Installer Docker : https://docs.docker.com/get-docker/"
    fi
    
    if ! docker ps | grep -q "mobilitysoft"; then
        echo "2. Démarrer l'application : docker-compose up -d"
    fi
    
    if [ ! -d ".venv" ]; then
        echo "3. Créer l'environnement virtuel : python3 -m venv .venv"
    fi
    
    if git diff-index --quiet HEAD --; then
        :
    else
        echo "4. Commiter vos changements : git add . && git commit -m 'msg'"
    fi
    
    echo ""
fi

echo "Pour plus d'informations, consultez :"
echo "  - QUICKSTART.md pour le démarrage rapide"
echo "  - SETUP.md pour la configuration détaillée"
echo "  - README.md pour la documentation complète"
echo ""

# Code de sortie
if [ $FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi
