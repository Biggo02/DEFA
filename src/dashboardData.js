import { defaApi } from './api';

export async function loadClientDashboard() {
  const [me, applications, loans, payments] = await Promise.all([
    defaApi.me(),
    defaApi.applications(),
    defaApi.loans(),
    defaApi.payments(),
  ]);

  const activeLoan = loans.find((loan) => ['active', 'ongoing', 'en_cours'].includes(String(loan.status).toLowerCase())) || loans[0] || null;
  const paid = payments.reduce((sum, payment) => sum + Number(payment.amount || 0), 0);
  const principal = Number(activeLoan?.principal_amount ?? activeLoan?.amount ?? 0);
  const total = Number(activeLoan?.total_amount ?? activeLoan?.amount_due ?? principal);
  const remaining = Math.max(total - paid, 0);
  const progress = total > 0 ? Math.min(100, Math.round((paid / total) * 100)) : 0;

  return { me, applications, loans, payments, activeLoan, paid, principal, total, remaining, progress };
}

export function money(value, currency = 'FC') {
  return `${Number(value || 0).toLocaleString('fr-FR')} ${currency}`;
}
