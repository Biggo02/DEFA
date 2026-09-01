import { defaApi } from './api';

export const LOAN_STATUS = Object.freeze({
  PENDING: 'PENDING', APPROVED: 'APPROVED', ACTIVE: 'ACTIVE', OVERDUE: 'OVERDUE', COMPLETED: 'COMPLETED', REJECTED: 'REJECTED'
});

export function loanSummary(loan, payments = []) {
  const total = Number(loan?.total_amount ?? loan?.amount_due ?? loan?.principal_amount ?? loan?.amount ?? 0);
  const paid = payments.reduce((s, p) => s + Number(p.amount || 0), 0);
  return { total, paid, remaining: Math.max(total - paid, 0), progress: total ? Math.min(100, Math.round(paid / total * 100)) : 0 };
}

export async function getLoanLifecycle(loanId) {
  const [loan, payments] = await Promise.all([defaApi.getLoan(loanId), defaApi.payments()]);
  const related = payments.filter((p) => String(p.loan ?? p.loan_id) === String(loanId));
  return { loan, payments: related, summary: loanSummary(loan, related) };
}
