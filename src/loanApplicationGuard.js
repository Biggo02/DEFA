import { defaApi } from './api';
import { MIN_LOAN_AMOUNT, LOAN_STEP, isValidLoanAmount } from './loanRules';

export const APPLICATION_STATUS = Object.freeze({
  DRAFT: 'DRAFT',
  SUBMITTED: 'SUBMITTED',
  UNDER_REVIEW: 'UNDER_REVIEW',
  NEEDS_INFO: 'NEEDS_INFO',
  APPROVED: 'APPROVED',
  REJECTED: 'REJECTED',
});

export function validateApplication(form) {
  const errors = {};
  const amount = Number(form.amount);
  if (!Number.isFinite(amount) || amount < MIN_LOAN_AMOUNT) errors.amount = `Le montant minimum est de ${MIN_LOAN_AMOUNT.toLocaleString('fr-FR')} FC.`;
  else if (amount % LOAN_STEP !== 0) errors.amount = `Le montant doit être un multiple de ${LOAN_STEP.toLocaleString('fr-FR')} FC (100 000, 200 000, 300 000…).`;
  if (!form.purpose) errors.purpose = 'Indiquez le motif du prêt.';
  if (!form.employmentStatus) errors.employmentStatus = 'Indiquez votre situation professionnelle.';
  if (Number(form.monthlyIncome || 0) < 0) errors.monthlyIncome = 'Le revenu ne peut pas être négatif.';
  if (Number(form.monthlyExpenses || 0) < 0) errors.monthlyExpenses = 'Les dépenses ne peuvent pas être négatives.';
  if (!form.homeAddress) errors.homeAddress = 'Le domicile est requis.';
  if (!form.locationConsent) errors.locationConsent = 'Votre consentement est requis pour enregistrer la localisation demandée.';
  return errors;
}

export async function fetchApplicationStatus(id) {
  if (!id) throw new Error('Dossier introuvable.');
  return defaApi.getApplication(id);
}

export async function submitApplication(form) {
  const errors = validateApplication(form);
  if (Object.keys(errors).length) {
    const error = new Error('Veuillez corriger les informations du dossier.');
    error.fields = errors;
    throw error;
  }
  if (!isValidLoanAmount(form.amount)) throw new Error('Montant de prêt invalide.');
  return defaApi.createApplication({
    ...form,
    amount: Number(form.amount),
    monthly_income: Number(form.monthlyIncome || 0),
    monthly_expenses: Number(form.monthlyExpenses || 0),
    existing_debt: Number(form.existingDebt || 0),
    location_consent: true,
    latitude: form.latitude ?? null,
    longitude: form.longitude ?? null,
  });
}
