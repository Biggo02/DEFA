import React from 'react';
import LoanStatusPage from '../pages/LoanStatusPage';

export default function LoanStatusRoute() {
  const params = new URLSearchParams(window.location.search);
  return <LoanStatusPage applicationId={params.get('id')} />;
}
