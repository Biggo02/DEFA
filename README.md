# DEFA — Finance Responsable

Plateforme web DEFA construite à partir de la maquette fournie : site public, espace client, espace agent, administration et états système.

## Interface actuellement intégrée
- Accueil DEFA et navigation publique
- Simulateur de prêt interactif
- Connexion / inscription / récupération du mot de passe
- 82 familles d’écrans couvertes par le routeur
- Espace client avec tableau de bord, prêt, échéancier et historique
- Assistant de demande de prêt en 8 étapes
- Espace agent avec scanner QR et saisie de paiement
- Espace administration avec vues de gestion
- Reçu/paiement et mise à jour visuelle du solde
- Responsive mobile/tablette/desktop
- Design cohérent avec la maquette : bleu DEFA, sidebar sombre, cartes, badges et tableaux

## Démarrage local
```bash
npm install
npm run dev
```

## Build
```bash
npm run build
```

## Architecture cible production
Le dépôt contient le socle frontend. Pour la mise en production financière, connecter un backend sécurisé avec PostgreSQL, authentification réelle, KYC, stockage documentaire, scoring serveur, transactions immuables, notifications, audit et géolocalisation consentie.

## Sécurité
Aucune localisation secrète ou surveillance permanente n'est prévue. Les informations personnelles et financières doivent être minimisées, protégées et traitées conformément aux obligations applicables en RDC. Les décisions de crédit restent contrôlables par un humain.