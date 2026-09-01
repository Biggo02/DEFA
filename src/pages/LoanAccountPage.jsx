import React, { useEffect, useState } from 'react';
import { defaApi } from '../api';

export default function LoanAccountPage({ loanId }) {
  const [state, setState] = useState({ loading: true, error: '', loan: null, payments: [] });
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const loan = await defaApi.getLoan(loanId);
        const payments = (await defaApi.payments()).filter(p => String(p.loan ?? p.loan_id) === String(loanId));
        if (active) setState({ loading: false, error: '', loan, payments });
      } catch (e) { if (active) setState({ loading: false, error: e.message, loan: null, payments: [] }); }
    })();
    return () => { active = false; };
  }, [loanId]);
  if (state.loading) return <section><h1>Mon prêt</h1><p>Chargement…</p></section>;
  if (state.error) return <section><h1>Mon prêt</h1><p role="alert">{state.error}</p></section>;
  const total = Number(state.loan?.total_amount ?? state.loan?.amount ?? 0);
  const paid = state.payments.reduce((s, p) => s + Number(p.amount || 0), 0);
  const remaining = Math.max(total - paid, 0);
  return <section>
    <h1>Mon prêt</h1>
    <p>Référence : {state.loan?.reference ?? state.loan?.id}</p>
    <p>Total : {total}</p><p>Déjà payé : {paid}</p><p>Solde restant : {remaining}</p>
    <h2>Historique des paiements</h2>
    {state.payments.length === 0 ? <p>Aucun paiement enregistré.</p> : <ul>{state.payments.map(p => <li key={p.id}>Paiement {p.amount} — {p.created_at ?? p.date ?? ''}</li>)}</ul>}
  </section>;
}
