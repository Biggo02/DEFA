import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { defaApi } from '../api';

export default function AgentFieldPage(){
  const nav = useNavigate();
  const [state,setState]=useState({items:[],loading:true,error:''});

  const load = useCallback(async () => {
    setState(s=>({...s,loading:true,error:''}));
    try {
      const [a,v,c]=await Promise.all([defaApi.assignments(),defaApi.verificationVisits(),defaApi.collections()]);
      setState({items:[...a.map(x=>({...x,type:'Mission'})),...v.map(x=>({...x,type:'Vérification'})),...c.map(x=>({...x,type:'Recouvrement'}))],loading:false,error:''});
    } catch(e) { setState({items:[],loading:false,error:e.message}); }
  },[]);

  useEffect(()=>{ load(); },[load]);

  const openItem = (x) => {
    if (x.type === 'Recouvrement') return nav('/app/recouvrement');
    if (x.type === 'Vérification') return nav(`/app/detail-d-une-visite?id=${encodeURIComponent(x.id || '')}`);
    return nav(`/app/fiche-client?id=${encodeURIComponent(x.client_id || x.customer_id || x.id || '')}`);
  };

  return <main>
    <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}><h1>Terrain</h1><button type="button" className="btn btnGhost" onClick={load}>Actualiser</button></div>
    {state.loading&&<p>Chargement…</p>}
    {state.error&&<p role="alert">{state.error}</p>}
    {!state.loading&&!state.error&&!state.items.length&&<p>Aucune mission terrain actuellement.</p>}
    {!state.loading&&!state.error&&state.items.length>0&&<ul>{state.items.map((x,i)=><li key={x.id??i} style={{marginBottom:10}}><button type="button" className="linkButton" onClick={()=>openItem(x)}><strong>{x.type}</strong> — {x.reference??x.loan_reference??x.id??'Dossier'}</button></li>)}</ul>}
  </main>;
}
