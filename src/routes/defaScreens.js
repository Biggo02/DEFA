import React from 'react';
import LoanJourneyPage from '../pages/LoanJourneyPage';
import AgentCollectionPage from '../pages/AgentCollectionPage';
import LoanStatusPage from '../pages/LoanStatusPage';
import LoanAccountPage from '../pages/LoanAccountPage';
import AdminApplicationReviewPage from '../pages/AdminApplicationReviewPage';

// Screen registry used by the route adapter. Keep this registry independent
// from the legacy entry point so migration can happen incrementally.
export const DEFA_SCREENS = Object.freeze({
  'loan-application': LoanJourneyPage,
  'loan-status': LoanStatusPage,
  'payment-entry': AgentCollectionPage,
  'loan-detail': LoanAccountPage,
  'schedule': LoanAccountPage,
  'payment-history': LoanAccountPage,
  'receipts': LoanAccountPage,
  'application-review': AdminApplicationReviewPage,
});
