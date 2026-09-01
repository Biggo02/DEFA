import React, { useEffect, useState } from 'react';
import { defaApi } from '../api';
export default function AdminRiskPage(){
 const [apps,setApps]=useState([]); const [error,setError]=useState('');
 useEffect(()=>{defaApi.applications().then(setApps).catch(e=>setError(e.message));},[]);
 const score=(a)=>{let s=0;if(a?.status==='SUBMITTED'||a?.status==='PENDING')s+=20;if(Number(a?.amount??a?.requested_amount)>0)s+=20;if(a?.purpose)s+=15;if(a?.income||a?.monthly_income)s+=20;if(a?.employment_status)s+=15;return Math.min(s,100)};
 return <main><h1>Analyse du risque</h1>{error&&<p role="alert">{error}</p>}<ul>{apps.map(a=><li key={a.id}>Demande {a.reference??a.id} — score indicatif {score(a)}/100 — {a.status}</li>)}</ul><p>Le score affiché est indicatif : la décision de crédit doit rester validée par les règles serveur et l'autorité compétente.</p></main>;
}
