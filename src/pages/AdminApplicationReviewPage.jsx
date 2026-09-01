import React, { useEffect, useState } from 'react';
import { defaApi } from '../api';

export default function AdminApplicationReviewPage({ applicationId }) {
  const [application, setApplication] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [note, setNote] = useState('');
  useEffect(() => { defaApi.getApplication(applicationId).then(setApplication).catch(e => setError(e.message)); }, [applicationId]);
  const decide = async (decision) => {
    if (decision === 'REJECTED' && !note.trim()) return setError('Le motif du refus est obligatoire.');
    setBusy(true); setError('');
    try { const updated = await defaApi.decideApplication(applicationId, { decision, reason: note.trim() }); setApplication(updated); }
    catch (e) { setError(e.message); } finally { setBusy(false); }
  };
  if (!application && !error) return <section><h1>Analyse de la demande</h1><p>Chargement…</p></section>;
  return <section>
    <h1>Analyse de la demande</h1>
    {error && <p role="alert">{error}</p>}
    {application && <>
      <p>Référence : {application.reference ?? application.id}</p>
      <p>Statut : {application.status}</p>
      <p>Montant demandé : {application.amount ?? application.requested_amount}</p>
      <p>Motif : {application.purpose ?? '—'}</p>
      <textarea value={note} onChange={e => setNote(e.target.value)} placeholder="Note d'analyse / motif" aria-label="Note d'analyse" />
      <div><button disabled={busy} onClick={() => decide('APPROVED')}>Approuver</button><button disabled={busy} onClick={() => decide('NEEDS_INFO')}>Demander des informations</button><button disabled={busy} onClick={() => decide('REJECTED')}>Refuser</button></div>
    </>}
  </section>;
}
