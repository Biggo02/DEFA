import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { defaApi } from '../api';

export default function AdminApplicationReviewPage({ applicationId }) {
  const location = useLocation();
  const nav = useNavigate();
  const [application, setApplication] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [note, setNote] = useState('');

  const resolvedId = applicationId || new URLSearchParams(location.search).get('id');

  useEffect(() => {
    let alive = true;
    setError('');
    const load = async () => {
      try {
        if (resolvedId) {
          const item = await defaApi.getApplication(resolvedId);
          if (alive) setApplication(item);
          return;
        }
        const items = await defaApi.applications();
        if (alive) {
          if (items.length) setApplication(items[0]);
          else setError('Aucune demande de prêt disponible à analyser.');
        }
      } catch (e) {
        if (alive) setError(e.message);
      }
    };
    load();
    return () => { alive = false; };
  }, [resolvedId]);

  const decide = async (decision) => {
    const id = application?.id || resolvedId;
    if (!id) return setError('Impossible d’identifier la demande à traiter.');
    if (decision === 'REJECTED' && !note.trim()) return setError('Le motif du refus est obligatoire.');
    setBusy(true); setError('');
    try {
      const updated = await defaApi.decideApplication(id, { decision, reason: note.trim() });
      setApplication(updated);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
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
      <div>
        <button type="button" disabled={busy} onClick={() => decide('APPROVED')}>Approuver</button>
        <button type="button" disabled={busy} onClick={() => decide('NEEDS_INFO')}>Demander des informations</button>
        <button type="button" disabled={busy} onClick={() => decide('REJECTED')}>Refuser</button>
      </div>
      <button type="button" className="btn btnGhost" onClick={() => nav('/app/demandes-de-pret')}>Retour aux demandes</button>
    </>}
  </section>;
}
