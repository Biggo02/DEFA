import React from 'react';
import LoanJourneyPage from '../pages/LoanJourneyPage';
import AgentCollectionPage from '../pages/AgentCollectionPage';

/**
 * Route adapters for the existing application router.
 * Import these components in main.jsx without replacing the existing router.
 */
export function VisibleLoanJourneyRoute() {
  return <LoanJourneyPage />;
}

export function VisibleAgentCollectionRoute() {
  return <AgentCollectionPage />;
}

export const VISIBLE_ROUTE_REGISTRY = Object.freeze({
  '/app/nouvelle-demande-de-pret': VisibleLoanJourneyRoute,
  '/app/enregistrer-paiement': VisibleAgentCollectionRoute,
});
