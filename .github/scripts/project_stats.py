#!/usr/bin/env python3
"""
Script pour générer des statistiques du projet MobilitySoft
Utile pour le rapport final du Labo 2
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path


def run_command(command):
    """Exécute une commande shell et retourne le résultat"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Erreur: {e}"


def count_lines_of_code():
    """Compte les lignes de code Python"""
    stats = {
        'app': 0,
        'tests': 0,
        'total': 0
    }
    
    for directory in ['app', 'tests']:
        if os.path.exists(directory):
            result = run_command(f"find {directory} -name '*.py' | xargs wc -l | tail -n 1")
            try:
                lines = int(result.split()[0])
                stats[directory] = lines
            except:
                stats[directory] = 0
    
    stats['total'] = stats['app'] + stats['tests']
    return stats


def count_files():
    """Compte les fichiers par type"""
    return {
        'python': run_command("find . -name '*.py' | wc -l"),
        'yaml': run_command("find . -name '*.yml' -o -name '*.yaml' | wc -l"),
        'markdown': run_command("find . -name '*.md' | wc -l"),
        'docker': run_command("find . -name 'Dockerfile' -o -name 'docker-compose*.yml' | wc -l")
    }


def get_docker_image_size():
    """Obtient la taille de l'image Docker si elle existe"""
    result = run_command("docker images mobilitysoft:latest --format '{{.Size}}'")
    return result if result else "N/A (image non construite)"


def get_git_stats():
    """Obtient des statistiques Git"""
    return {
        'commits': run_command("git rev-list --count HEAD"),
        'branches': run_command("git branch -a | wc -l"),
        'contributors': run_command("git log --format='%an' | sort -u | wc -l"),
        'last_commit': run_command("git log -1 --format='%h - %s (%ar)'")
    }


def get_test_stats():
    """Obtient les statistiques des tests"""
    test_files = []
    total_tests = 0
    
    if os.path.exists('tests'):
        for file in Path('tests').glob('test_*.py'):
            result = run_command(f"grep -c 'def test_' {file}")
            try:
                count = int(result)
                test_files.append({
                    'file': file.name,
                    'tests': count
                })
                total_tests += count
            except:
                pass
    
    return {
        'total_tests': total_tests,
        'test_files': len(test_files),
        'details': test_files
    }


def get_dependencies_count():
    """Compte les dépendances Python"""
    if os.path.exists('requirements.txt'):
        result = run_command("cat requirements.txt | grep -v '^#' | grep -v '^$' | wc -l")
        return result
    return "0"


def generate_report():
    """Génère un rapport complet des statistiques"""
    print("=" * 70)
    print("📊 STATISTIQUES DU PROJET MOBILITYSOFT")
    print("=" * 70)
    print()
    
    # Informations générales
    print("🔍 INFORMATIONS GÉNÉRALES")
    print("-" * 70)
    print(f"Date du rapport       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Répertoire de travail : {os.getcwd()}")
    print()
    
    # Statistiques Git
    print("📝 STATISTIQUES GIT")
    print("-" * 70)
    git_stats = get_git_stats()
    print(f"Nombre de commits     : {git_stats['commits']}")
    print(f"Nombre de branches    : {git_stats['branches']}")
    print(f"Contributeurs         : {git_stats['contributors']}")
    print(f"Dernier commit        : {git_stats['last_commit']}")
    print()
    
    # Lignes de code
    print("💻 LIGNES DE CODE")
    print("-" * 70)
    loc = count_lines_of_code()
    print(f"Code application (app/)   : {loc['app']:>6} lignes")
    print(f"Code tests (tests/)       : {loc['tests']:>6} lignes")
    print(f"Total                     : {loc['total']:>6} lignes")
    print()
    
    # Fichiers
    print("📁 FICHIERS PAR TYPE")
    print("-" * 70)
    files = count_files()
    print(f"Fichiers Python (.py)     : {files['python']:>3}")
    print(f"Fichiers YAML             : {files['yaml']:>3}")
    print(f"Fichiers Markdown (.md)   : {files['markdown']:>3}")
    print(f"Fichiers Docker           : {files['docker']:>3}")
    print()
    
    # Tests
    print("🧪 STATISTIQUES DES TESTS")
    print("-" * 70)
    test_stats = get_test_stats()
    print(f"Nombre total de tests     : {test_stats['total_tests']}")
    print(f"Fichiers de tests         : {test_stats['test_files']}")
    print()
    print("Détails par fichier :")
    for detail in test_stats['details']:
        print(f"  - {detail['file']:<30} : {detail['tests']:>2} tests")
    print()
    
    # Dépendances
    print("📦 DÉPENDANCES")
    print("-" * 70)
    deps = get_dependencies_count()
    print(f"Dépendances Python        : {deps}")
    print()
    
    # Docker
    print("🐳 DOCKER")
    print("-" * 70)
    image_size = get_docker_image_size()
    print(f"Taille de l'image         : {image_size}")
    print()
    
    # Workflows CI/CD
    print("🔄 WORKFLOWS CI/CD")
    print("-" * 70)
    workflow_dir = Path(".github/workflows")
    if workflow_dir.exists():
        workflows = list(workflow_dir.glob("*.yml"))
        print(f"Nombre de workflows       : {len(workflows)}")
        print("Liste des workflows :")
        for wf in workflows:
            print(f"  - {wf.name}")
    else:
        print("Aucun workflow trouvé")
    print()
    
    # Documentation
    print("📚 DOCUMENTATION")
    print("-" * 70)
    docs = {
        'README.md': os.path.exists('README.md'),
        'SETUP.md': os.path.exists('SETUP.md'),
        'QUICKSTART.md': os.path.exists('QUICKSTART.md'),
        'RECAP.md': os.path.exists('RECAP.md'),
        'RAPPORT_LABO2.md': os.path.exists('RAPPORT_LABO2.md')
    }
    for doc, exists in docs.items():
        status = "✅" if exists else "❌"
        print(f"{status} {doc}")
    print()
    
    # Récapitulatif
    print("=" * 70)
    print("✨ RÉCAPITULATIF")
    print("=" * 70)
    print(f"✅ {loc['total']} lignes de code")
    print(f"✅ {test_stats['total_tests']} tests automatisés")
    print(f"✅ {git_stats['commits']} commits")
    print(f"✅ {len(workflows) if workflow_dir.exists() else 0} workflows CI/CD")
    print(f"✅ {sum(1 for v in docs.values() if v)} documents de référence")
    print()
    print("🚀 Projet prêt pour la démo !")
    print("=" * 70)


def generate_json_report():
    """Génère un rapport JSON pour traitement automatisé"""
    report = {
        'generated_at': datetime.now().isoformat(),
        'git': get_git_stats(),
        'code': count_lines_of_code(),
        'files': count_files(),
        'tests': get_test_stats(),
        'dependencies': get_dependencies_count(),
        'docker_image_size': get_docker_image_size()
    }
    
    with open('project_stats.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("\n💾 Rapport JSON sauvegardé dans : project_stats.json")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        generate_json_report()
    else:
        generate_report()
        
        # Proposer de générer aussi le JSON
        print("\n💡 Pour générer un rapport JSON, exécutez :")
        print("   python .github/scripts/project_stats.py --json")
