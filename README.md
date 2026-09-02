# DEFA — Finance Responsable

DEFA est une plateforme de demande, analyse, octroi et suivi de micro-prêts. Le frontend est désormais **100 % Django Templates + HTML + CSS** : React/Vite n'est plus utilisé pour servir l'interface.

## Stack
- Django 5.2
- Django REST Framework
- PostgreSQL en environnement Docker / SQLite possible en développement local
- HTML + Django Templates + CSS responsive
- Sessions Django pour l'interface web
- API REST conservée pour les intégrations
- Docker + Gunicorn pour le déploiement

## Fonctionnalités
- Site public : accueil, fonctionnement, simulateur, éligibilité, sécurité, FAQ, contact
- Inscription / connexion
- Espace client
- Dossier de prêt complet : identité, adresse, activité, revenus, commerce, références, documents et consentement de localisation
- Soumission et suivi du dossier
- Scoring indicatif et vérification humaine
- Espace agent : clients assignés, visites, QR, paiements et recouvrement
- Administration : demandes, KYC, documents, clients, prêts, paiements, alertes, audit et paramètres
- Contrats et échéanciers
- Paiements en espèces avec reçu et journal d'audit
- États système et page 404 personnalisée

## Règle de tarification DEFA
- Minimum : **100 000 FC**
- Incrément : **100 000 FC** uniquement
- Frais : **12 % du capital**
- Total à rembourser : **capital + 12 %**

Exemples :
- 100 000 FC → 12 000 FC de frais → 112 000 FC
- 200 000 FC → 24 000 FC de frais → 224 000 FC
- 500 000 FC → 60 000 FC de frais → 560 000 FC

La validation est faite côté serveur. Le total d'un prêt est recalculé par Django avant sauvegarde afin d'éviter qu'une valeur envoyée par le navigateur puisse remplacer les conditions DEFA.

## Démarrage local
```bash
cd backend
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Puis ouvrir le port **8000** du Codespace.

## Tests
```bash
cd backend
python manage.py test
```

## Docker
Depuis la racine :
```bash
docker compose up --build
```

Le service web écoute sur le port 8000 et utilise Gunicorn dans le conteneur. Avant production, remplacer les secrets de développement et configurer PostgreSQL, HTTPS, domaines autorisés, stockage privé des documents et sauvegardes.

## Architecture
```text
Navigateur
   │
   ▼
Django Templates / HTML / CSS
   │
   ├── Sessions Django
   ├── Vues métier
   └── API REST
           │
           ▼
       PostgreSQL
```

## Sécurité
- CSRF Django pour les formulaires
- contrôle d'accès par rôle
- validation serveur des montants et données
- documents liés au profil et non exposés comme données publiques
- consentement explicite pour la localisation
- journal d'audit des opérations sensibles
- paiements enregistrés comme nouvelles transactions, sans écrasement silencieux
- aucune surveillance clandestine

Les procédures de crédit, frais, garanties, recouvrement, traitement des données et documents contractuels doivent être validées juridiquement et configurées conformément à la réglementation applicable en RDC avant toute mise en production.
