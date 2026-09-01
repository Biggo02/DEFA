// Central manifest consumed by the existing router. Keeping this separate makes
// the migration from the legacy monolithic entry point incremental and safe.
export const DEFA_ROUTE_MANIFEST = Object.freeze({
  client: {
    '/app/tableau-de-bord': 'dashboard',
    '/app/nouvelle-demande-de-pret': 'loan-application',
    '/app/statut-de-la-demande': 'loan-status',
    '/app/details-du-pret': 'loan-detail',
    '/app/echeancier': 'schedule',
    '/app/historique-des-paiements': 'payment-history',
    '/app/mes-recus': 'receipts',
  },
  agent: {
    '/app/scanner-qr': 'qr-scanner',
    '/app/dossier-apres-scan': 'scanned-loan',
    '/app/enregistrer-paiement': 'payment-entry',
    '/app/confirmation-paiement': 'payment-confirmation',
    '/app/recu-genere': 'receipt',
    '/app/recouvrement': 'collections',
  },
  admin: {
    '/app/demandes-de-pret': 'applications',
    '/app/analyse-d-une-demande': 'application-review',
    '/app/score-de-credit': 'credit-score',
    '/app/verification-kyc': 'kyc-review',
    '/app/prets': 'loans',
    '/app/paiements': 'payments',
    '/app/agents': 'agents',
    '/app/visites-terrain': 'field-visits',
    '/app/alertes-fraude': 'fraud-alerts',
    '/app/journal-d-audit': 'audit-log',
  },
});

export function resolveDefaRoute(pathname) {
  for (const [role, routes] of Object.entries(DEFA_ROUTE_MANIFEST)) {
    if (routes[pathname]) return { role, screen: routes[pathname] };
  }
  return null;
}
