import React, { useEffect, useState } from 'react';
import { defaApi } from '../api';

function Panel({title, children}) { return <section><h2>{title}</h2>{children}</section>; }
export default function AdminOperationsPage() {
  const [data,setData]=useState({applications:[],loans:[],payments:[],alerts:[],agents:[]});
  const [error,setError]=useState('');
  useEffect(()=>{ Promise.allSettled([defaApi.applications(),defaApi.loans(),defaApi.payments(),defaApi.fraudAlerts(),defaApi.assignments()]).then(r=>setData({applications:r[0].status==='fulfilled'?r[0].value:[],loans:r[1].status==='fulfilled'?r[1].value:[],payments:r[2].status==='fulfilled'?r[2].value:[],alerts:r[3].status==='fulfilled'?r[3].value:[],agents:r[4].status==='fulfilled'?r[4].value:[]})).catch(e=>setError(e.message)); },[]);
  return <main><h1>Opérations DEFA</h1>{error&&<p role="alert">{error}</p>}<div><Panel title="Demandes"><p>{data.applications.length} demande(s)</p></Panel><Panel title="Prêts"><p>{data.loans.length} prêt(s)</p></Panel><Panel title="Paiements"><p>{data.payments.length} paiement(s)</p></Panel><Panel title="Alertes fraude"><p>{data.alerts.length} alerte(s)</p></Panel><Panel title="Missions terrain"><p>{data.agents.length} mission(s)</p></Panel></div></main>;
}
