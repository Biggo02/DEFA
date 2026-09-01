import React, { useEffect, useState } from 'react';
import { loadClientDashboard, money } from './dashboardData';

export default function ClientDashboardLive() {
  const [state, setState] = useState({ loading: true, error: '', data: null });

  useEffect(() => {
    let alive = true;
    loadClientDashboard()
      .then((data) => alive && setState({ loading: false, error: '', data }))
      .catch((error) => alive && setState({ loading: false, error: error.message, data: null }));
    return () => { alive = false; };
  }, []);

  if (state.loading) return <div className="liveDashboardState"><div className="loader"/><h2>Chargement de votre espace…</h2><p>Récupération sécurisée de vos informations DEFA.</p></div>;
  if (state.error) return <div className="liveDashboardState error"><h2>Impossible de charger votre tableau de bord</h2><p>{state.error}</p><button className="btn btnPrimary" onClick={() => window.location.reload()}>Réessayer</button></div>;

  const { data } = state;
  const name = data.me?.first_name || data.me?.firstName || data.me?.name || 'Client';
  const loan = data.activeLoan;
  const status = loan?.status || 'Aucun prêt actif';

  if (!loan) return <div className="liveDashboardState"><h2>Bonjour {name} 👋</h2><p>Vous n'avez actuellement aucun prêt actif.</p><a className="btn btnPrimary" href="/app/nouvelle-demande-de-pret">Demander un prêt</a></div>;

  return <section className="liveDashboard">
    <div className="liveWelcome"><div><span className="eyebrow">MON ESPACE DEFA</span><h1>Bonjour {name} 👋</h1><p>Voici la situation réelle de votre prêt.</p></div><span className="badge green">{status}</span></div>
    <div className="liveCards">
      <article><span>Montant initial</span><strong>{money(data.principal)}</strong></article>
      <article><span>Total à rembourser</span><strong>{money(data.total)}</strong></article>
      <article><span>Déjà remboursé</span><strong>{money(data.paid)}</strong></article>
      <article><span>Solde restant</span><strong>{money(data.remaining)}</strong></article>
    </div>
    <article className="progressCard"><div className="progressHead"><div><span>Progression du remboursement</span><strong>{data.progress}%</strong></div></div><div className="progressTrack"><div className="progressValue" style={{ width: `${data.progress}%` }}/></div><p>{money(data.paid)} remboursés sur {money(data.total)}.</p></article>
    <article className="historyCard"><div className="cardHeader"><div><span className="eyebrow">ACTIVITÉ</span><h2>Derniers paiements</h2></div><a href="/app/historique-des-paiements">Voir tout</a></div>{data.payments.length ? <div className="paymentRows">{data.payments.slice(0, 5).map((payment) => <div className="paymentRow" key={payment.id || payment.reference}><div><strong>{money(payment.amount)}</strong><span>{payment.created_at || payment.date || 'Paiement enregistré'}</span></div><span className="badge green">Payé</span></div>)}</div> : <p>Aucun paiement enregistré pour le moment.</p>}</article>
  </section>;
}
