import { defaApi } from './api';

export async function scanLoanAndCollect(qrToken) {
  if (!qrToken?.trim()) throw new Error('QR Code invalide.');
  const loan = await defaApi.getLoanByQr(qrToken.trim());
  return loan;
}

export async function collectPayment(loanId, amount, extra = {}) {
  const value = Number(amount);
  if (!loanId) throw new Error('Dossier de prêt introuvable.');
  if (!Number.isFinite(value) || value <= 0) throw new Error('Le montant doit être supérieur à zéro.');
  return defaApi.createPayment({ loan: loanId, amount: value, ...extra });
}

export function buildReceiptData(payment, loan, client) {
  return {
    receiptNumber: payment?.receipt_number || payment?.reference || `DEFA-${payment?.id || 'PAY'}`,
    loanReference: loan?.reference || loan?.id,
    clientName: client?.name || client?.full_name || '',
    amount: Number(payment?.amount || 0),
    date: payment?.created_at || payment?.date || new Date().toISOString(),
  };
}
