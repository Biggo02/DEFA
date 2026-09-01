import { defaApi } from './api';

export async function reviewApplication(id) {
  if (!id) throw new Error('Demande introuvable.');
  return defaApi.getApplication(id);
}

export async function approveApplication(id, notes = '') {
  if (!id) throw new Error('Demande introuvable.');
  return defaApi.updateApplication(id, { status: 'APPROVED', review_notes: notes });
}

export async function requestMoreInformation(id, message) {
  if (!id) throw new Error('Demande introuvable.');
  if (!message?.trim()) throw new Error('Précisez les informations demandées au client.');
  return defaApi.updateApplication(id, { status: 'NEEDS_INFO', review_notes: message.trim() });
}

export async function rejectApplication(id, reason) {
  if (!id) throw new Error('Demande introuvable.');
  if (!reason?.trim()) throw new Error('Un motif de refus est obligatoire.');
  return defaApi.updateApplication(id, { status: 'REJECTED', rejection_reason: reason.trim() });
}
