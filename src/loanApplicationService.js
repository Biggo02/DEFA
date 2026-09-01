import { defaApi } from './api';

/** Submit a complete DEFA loan application through the Django API. */
export async function submitLoanApplication(form) {
  const payload = {
    amount: Number(form.amount),
    purpose: form.purpose,
    employment_status: form.employmentStatus,
    monthly_income: Number(form.monthlyIncome || 0),
    monthly_expenses: Number(form.monthlyExpenses || 0),
    existing_debt: Number(form.existingDebt || 0),
    business_name: form.businessName || '',
    business_type: form.businessType || '',
    business_age_months: Number(form.businessAgeMonths || 0),
    home_address: form.homeAddress || '',
    business_address: form.businessAddress || '',
    references: form.references || [],
    location_consent: Boolean(form.locationConsent),
    latitude: form.latitude ?? null,
    longitude: form.longitude ?? null,
  };

  if (!payload.amount || payload.amount <= 0) throw new Error('Le montant demandé doit être supérieur à zéro.');
  if (!payload.purpose) throw new Error('Veuillez indiquer le motif du prêt.');
  if (!payload.location_consent) throw new Error('Le consentement de localisation est requis lorsque la localisation est demandée.');

  return defaApi.createApplication(payload);
}

export async function saveApplicationDraft(form) {
  localStorage.setItem('defa_loan_draft', JSON.stringify(form));
  return form;
}

export function getApplicationDraft() {
  try { return JSON.parse(localStorage.getItem('defa_loan_draft') || 'null'); }
  catch { return null; }
}
