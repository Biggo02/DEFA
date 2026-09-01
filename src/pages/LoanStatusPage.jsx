import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { defaApi } from '../api';

export default function LoanStatusPage({ applicationId }) {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const id = applicationId || params.get('id');
  const [state, setState] = useState({ loading: true, error: '', data: null });

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        let data;
        if (id) data = await defaApi.getApplication(id);
        else {
          const list = await defaApi.applications();
          data = [...list].sort((a,b) => new Date(b.updated_at || b.created_at || 0) - new Date(a.updated_at || a.created_at || 0))[0];
          if (!data) throw new Error('Aucune demande de prêt trouvée.');
        }
        if (!cancelled) setState({ loading: false, error: '', data });
      } catch (error) { if (!cancelled) setState({ loading: false, error: error.message, data: null }); }
    };
    load();
    return () => { cancelled = true; };
  }, [id]);

  if (state.loading) return <section className="pageState"><h2>Chargement du dossier…</h2><p>Récupération du statut depuis DEFA.</p></section>;
  if (state.error) return <section className="pageState error"><h2>Impossible de charger le dossier</h2><p>{state.error}</p><button className="btn btnPrimary" onClick={() => window.location.reload()}>Réessayer</button></section>;
  const d = state.data;
  const status = String(d.status || 'UNDER_REVIEW').toUpperCase();
  const labels = { DRAFT:'Brouillon', SUBMITTED:'Demande envoyée', UNDER_REVIEW:'En cours d’analyse', NEEDS_INFO:'Informations nécessaires', APPROVED:'Approuvée', REJECTED:'Refusée' };
  return <section className="pageState">
    <span className="eyebrow">SUIVI DE DEMANDE</span><h1>{labels[status] || d.status}</h1>
    <p>Référence : <strong>{d.reference || d.id}</strong></p>
    <div className="infoRows"><div><span>Montant demandé</span><b>{Number(d.amount || 0).toLocaleString('fr-FR')} FC</b></div><div><span>Statut</span><b>{labels[status] || d.status}</b></div><div><span>Soumise le</span><b>{d.created_at ? new Date(d.created_at).toLocaleDateString('fr-FR') : '—'}</b></div><div><span>Dernière mise à jour</span><b>{d.updated_at ? new Date(d.updated_at).toLocaleDateString('fr-FR') : '—'}</b></div></div>
    {d.review_notes && <div className="notice"><b>Message de DEFA</b><p>{d.review_notes}</p></div>}
    {status === 'NEEDS_INFO' && <button className="btn btnPrimary" onClick={() => navigate('/app/nouvelle-demande-de-pret')}>Compléter mon dossier</button>}
    {status === 'APPROVED' && <button className="btn btnPrimary" onClick={() => navigate('/app/details-du-pret')}>Voir mon prêt</button>}
  </section>;
}
