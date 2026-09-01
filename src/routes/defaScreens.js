import React from 'react';
import LoanJourneyPage from '../pages/LoanJourneyPage';
import AgentCollectionPage from '../pages/AgentCollectionPage';
import LoanStatusPage from '../pages/LoanStatusPage';
import LoanAccountPage from '../pages/LoanAccountPage';
import LoanSchedulePage from '../pages/LoanSchedulePage';
import PaymentHistoryPage from '../pages/PaymentHistoryPage';
import ReceiptListPage from '../pages/ReceiptListPage';
import AgentScannedLoanPage from '../pages/AgentScannedLoanPage';
import AdminApplicationReviewPage from '../pages/AdminApplicationReviewPage';
import AdminOperationsPage from '../pages/AdminOperationsPage';
import AgentFieldPage from '../pages/AgentFieldPage';
import AdminRiskPage from '../pages/AdminRiskPage';

export const DEFA_SCREENS = Object.freeze({
  'loan-application': LoanJourneyPage,
  'loan-status': LoanStatusPage,
  'payment-entry': AgentCollectionPage,
  'loan-detail': LoanAccountPage,
  'schedule': LoanSchedulePage,
  'payment-history': PaymentHistoryPage,
  'receipts': ReceiptListPage,
  'scanned-loan': AgentScannedLoanPage,
  'application-review': AdminApplicationReviewPage,
  'applications': AdminOperationsPage,
  'application-review-dashboard': AdminRiskPage,
  'credit-score': AdminRiskPage,
  'field-visits': AgentFieldPage,
  'collections': AgentFieldPage,
});
