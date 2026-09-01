import React, { useEffect, useState } from 'react';
import { defaApi } from '../api';
export default function AgentFieldPage(){
 const [state,setState]=useState({items:[],loading:true,error:''});
 useEffect(()=>{Promise.all([defaApi.assignments(),defaApi.verificationVisits(),defaApi.collections()]).then(([a,v,c])=>setState({items:[...a.map(x=>({...x,type:'Mission'})),...v.map(x=>({...x,type:'Vérification'})),...c.map(x=>({...x,type:'Recouvrement'}))],loading:false,error:''})).catch(e=>setState({items:[],loading:false,error:e.message}));},[]);
 return <main><h1>Terrain</h1>{state.loading&&<p>Chargement…</p>}{state.error&&<p role="alert">{state.error}</p>} {!state.loading&&!state.error&&<ul>{state.items.map((x,i)=><li key={x.id??i}><strong>{x.type}</strong> — {x.reference??x.loan_reference??x.id??'Dossier'}</li>)}</ul>}</main>;
}
