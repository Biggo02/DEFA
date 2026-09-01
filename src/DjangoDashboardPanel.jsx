import React, { useEffect, useState } from 'react';
import { loadClientDashboard, money } from './dashboardData';

export default function DjangoDashboardPanel() {
  const [state, setState] = useState({ loading: true, error: null, data: null });

  const refresh = () => {
    setState({ loading: true, error: null, data: null });
    loadClientDashboard()
      .then((data) => setState({ loading: false, error: null, data }))
      .catch((error) => setState({ loading: false, error, data: null }));
  };

  useEffect(refresh, []);

  if (state.loading) return <div className="dashboardState"><strong>Chargement sécurisé…</strong><span>Connexion à votre espace DEFA.</span></div>;
  if (state.error) return <div className="dashboardState dashboardError"><strong>Impossible de récupérer vos données.</strong><span>{state.error.message}</span><button className="btn btnPrimary" onClick={refresh}>Réessayer</button></div>;

  const d = state.data;
  const loan = d.activeLoan;
  if (!loan) return <div className="dashboardState"><strong>Aucun prêt actif</strong><span>Votre espace est prêt pour votre prochaine demande.</span><a className="btn btnPrimary" href="/app/nouvelle-demande-de-pret">Demander un prêt</a></div>;

  return <div className="djangoDashboardPanel">
    <div className="dashboardSummary">
      <div><span>Prêt actif</span><strong>{money(d.principal)}</strong><small>{loan.reference || loan.id || 'Dossier DEFA'}</small></div>
      <div><span>Remboursé</span><strong>{money(d.paid)}</strong><small>{d.progress}%</small></div>
      <div><span>Solde</span><strong>{money(d.remaining)}</strong><small>{loan.status || 'En cours'}</small></div>
    </div>
    <div className="dashboardProgress"><div><span>Progression</span><b>{d.progress}%</b></div><div className="progressTrack"><div className="progressValue" style={{ width: `${d.progress}%` }}/></div></div>
    <div className="dashboardRecent"><h3>Dernières transactions</h3>{d.payments.slice(0, 5).map((p) => <div className="dashboardTransaction" key={p.id || p.reference}><span>{p.reference || 'Paiement DEFA'}</span><b>{money(p.amount)}</b></div>)}{!d.payments.length && <span>Aucun paiement enregistré.</span>}</div>
  </div>;
}
