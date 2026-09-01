import { defaApi } from './api';

export async function recordAgentPayment(loanId, amount, metadata = {}) {
  const value = Number(amount);
  if (!loanId) throw new Error('Prêt introuvable.');
  if (!Number.isFinite(value) || value <= 0) throw new Error('Montant de paiement invalide.');
  return defaApi.createPayment({
    loan: loanId,
    amount: value,
    ...metadata,
  });
}

export async function verifyLoanByQr(qrToken) {
  if (!qrToken) throw new Error('QR Code invalide.');
  return defaApi.getLoanByQr(qrToken);
}
