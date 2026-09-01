# DEFA — Cadre réglementaire RDC (pré-production)

> Document de préparation technique et produit. Il ne remplace pas l'avis d'un avocat ni l'agrément/validation de la Banque Centrale du Congo.

## 1. Qualification à confirmer

DEFA envisage l'octroi direct de crédits à des clients en RDC. La BCC distingue notamment les entreprises de micro-crédit, qui effectuent du crédit direct sans collecte de l'épargne du public, et les sociétés de microfinance. L'activité de microfinance est encadrée par la Loi n°11/020 du 15 septembre 2011 et, selon la catégorie retenue, par la Loi n°22/069 du 27 décembre 2022 et les instructions BCC applicables.

Avant tout prêt réel, la structure juridique de DEFA, son activité exacte, ses sources de financement, son modèle d'agents et son mode de recouvrement doivent être validés par un conseil juridique congolais et la BCC si nécessaire.

## 2. Exigences produit à intégrer

- KYC complet et traçable.
- Vérification de l'identité et des informations fournies.
- Évaluation de la capacité de remboursement et prévention du surendettement.
- Information claire sur le coût total, les conditions et l'échéancier.
- Contrat consultable avant acceptation.
- Confidentialité des données personnelles.
- Journal d'audit des décisions et paiements.
- Mécanisme de plainte/réclamation.
- Procédure de recouvrement documentée, respectueuse et non coercitive.
- Contrôles LBC/FT applicables au modèle retenu.

## 3. Architecture de conformité DEFA

Client → KYC → analyse solvabilité → vérification terrain → décision → contrat → décaissement → échéancier → paiements → rapprochement → recouvrement → clôture.

Chaque étape doit être horodatée et attribuée à un utilisateur autorisé.

## 4. Localisation

La localisation ne doit jamais être captée secrètement. DEFA doit demander un consentement explicite, indiquer la finalité, limiter la collecte à ce qui est nécessaire et prévoir une politique de conservation/suppression adaptée.

## 5. Argent et paiements

Les montants, soldes, échéanciers, paiements et reçus finaux doivent être calculés et validés côté serveur. Le frontend ne doit jamais pouvoir modifier directement un solde ou déclarer un paiement comme définitif.

## 6. Go-live gate

Ne pas décaisser de fonds à de vrais clients tant que :

1. le statut réglementaire/agrément applicable n'est pas confirmé ;
2. les contrats et conditions tarifaires n'ont pas été validés juridiquement ;
3. les procédures KYC/LBC-FT et de protection des clients ne sont pas approuvées ;
4. le staging E2E est validé ;
5. les contrôles d'accès et sauvegardes sont testés ;
6. le mécanisme de plaintes et de recouvrement est opérationnel.
