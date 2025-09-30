# 🚀 Deployment Guide - TechCorp Inventory System

Ce guide vous explique comment déployer et développer avec le TechCorp Inventory System.

## 🏗️ Structure de Déploiement

- `docker-compose.dev.yml` : Configuration pour le développement
- `../docker-compose.yml` (racine) : Configuration de production/base

## 🔧 Développement Local

### Prérequis
- Docker et Docker Compose installés
- Python 3.11+ (pour les tests locaux)

### Démarrage rapide - Développement

```bash
# Depuis le répertoire build/deploy/
docker-compose -f docker-compose.dev.yml up --build
```

L'application sera accessible sur : http://localhost:3206

### Fonctionnalités du mode développement
- **Hot reload** : Les changements de code sont immédiatement pris en compte
- **Volume mounting** : Code source monté depuis `../app/`
- **Logs détaillés** : Affichage complet des logs de développement
- **Variables d'environnement** : Configuration de développement activée

## 🚀 Production

### Déploiement depuis la racine

```bash
# Depuis la racine du projet
docker-compose up -d --build
```

### Différences production vs développement
- **Production** : Image optimisée, pas de hot reload
- **Développement** : Volume mounting, logs verbeux, auto-reload

## 🧪 Tests

```bash
# Installer les dépendances de test
pip install -r ../app/requirements.txt

# Exécuter tous les tests
python ../app/tests/main.py
```

## 🔐 Comptes de Test

| Username | Password | Rôle | Description |
|----------|----------|------|-------------|
| admin | password123 | Admin | Accès complet + données personnelles |
| manager | password123 | Manager | Gestion équipe |
| employee | password123 | Employee | Accès de base |

## 🐛 Dépannage

### Container ne démarre pas
```bash
# Vérifier les logs
docker-compose logs

# Nettoyer et redémarrer
docker-compose down -v
docker-compose up --build
```

### Base de données corrompue
```bash
# Supprimer les volumes
docker-compose down -v
# Redémarrer (recréation automatique)
docker-compose up
```

### Tests échouent
```bash
# Vérifier les dépendances
pip install -r ../app/requirements.txt

# Tests individuels
cd ../app/tests/
python test_app.py
```

## 📱 Endpoints de l'API

- `GET /` : Page d'accueil
- `GET /login` : Formulaire de connexion
- `POST /login` : Traitement connexion
- `GET /dashboard` : Tableau de bord utilisateur
- `GET /profile` : Profil utilisateur (avec données personnelles pour admin)
- `GET /inventory` : Gestion inventaire
- `GET /forgot_password` : Demande de reset de mot de passe
- `POST /reset_password` : Traitement reset (⚠️ vulnérable)
- `GET /health` : Health check pour Docker

## 🔥 Challenge de Sécurité

Cette application contient **intentionnellement** une vulnérabilité de type "Password Reset Broken Logic".

**Objectif pédagogique** : Comprendre comment exploiter une validation insuffisante dans le processus de reset de mot de passe.