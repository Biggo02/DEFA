# PROMPT COMPLET — CONCEPTION ET DÉVELOPPEMENT DE DEFA

## 1. RÔLE

Tu es un architecte logiciel senior, expert UX/UI fintech, développement full-stack, sécurité applicative, KYC, scoring de crédit, gestion des prêts, recouvrement terrain, géolocalisation et conception de plateformes SaaS professionnelles en RDC.

Ta mission est de concevoir et développer **DEFA — Finance Responsable**, une plateforme web professionnelle de demande, analyse, octroi et suivi de micro-prêts, avec une priorité absolue donnée à la sélection des emprunteurs solvables, à la vérification physique, à la traçabilité et au recouvrement responsable.

Le projet doit être réellement fonctionnel, pas une simple maquette. Toutes les pages, tous les boutons, formulaires, filtres, tableaux, statuts, QR codes, cartes, calculs et workflows doivent fonctionner.

---

## 2. RÉFÉRENCE UI OBLIGATOIRE

Utilise la maquette fournie comme **référence visuelle principale et stricte**. Respecte l'ordre, les noms, la structure et l'intention des 82 écrans présentés dans la maquette.

Ne supprime aucune page de la liste. Ne fusionne pas arbitrairement les pages. Chaque écran doit avoir sa propre route et son propre état fonctionnel, même lorsque plusieurs écrans utilisent le même composant.

L'interface doit conserver l'esprit de la maquette :
- design fintech moderne et professionnel ;
- blanc et bleu comme base ;
- vert pour les validations et situations saines ;
- rouge pour les risques, refus et retards ;
- orange pour certains avertissements ;
- cartes à coins légèrement arrondis ;
- tableaux propres ;
- sidebar sombre dans les espaces Client, Agent et Administration ;
- excellente lisibilité ;
- responsive mobile/tablette/desktop ;
- icônes modernes ;
- graphiques et indicateurs visuels ;
- cartes géographiques ;
- QR codes ;
- badges de statut ;
- parcours guidés et barres de progression.

Le logo doit afficher **DEFA** avec la signature **Finance Responsable**.

---

## 3. POSITIONNEMENT

DEFA permet à une personne de demander un prêt. Le système analyse son profil avant toute décision.

La priorité commerciale initiale est donnée aux :
1. petits commerçants ;
2. indépendants ayant une activité vérifiable ;
3. salariés disposant de preuves de revenus ;
4. autres demandeurs présentant une capacité de remboursement démontrable.

DEFA ne doit jamais présenter l'approbation comme automatique. Le système collecte les informations, calcule un score indicatif, vérifie les documents et permet à un agent/administrateur d'effectuer les contrôles nécessaires avant décision.

---

## 4. PRINCIPES DE SÉCURITÉ ET DE CONFORMITÉ

Construire le système selon les principes suivants :
- consentement explicite pour la collecte et l'utilisation des données personnelles ;
- aucune géolocalisation secrète ou à l'insu du client ;
- demander l'autorisation du navigateur avant toute localisation ;
- enregistrer la date, l'heure et le contexte de chaque collecte de localisation ;
- minimiser les données collectées ;
- chiffrement des données sensibles en transit et au repos lorsque possible ;
- contrôle d'accès par rôle ;
- authentification robuste ;
- journal d'audit immuable ;
- protection CSRF/XSS/SQL injection ;
- limitation des tentatives de connexion ;
- sauvegardes ;
- validation des fichiers ;
- antivirus/contrôle MIME pour les documents uploadés ;
- ne jamais exposer publiquement les pièces d'identité ;
- ne jamais afficher les coordonnées sensibles d'un client à un autre client ;
- ne jamais permettre à un agent de modifier rétroactivement un paiement sans traçabilité ;
- séparation stricte entre demandeur, agent et administrateur.

Pour les situations de défaut de paiement, prévoir uniquement des mécanismes légaux et responsables : suivi du dossier, notifications, assignation d'un agent, visites autorisées et documentation des actions. **Aucune fonction de traçage clandestin, espionnage ou surveillance à l'insu du client.**

Prévoir dans l'application des textes indiquant que les procédures d'octroi, taux, frais, garanties, recouvrement et traitement des données doivent être configurés conformément à la réglementation applicable en RDC et validés juridiquement avant mise en production.

---

# 5. ARCHITECTURE TECHNIQUE

Utiliser une architecture moderne, maintenable et économique.

Stack recommandée :
- Frontend : React + TypeScript + Vite ;
- UI : Tailwind CSS + composants accessibles ;
- Icônes : Lucide ;
- Graphiques : Recharts ;
- Cartes : Leaflet + OpenStreetMap ;
- QR : bibliothèque QR fiable côté client/serveur ;
- Backend : Django + Django REST Framework ;
- Base de données : PostgreSQL ;
- Authentification : sessions sécurisées ou JWT avec rotation/expiration appropriée ;
- stockage des documents : stockage privé ;
- API REST versionnée ;
- tests automatisés ;
- Docker pour développement et déploiement ;
- GitHub Actions pour CI ;
- variables sensibles uniquement dans `.env`.

Si l'environnement de génération impose une autre stack, conserver les mêmes fonctionnalités, routes, données, rôles et principes d'architecture.

---

# 6. RÔLES

## Client
Peut :
- créer son compte ;
- compléter son profil ;
- soumettre une demande ;
- fournir identité, emploi, revenus, charges, commerce, domicile, localisation et références ;
- consulter le statut ;
- consulter les conditions proposées ;
- consulter son contrat ;
- suivre le capital restant ;
- consulter l'échéancier ;
- voir chaque paiement enregistré ;
- consulter/télécharger ses reçus ;
- recevoir des notifications ;
- demander de l'aide.

## Agent
Peut :
- consulter les clients assignés ;
- voir les visites à effectuer ;
- utiliser la carte ;
- naviguer vers un client ;
- scanner le QR d'un dossier ;
- consulter uniquement les informations nécessaires à son intervention ;
- enregistrer un paiement reçu ;
- faire signer le client selon le processus défini ;
- générer un reçu ;
- enregistrer une visite et son résultat ;
- produire son rapport quotidien.

## Administrateur
Peut :
- analyser les demandes ;
- vérifier KYC ;
- contrôler les documents ;
- analyser le scoring ;
- approuver/refuser/suspendre une demande ;
- définir le montant, la durée et les conditions autorisées ;
- créer et gérer les contrats ;
- gérer les prêts ;
- suivre les paiements ;
- affecter les agents ;
- suivre le recouvrement ;
- consulter la carte globale ;
- gérer les alertes ;
- gérer les paramètres de scoring ;
- consulter les rapports ;
- consulter le journal d'audit ;
- gérer les utilisateurs et permissions.

---

# 7. MODÈLE DE DONNÉES MINIMAL

Créer au minimum les entités suivantes :

- User
- Role
- ClientProfile
- IdentityVerification
- Address
- Employment
- Income
- Expense
- Business
- BusinessLocation
- Reference
- UploadedDocument
- LoanApplication
- CreditScore
- Verification
- VerificationVisit
- LoanOffer
- Loan
- LoanSchedule
- Installment
- Payment
- PaymentReceipt
- Contract
- Agent
- AgentAssignment
- CollectionVisit
- LocationConsent
- LocationRecord
- Notification
- FraudAlert
- AuditLog
- SystemSetting

Chaque entité doit avoir identifiant unique, timestamps, statut lorsque nécessaire et relations cohérentes.

---

# 8. WORKFLOW PRINCIPAL DU CLIENT

1. Le visiteur arrive sur l'accueil.
2. Il consulte les types de financement disponibles.
3. Il utilise le simulateur.
4. Il consulte les conditions d'éligibilité.
5. Il crée un compte.
6. Il vérifie son numéro/contact selon le mécanisme disponible.
7. Il complète son identité.
8. Il fournit ses informations professionnelles.
9. Il fournit revenus et charges.
10. S'il possède un commerce, il renseigne le commerce et sa localisation.
11. Il renseigne son domicile.
12. Il fournit les références autorisées.
13. Il téléverse les documents demandés.
14. Il consent explicitement aux vérifications nécessaires.
15. Il peut partager sa localisation uniquement après consentement.
16. Le système contrôle la complétude.
17. Le système calcule un score indicatif selon les paramètres DEFA.
18. La demande passe à **En vérification**.
19. Un agent peut être assigné pour vérification terrain.
20. L'administrateur examine le dossier.
21. L'administrateur approuve, demande des informations complémentaires ou refuse.
22. Si approuvé, une proposition de prêt est créée.
23. Le client consulte les conditions.
24. Le contrat est accepté/signé selon le processus légal retenu.
25. Le prêt devient actif.
26. Un échéancier est généré.
27. Les paiements sont enregistrés au fur et à mesure.
28. Le solde et l'historique se mettent automatiquement à jour.
29. À la fin du remboursement, le prêt passe à **Remboursé**.

---

# 9. SIMULATEUR

Le simulateur doit permettre de sélectionner :
- montant souhaité ;
- durée ;
- fréquence de remboursement ;
- date indicative de début.

Afficher dynamiquement :
- montant emprunté ;
- frais/intérêts selon paramètres configurables ;
- montant total à rembourser ;
- montant estimatif par échéance ;
- nombre d'échéances ;
- avertissement indiquant que la simulation n'est pas une approbation.

Ne jamais coder en dur un taux légal ou commercial définitif. Les paramètres doivent être administrables.

---

# 10. SCORING

Créer un moteur de scoring configurable et transparent.

Exemples de facteurs :
- identité vérifiée ;
- stabilité professionnelle ;
- ancienneté du commerce ;
- revenus moyens ;
- charges ;
- ratio dette/revenu ;
- stabilité de l'adresse ;
- qualité des références ;
- historique de remboursement DEFA ;
- cohérence des informations ;
- résultats de vérification terrain ;
- signaux de fraude.

Afficher un score sous forme de catégorie et de pourcentage indicatif, par exemple :
- Excellent ;
- Bon ;
- Moyen ;
- À vérifier ;
- Risqué.

Le scoring ne doit pas être présenté comme une garantie de remboursement. L'administrateur garde la décision finale.

---

# 11. GÉOLOCALISATION

La localisation sert à faciliter les vérifications et visites autorisées.

Fonctions :
- demander explicitement la permission ;
- afficher une carte ;
- capturer latitude/longitude après consentement ;
- enregistrer précision et timestamp ;
- permettre au client de confirmer le point ;
- distinguer domicile et commerce ;
- permettre à l'agent de voir les points des clients qui lui sont assignés ;
- proposer un itinéraire ;
- ne pas suivre continuellement le client sans consentement et base légitime.

---

# 12. QR CODE

Chaque dossier de prêt actif peut avoir un QR code unique.

Lorsqu'un agent scanne le QR :
- authentifier l'agent ;
- vérifier que le dossier est valide ;
- afficher le dossier minimal nécessaire ;
- afficher le montant initial ;
- afficher le total restant ;
- afficher les échéances ;
- afficher les retards ;
- afficher le dernier paiement ;
- permettre l'enregistrement d'un nouveau paiement si l'agent est autorisé.

Après paiement :
- recalculer automatiquement le solde ;
- mettre à jour l'échéance ;
- enregistrer date/heure/agent ;
- générer le reçu ;
- créer une entrée d'audit ;
- afficher la confirmation au client et à l'agent.

---

# 13. PAIEMENTS ET RECOUVREMENT

Le remboursement peut être fractionné selon le contrat.

Chaque paiement doit conserver :
- ID ;
- prêt ;
- client ;
- agent ;
- montant ;
- date ;
- mode ;
- référence ;
- signature/confirmation selon le processus ;
- reçu ;
- timestamp serveur ;
- audit.

Ne jamais permettre qu'un paiement soit simplement écrasé. Toute correction doit créer une trace de correction/annulation.

Le dashboard client doit toujours montrer :
- montant initial ;
- montant total dû ;
- total déjà payé ;
- restant à payer ;
- prochaine échéance ;
- échéances en retard ;
- pourcentage remboursé ;
- historique complet.

---

# 14. WHATSAPP

Après soumission d'une demande, prévoir une action permettant à l'équipe DEFA de contacter le client via WhatsApp si le canal est disponible.

Ne pas utiliser d'API WhatsApp payante sans nécessité. Prévoir une configuration permettant soit un lien `wa.me`, soit une intégration officielle ultérieure.

Le numéro ne doit pas être exposé publiquement à des tiers.

---

# 15. LES 82 PAGES À IMPLÉMENTER

## SITE PUBLIC

### 1. Accueil
Hero DEFA, message de confiance, CTA "Demander un prêt", CTA "Simuler un prêt", avantages, statistiques, fonctionnement, sécurité, FAQ courte et footer.

### 2. Comment ça marche
Parcours en étapes : demande → vérification → décision → contrat → remboursement.

### 3. Simulateur de prêt
Formulaire de simulation et résultat dynamique.

### 4. Conditions d'éligibilité
Critères, documents, profils privilégiés, avertissements et FAQ.

### 5. Sécurité & confiance
KYC, vérifications, protection des données, contrôles, audit et recouvrement responsable.

### 6. FAQ
Accordéons de questions/réponses.

### 7. À propos de DEFA
Mission, vision, finance responsable, équipe/illustration, valeurs.

### 8. Contact
Formulaire, coordonnées configurables, horaires et CTA WhatsApp.

### 9. Connexion
Identifiant/contact, mot de passe, récupération, sécurité.

### 10. Inscription
Création de compte, consentements, validation.

### 11. Mot de passe oublié
Demande de récupération et confirmation.

---

## ESPACE CLIENT

### 12. Tableau de bord
Résumé financier, statut du prêt, prochaine échéance, progression, demandes récentes, notifications et raccourci vers nouvelle demande.

### 13. Nouvelle demande de prêt
Wizard multi-étapes avec barre de progression et sauvegarde temporaire.

### 14. Identité / KYC
Informations personnelles, pièce d'identité, selfie/photo si légalement nécessaire, statut de vérification.

### 15. Situation professionnelle
Salarié, indépendant, commerçant, profession, employeur, ancienneté, preuves.

### 16. Revenus et charges
Revenus réguliers/irréguliers, charges, dettes existantes et calcul de capacité.

### 17. Commerce
Nom, type d'activité, ancienneté, chiffre d'affaires estimé, preuves et photos autorisées.

### 18. Domicile
Adresse structurée, ancienneté, preuve de domicile et contact d'urgence si légalement requis.

### 19. Géolocalisation
Consentement, carte, position du commerce/domicile, précision et confirmation.

### 20. Références
Ajout et validation des références selon les règles DEFA.

### 21. Documents
Liste des documents requis, upload, aperçu, statut de vérification.

### 22. Résumé de la demande
Toutes les informations, corrections, consentements et bouton de soumission.

### 23. Statut de la demande
Timeline : brouillon → soumise → en vérification → informations demandées → approuvée/refusée.

### 24. Détails du prêt
Montant, durée, total dû, conditions, dates, statut, contrat et QR.

### 25. Échéancier
Tableau des échéances, dates, montants, payé, restant, retard.

### 26. Historique des paiements
Liste filtrable des paiements.

### 27. Détail d'un paiement
Reçu, montant, date, agent, référence, statut.

### 28. Mes reçus
Galerie/liste des reçus avec recherche et téléchargement.

### 29. Visualisation d'un reçu
Reçu professionnel DEFA avec QR de vérification et informations essentielles.

### 30. Notifications
Demandes, approbation, échéances, paiements, retards, informations manquantes.

### 31. Profil
Données personnelles, photo, coordonnées et informations générales.

### 32. Sécurité
Mot de passe, sessions, appareils, authentification renforcée et consentements.

### 33. Aide
FAQ, assistance, contact DEFA et aide sur le remboursement.

---

## ESPACE AGENT

### 34. Dashboard agent
Clients assignés, visites du jour, recouvrement du jour, montants encaissés, alertes.

### 35. Clients assignés
Tableau des clients avec recherche, filtres et statuts.

### 36. Fiche client
Informations nécessaires à la mission, prêt, échéancier, historique et visites.

### 37. Planning des visites
Calendrier/liste des visites avec statut.

### 38. Détail d'une visite
Client, adresse autorisée, motif, horaire, notes, résultat et preuve de passage.

### 39. Carte des clients
Carte avec marqueurs des clients assignés, filtres par statut.

### 40. Navigation / tournée
Carte avec itinéraire de tournée et ordre recommandé.

### 41. Scanner QR
Interface caméra/scanner avec validation.

### 42. Dossier après scan
Dossier de prêt minimal nécessaire, restant dû et actions autorisées.

### 43. Enregistrer paiement
Montant, mode, référence, confirmation et signature selon processus.

### 44. Confirmation paiement
Confirmation visuelle avec nouveau solde et génération du reçu.

### 45. Reçu généré
Reçu professionnel avec QR et informations de transaction.

### 46. Historique paiements
Paiements enregistrés par l'agent avec filtres.

### 47. Recouvrement
Clients en retard, priorité, montant restant, dernières visites et actions.

### 48. Rapport quotidien
Visites, paiements, montants, incidents, commentaires et soumission.

### 49. Profil agent
Profil, zone, statut, sécurité et paramètres.

---

## ADMINISTRATION

### 50. Dashboard général
KPI : demandes, prêts actifs, montant prêté, remboursements, retards, risque, agents actifs, alertes.

### 51. Demandes de prêt
Tableau complet des demandes avec filtres et statuts.

### 52. Analyse d'une demande
Vue 360° : profil, KYC, revenus, commerce, domicile, références, documents, scoring et historique.

### 53. Score de crédit
Score, facteurs, alertes, capacité estimée et explications.

### 54. Vérification KYC
Files de vérification, documents, statut, validation/rejet avec motif.

### 55. Documents
Gestion sécurisée des documents et statuts.

### 56. Clients
Recherche, filtres, segmentation, statut et historique.

### 57. Fiche client complète
Vue 360° complète avec prêt(s), paiements, vérifications, visites, risques et audit.

### 58. Prêts
Tous les prêts avec filtres et statuts.

### 59. Détail d'un prêt
Montant, contrat, échéancier, paiements, retards, agent, QR, audit.

### 60. Échéanciers
Gestion et consultation des échéanciers.

### 61. Paiements
Liste de toutes les transactions avec filtres et export autorisé.

### 62. Recouvrement
Portefeuille en retard, priorités, affectations et suivi.

### 63. Agents
Liste, statut, zone, performance et clients assignés.

### 64. Visites terrain
Toutes les visites, résultats, dates, agents et preuves autorisées.

### 65. Carte générale
Carte des demandes/clients/agents selon les permissions, avec filtres et confidentialité.

### 66. Alertes fraude
Incohérences, doublons, documents suspects, comportements anormaux et alertes à investiguer.

### 67. Scoring / paramètres
Gestion des règles, pondérations, seuils et paramètres de prêt.

### 68. Notifications
Templates, événements, historique et paramètres.

### 69. Rapports
Rapports financiers, risque, recouvrement, agents, portefeuille et activité.

### 70. Journal d'audit
Toutes les actions sensibles : connexion, modification, validation, paiement, décision, affectation.

### 71. Utilisateurs
Comptes, rôles, statut, permissions et sécurité.

### 72. Paramètres DEFA
Identité, paramètres commerciaux, produits de prêt, notifications, sécurité et configuration.

### 73. Sécurité
Politiques, sessions, accès, événements suspects, paramètres de sécurité.

---

## ÉTATS PARTICULIERS / PAGES SYSTÈME

### 74. Demande en cours
Illustration, statut et prochaine action.

### 75. Informations manquantes
Liste précise des informations à fournir avec CTA.

### 76. Approuvée
Confirmation de l'approbation, conditions proposées et prochaine étape.

### 77. Refusée
Message respectueux, motif générique/autorisé, possibilité de consulter l'aide et, si la politique le permet, nouvelle demande ultérieure.

### 78. Prêt en retard
Montant en retard, échéances concernées, actions possibles et contact DEFA.

### 79. Paiement partiel
Montant reçu, restant de l'échéance, nouveau solde.

### 80. Prêt remboursé
Confirmation, total remboursé, date de clôture et reçu final.

### 81. Compte suspendu
Raison générale, assistance et procédure de réactivation.

### 82. Erreur / 404
Page DEFA professionnelle avec illustration, message et retour à l'accueil.

---

# 16. NAVIGATION

## Site public
Header : logo DEFA | Accueil | Comment ça marche | Simulateur | Éligibilité | Sécurité | FAQ | À propos | Contact | Connexion | Inscription.

## Client
Sidebar :
- Tableau de bord
- Nouvelle demande
- Mes demandes
- Mon prêt
- Échéancier
- Paiements
- Reçus
- Notifications
- Profil
- Sécurité
- Aide
- Déconnexion

## Agent
Sidebar :
- Dashboard
- Clients assignés
- Visites
- Carte
- Tournée
- Scanner QR
- Paiements
- Recouvrement
- Rapports
- Profil
- Déconnexion

## Administration
Sidebar :
- Dashboard
- Demandes
- KYC
- Documents
- Clients
- Prêts
- Échéanciers
- Paiements
- Recouvrement
- Agents
- Visites terrain
- Carte
- Alertes fraude
- Scoring
- Notifications
- Rapports
- Audit
- Utilisateurs
- Paramètres
- Sécurité
- Déconnexion

---

# 17. DESIGN SYSTEM

Créer un design system centralisé :
- couleurs DEFA ;
- typographie ;
- espacements ;
- boutons ;
- champs ;
- selects ;
- cartes ;
- badges ;
- modales ;
- tableaux ;
- pagination ;
- alertes ;
- toasts ;
- loaders ;
- skeletons ;
- empty states ;
- états d'erreur ;
- composants carte ;
- composants QR ;
- composants upload ;
- timeline ;
- graphiques.

Le rendu doit être cohérent avec la maquette fournie, sans reproduire de manière servile des éléments appartenant à une marque tierce.

---

# 18. RESPONSIVE

Toutes les pages doivent fonctionner sur :
- téléphone ;
- tablette ;
- ordinateur.

Sur mobile :
- sidebar transformée en menu ;
- tableaux transformés en cartes ou scroll horizontal contrôlé ;
- formulaires en une colonne ;
- boutons facilement utilisables au doigt ;
- scanner QR adapté à la caméra ;
- cartes adaptées à la taille de l'écran.

---

# 19. ACCESSIBILITÉ

Respecter autant que possible WCAG :
- contrastes ;
- labels explicites ;
- navigation clavier ;
- focus visible ;
- messages d'erreur accessibles ;
- textes alternatifs ;
- tailles de zones tactiles adaptées.

---

# 20. ÉTATS ET VALIDATIONS

Chaque formulaire doit gérer :
- vide ;
- saisie valide ;
- saisie invalide ;
- champ obligatoire ;
- chargement ;
- succès ;
- erreur serveur ;
- fichier refusé ;
- session expirée.

Chaque action sensible doit demander confirmation et être auditée.

---

# 21. SEED / DONNÉES DE DÉMONSTRATION

Créer des données de démonstration réalistes mais fictives :
- clients ;
- agents ;
- demandes ;
- prêts ;
- échéances ;
- paiements ;
- visites ;
- alertes ;
- notifications.

Ne jamais utiliser de vraies pièces d'identité ou données personnelles.

Créer des comptes de démonstration documentés dans README, sans secrets réels.

---

# 22. API

Créer des endpoints REST propres pour :
- auth ;
- profil ;
- KYC ;
- documents ;
- demandes ;
- scoring ;
- offres ;
- contrats ;
- prêts ;
- échéanciers ;
- paiements ;
- reçus ;
- agents ;
- visites ;
- géolocalisation ;
- notifications ;
- alertes ;
- rapports ;
- audit ;
- paramètres.

Appliquer pagination, filtrage, permissions, validation et gestion des erreurs.

---

# 23. TESTS

Créer des tests pour :
- inscription ;
- connexion ;
- permissions ;
- soumission d'une demande ;
- validation KYC ;
- scoring ;
- approbation ;
- création du prêt ;
- génération d'échéancier ;
- paiement ;
- recalcul du solde ;
- QR ;
- permissions agent ;
- recouvrement ;
- audit ;
- géolocalisation avec consentement ;
- erreurs 404/403/500.

---

# 24. LIVRABLES

Le dépôt doit contenir :
- frontend complet ;
- backend complet ;
- modèles ;
- migrations ;
- API ;
- composants UI ;
- toutes les 82 routes ;
- données de démonstration ;
- tests ;
- README ;
- `.env.example` ;
- Docker ;
- CI GitHub Actions ;
- documentation d'installation ;
- documentation des rôles ;
- documentation de l'architecture ;
- documentation du scoring ;
- documentation du workflow de paiement ;
- documentation de sécurité.

---

# 25. RÈGLE FONDAMENTALE DE DÉVELOPPEMENT

**Ne crée pas seulement des écrans statiques.** Chaque écran doit être relié à un état ou à une donnée réaliste.

Exemples :
- cliquer sur "Demander un prêt" ouvre réellement le wizard ;
- terminer le wizard crée réellement une demande ;
- le statut passe réellement à "En vérification" ;
- l'administrateur voit réellement la demande ;
- une approbation crée réellement une offre/prêt ;
- l'échéancier est réellement calculé ;
- un agent peut réellement scanner un QR de démonstration ;
- un paiement modifie réellement le solde ;
- le dashboard client reflète réellement le paiement ;
- un prêt remboursé passe réellement à "Remboursé" ;
- toutes les actions sensibles apparaissent dans l'audit.

---

# 26. ORDRE D'EXÉCUTION

1. Inspecter le dépôt et confirmer son état.
2. Initialiser proprement l'architecture.
3. Créer le design system.
4. Créer le backend et les modèles.
5. Créer l'authentification et les rôles.
6. Créer les API.
7. Créer le site public.
8. Créer l'espace client.
9. Créer l'espace agent.
10. Créer l'administration.
11. Créer les états système.
12. Connecter toutes les données.
13. Ajouter les seed data.
14. Ajouter tests et validation.
15. Ajouter Docker/CI.
16. Exécuter les tests.
17. Corriger toutes les erreurs.
18. Vérifier les 82 routes une par une.
19. Vérifier responsive et navigation.
20. Fournir un README final avec instructions de lancement.

---

# 27. CRITÈRE FINAL D'ACCEPTATION

Le projet est considéré terminé uniquement lorsque :

- les 82 pages de la maquette existent ;
- les noms et l'ordre des pages correspondent à la maquette ;
- les trois espaces Client / Agent / Administration sont séparés ;
- les permissions sont réellement appliquées ;
- une demande complète peut être créée de bout en bout ;
- une demande peut être vérifiée ;
- une décision peut être prise ;
- un prêt peut être créé ;
- un échéancier peut être généré ;
- un paiement peut être enregistré ;
- le solde se met automatiquement à jour ;
- un reçu avec QR peut être généré ;
- l'agent peut retrouver un dossier par QR ;
- les visites et le recouvrement sont traçables ;
- la localisation est basée sur un consentement explicite ;
- aucun mécanisme de surveillance clandestine n'est présent ;
- les actions sensibles sont auditées ;
- les erreurs principales sont gérées ;
- les tests passent ;
- le projet peut être lancé depuis une nouvelle installation en suivant le README.

**Construis DEFA comme un produit fintech réel, professionnel, sécurisé, maintenable et adapté au contexte de la RDC, tout en respectant fidèlement la structure et les 82 écrans de la maquette fournie.**
