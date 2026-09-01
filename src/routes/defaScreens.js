import React from 'react';
import LoanJourneyPage from '../pages/LoanJourneyPage';
import AgentCollectionPage from '../pages/AgentCollectionPage';
import LoanStatusPage from '../pages/LoanStatusPage';

// Screen registry used by the route adapter. Keep this registry independent
// from the legacy entry point so migration can happen incrementally.
export const DEFA_SCREENS = Object.freeze({
  'loan-application': LoanJourneyPage,
  'loan-status': LoanStatusPage,
  'payment-entry': AgentCollectionPage,
});
