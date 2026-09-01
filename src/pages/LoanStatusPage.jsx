import React, { useEffect, useState } from 'react';
import { defaApi } from '../api';

export default function LoanStatusPage({ applicationId }) {
  const [state, setState] = useState({loading:true,error:null,data:null});
  useEffect(() => {
    if (!applicationId) { setState({loading:false,error:new Error('Dossier introuvable.'),data:null}); return; }
    defaApi.getApplication(applicationId)
      .then(data => setState({loading:false,error:null,data}))
      .catch(error => setState({loading:false,error,data:null}));
  }, [applicationId]);
  if (state.loading) return <section className="pageState"><h2>Chargement du dossier…</h2></section>;
  if (state.error) return <section className="pageState error"><h2>Impossible de charger le dossier</h2><p>{state.error.message}</p></section>;
  const d=state.data;
  return <section className="pageState"><span className="eyebrow">DEFA</span><h1>Suivi de ma demande</h1><p>Référence : {d.reference || d.id}</p><strong>{d.status || 'En cours d’analyse'}</strong>{d.review_notes && <div className="notice"><b>Message de DEFA</b><p>{d.review_notes}</p></div>}</section>;
}
