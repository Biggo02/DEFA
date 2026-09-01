import { defaApi } from './api';

const money = (value) => `${Number(value || 0).toLocaleString('fr-FR')} FC`;

export async function loadClientDashboard() {
  const [me, applications, loans, payments] = await Promise.all([
    defaApi.me(),
    defaApi.applications(),
    defaApi.loans(),
    defaApi.payments(),
  ]);

  const activeLoan = loans.find((loan) => ['ACTIVE', 'DISBURSED', 'IN_PROGRESS'].includes(String(loan.status).toUpperCase())) || loans[0] || null;
  const loanPayments = activeLoan
    ? payments.filter((payment) => String(payment.loan || payment.loan_id || '') === String(activeLoan.id))
    : payments;

  const paid = loanPayments.reduce((sum, payment) => sum + Number(payment.amount || 0), 0);
  const principal = Number(activeLoan?.principal_amount ?? activeLoan?.amount ?? 0);
  const total = Number(activeLoan?.total_amount ?? activeLoan?.amount_due ?? principal);
  const remaining = Math.max(total - paid, 0);
  const progress = total > 0 ? Math.min(100, Math.round((paid / total) * 100)) : 0;

  return {
    me,
    applications,
    loans,
    payments,
    activeLoan,
    paid,
    principal,
    total,
    remaining,
    progress,
    formatted: {
      paid: money(paid),
      principal: money(principal),
      total: money(total),
      remaining: money(remaining),
    },
  };
}

export { money };