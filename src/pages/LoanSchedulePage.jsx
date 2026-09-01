import React, { useEffect, useState } from 'react';
import { defaApi } from '../api';
export default function LoanSchedulePage({ loanId }) {
 const [loan,setLoan]=useState(null),[err,setErr]=useState('');
 useEffect(()=>{defaApi.getLoan(loanId).then(setLoan).catch(e=>setErr(e.message))},[loanId]);
 if(err)return <section><h1>Mon échéancier</h1><p role="alert">{err}</p></section>;
 if(!loan)return <section><h1>Mon échéancier</h1><p>Chargement…</p></section>;
 const items=loan.schedule ?? loan.installments ?? loan.repayment_schedule ?? [];
 return <section><h1>Mon échéancier</h1><p>Prêt : {loan.reference ?? loan.id}</p>{items.length?<table><thead><tr><th>Échéance</th><th>Montant</th><th>Payé</th><th>Statut</th></tr></thead><tbody>{items.map((x,i)=><tr key={x.id??i}><td>{x.due_date??x.date??'—'}</td><td>{x.amount??x.total??0}</td><td>{x.paid_amount??x.paid??0}</td><td>{x.status??'—'}</td></tr>)}</tbody></table>:<p>L’échéancier sera affiché dès qu’il est enregistré par DEFA.</p>}</section>;
}
