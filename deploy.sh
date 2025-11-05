#!/bin/bash

# Script de déploiement et test pour MobilitySoft
# Usage: ./deploy.sh [command]

set -e  # Arrêter en cas d'erreur

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonctions utilitaires
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Vérifier que Docker est installé
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    print_success "Docker est installé"
}

# Vérifier que docker-compose est installé
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "docker-compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    print_success "docker-compose est installé"
}

# Créer le fichier .env s'il n'existe pas
setup_env() {
    if [ ! -f .env ]; then
        print_info "Création du fichier .env depuis .env.example"
        cp .env.example .env
        print_success "Fichier .env créé. Veuillez le modifier si nécessaire."
    else
        print_success "Fichier .env existe déjà"
    fi
}

# Démarrer l'application avec docker-compose
start() {
    print_info "Démarrage de MobilitySoft avec Docker Compose..."
    check_docker
    check_docker_compose
    setup_env
    
    docker-compose up -d
    print_success "Application démarrée !"
    print_info "Application accessible sur http://localhost:8000"
    print_info "Documentation API : http://localhost:8000/docs (si activé)"
}

# Arrêter l'application
stop() {
    print_info "Arrêt de MobilitySoft..."
    docker-compose down
    print_success "Application arrêtée"
}

# Arrêter et supprimer les volumes
clean() {
    print_info "Nettoyage complet (suppression des données)..."
    docker-compose down -v
    print_success "Nettoyage terminé"
}

# Afficher les logs
logs() {
    print_info "Affichage des logs (Ctrl+C pour quitter)..."
    docker-compose logs -f
}

# Rebuild l'image Docker
rebuild() {
    print_info "Reconstruction de l'image Docker..."
    docker-compose build --no-cache
    print_success "Image reconstruite"
}

# Exécuter les tests
test() {
    print_info "Exécution des tests..."
    
    # Vérifier si l'environnement virtuel existe
    if [ ! -d ".venv" ]; then
        print_info "Création de l'environnement virtuel..."
        python3 -m venv .venv
    fi
    
    # Activer l'environnement virtuel
    source .venv/bin/activate
    
    # Installer les dépendances
    print_info "Installation des dépendances..."
    pip install -q -r requirements.txt
    
    # Exécuter les tests
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/mobilitysoft_test_db"
    pytest tests/ -v
    
    print_success "Tests terminés"
}

# Vérifier l'état de l'application
status() {
    print_info "État des conteneurs Docker :"
    docker-compose ps
}

# Afficher l'aide
help() {
    echo "Usage: ./deploy.sh [command]"
    echo ""
    echo "Commandes disponibles :"
    echo "  start    - Démarrer l'application avec Docker Compose"
    echo "  stop     - Arrêter l'application"
    echo "  restart  - Redémarrer l'application"
    echo "  clean    - Arrêter et supprimer toutes les données"
    echo "  logs     - Afficher les logs en temps réel"
    echo "  rebuild  - Reconstruire l'image Docker"
    echo "  test     - Exécuter les tests"
    echo "  status   - Afficher l'état des conteneurs"
    echo "  help     - Afficher cette aide"
}

# Redémarrer l'application
restart() {
    stop
    start
}

# Point d'entrée principal
case "${1:-help}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    clean)
        clean
        ;;
    logs)
        logs
        ;;
    rebuild)
        rebuild
        ;;
    test)
        test
        ;;
    status)
        status
        ;;
    help|*)
        help
        ;;
esac
