import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { defaApi } from '../api';

export default function AdminRiskPage(){
  const nav = useNavigate();
  const [apps,setApps]=useState([]);
  const [error,setError]=useState('');
  const [loading,setLoading]=useState(true);

  const load = async () => {
    setLoading(true); setError('');
    try { setApps(await defaApi.applications()); }
    catch(e){ setError(e.message); }
    finally { setLoading(false); }
  };
  useEffect(()=>{ load(); },[]);

  const score=(a)=>{
    let s=0;
    if(['SUBMITTED','PENDING'].includes(String(a?.status||'').toUpperCase()))s+=20;
    if(Number(a?.amount??a?.requested_amount)>0)s+=20;
    if(a?.purpose)s+=15;
    if(a?.income||a?.monthly_income)s+=20;
    if(a?.employment_status)s+=15;
    return Math.min(s,100);
  };

  return <main>
    <h1>Analyse du risque</h1>
    <p>Les scores sont indicatifs et ne remplacent pas la décision serveur.</p>
    {error&&<p role="alert">{error}</p>}
    {loading&&<p>Chargement des demandes…</p>}
    {!loading&&!apps.length&&<div className="panel"><p>Aucune demande à analyser.</p><button type="button" className="btn btnGhost" onClick={load}>Actualiser</button></div>}
    {!loading&&apps.length>0&&<div className="panel"><ul>{apps.map(a=><li key={a.id} style={{marginBottom:12}}><button type="button" className="linkButton" onClick={()=>nav(`/app/analyse-d-une-demande?id=${encodeURIComponent(a.id)}`)}>Demande {a.reference??a.id}</button> — score indicatif <strong>{score(a)}/100</strong> — {a.status}</li>)}</ul><button type="button" className="btn btnGhost" onClick={load}>Actualiser</button></div>}
  </main>;
}
