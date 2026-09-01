import { defaApi } from './api';

export function calculatePaid(payments = []) {
  return payments.reduce((total, payment) => total + Math.max(0, Number(payment.amount || 0)), 0);
}

export function calculateLoanBalance(loan, payments = []) {
  const totalDue = Number(loan?.total_amount ?? loan?.amount_due ?? loan?.principal_amount ?? loan?.amount ?? 0);
  const paid = calculatePaid(payments);
  return { totalDue, paid, remaining: Math.max(totalDue - paid, 0), progress: totalDue ? Math.min(100, Math.round(paid / totalDue * 100)) : 0 };
}

export async function loadLoanReconciliation(loanId) {
  const [loan, payments] = await Promise.all([defaApi.getLoan(loanId), defaApi.payments()]);
  const ownPayments = payments.filter((p) => String(p.loan || p.loan_id) === String(loanId));
  return { loan, payments: ownPayments, ...calculateLoanBalance(loan, ownPayments) };
}
