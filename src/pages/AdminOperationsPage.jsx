import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { defaApi } from '../api';

function Panel({title, children, onClick}) {
  return <button type="button" className="panel operationPanel" onClick={onClick}><h2>{title}</h2>{children}</button>;
}

export default function AdminOperationsPage() {
  const nav = useNavigate();
  const [data,setData]=useState({applications:[],loans:[],payments:[],alerts:[],agents:[]});
  const [error,setError]=useState('');
  const [loading,setLoading]=useState(true);

  const load = useCallback(async()=>{
    setLoading(true); setError('');
    const results=await Promise.allSettled([defaApi.applications(),defaApi.loans(),defaApi.payments(),defaApi.fraudAlerts(),defaApi.assignments()]);
    setData({
      applications:results[0].status==='fulfilled'?results[0].value:[],
      loans:results[1].status==='fulfilled'?results[1].value:[],
      payments:results[2].status==='fulfilled'?results[2].value:[],
      alerts:results[3].status==='fulfilled'?results[3].value:[],
      agents:results[4].status==='fulfilled'?results[4].value:[]
    });
    const failed=results.find(r=>r.status==='rejected');
    if(failed) setError(failed.reason?.message || 'Certaines données n’ont pas pu être chargées.');
    setLoading(false);
  },[]);

  useEffect(()=>{load();},[load]);

  return <main>
    <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}><h1>Opérations DEFA</h1><button type="button" className="btn btnGhost" onClick={load}>Actualiser</button></div>
    {loading&&<p>Chargement des opérations…</p>}
    {error&&<p role="alert">{error}</p>}
    <div>
      <Panel title="Demandes" onClick={()=>nav('/app/demandes-de-pret')}><p>{data.applications.length} demande(s)</p></Panel>
      <Panel title="Prêts" onClick={()=>nav('/app/prets')}><p>{data.loans.length} prêt(s)</p></Panel>
      <Panel title="Paiements" onClick={()=>nav('/app/paiements')}><p>{data.payments.length} paiement(s)</p></Panel>
      <Panel title="Alertes fraude" onClick={()=>nav('/app/alertes-fraude')}><p>{data.alerts.length} alerte(s)</p></Panel>
      <Panel title="Missions terrain" onClick={()=>nav('/app/visites-terrain')}><p>{data.agents.length} mission(s)</p></Panel>
    </div>
  </main>;
}
