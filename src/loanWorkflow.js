import { defaApi } from './api';

export const APPLICATION_STEPS = [
  'Identité', 'Situation professionnelle', 'Revenus et charges', 'Commerce',
  'Domicile', 'Localisation', 'Références', 'Documents', 'Résumé'
];

export function applicationProgress(step) {
  return Math.round((Math.max(1, Math.min(step, APPLICATION_STEPS.length)) / APPLICATION_STEPS.length) * 100);
}

export async function submitForReview(form) {
  const result = await defaApi.createApplication(form);
  localStorage.removeItem('defa_loan_draft');
  return result;
}

export async function refreshLoanState() {
  const [applications, loans, payments] = await Promise.all([
    defaApi.applications(), defaApi.loans(), defaApi.payments()
  ]);
  return { applications, loans, payments };
}
