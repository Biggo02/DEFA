import React, { useState } from 'react';
import { scanLoanAndCollect, collectPayment } from '../agentCollectionWorkflow';

export default function AgentCollectionPage() {
  const [qr, setQr] = useState(''); const [loan, setLoan] = useState(null); const [amount, setAmount] = useState(''); const [message, setMessage] = useState('');
  const scan = async () => { try { setMessage(''); setLoan(await scanLoanAndCollect(qr)); } catch (e) { setMessage(e.message); } };
  const pay = async () => { try { setMessage(''); const p = await collectPayment(loan.id, amount); setMessage(`Paiement enregistré : ${p.reference || p.id}`); } catch (e) { setMessage(e.message); } };
  return <div className="journeyCard"><span className="badge">Recouvrement</span><h1>Scanner un prêt</h1><p>Entrez ou scannez le QR du dossier autorisé.</p><div className="journeyGrid"><label className="field"><span>QR / token</span><input value={qr} onChange={e=>setQr(e.target.value)} placeholder="Scanner le QR…"/></label><button className="btn btnPrimary" onClick={scan}>Rechercher</button></div>{loan && <div className="panel"><h2>Dossier {loan.reference || loan.id}</h2><p>Statut : {loan.status}</p><p>Solde serveur : {loan.remaining ?? loan.balance ?? '—'}</p><label className="field"><span>Montant encaissé</span><input type="number" value={amount} onChange={e=>setAmount(e.target.value)}/></label><button className="btn btnPrimary" onClick={pay}>Enregistrer le paiement</button></div>}{message && <div className="notice">{message}</div>}</div>;
}
