import React,{useMemo,useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {ShieldCheck,WalletCards,CheckCircle2,ArrowUpRight,ChevronRight,UserRound,FileCheck2,ClipboardCheck} from 'lucide-react';

export default function HomePage(){
 const nav=useNavigate();
 const [amount,setAmount]=useState(25000);
 const [days,setDays]=useState(30);
 const total=useMemo(()=>Math.round(amount*1.08),[amount]);
 const installments=Math.max(1,Math.ceil(days/7));
 const due=Math.ceil(total/installments);
 const go=(path)=>nav(path);
 return <>
  <section className="hero homeHero">
   <div className="heroText">
    <span className="badge green">Crédit responsable</span>
    <h1>Financez vos projets avec <em>DEFA</em>.</h1>
    <p>Un processus simple, transparent et basé sur votre capacité réelle de remboursement.</p>
    <div className="heroBtns">
     <button type="button" className="btn btnPrimary" onClick={()=>go('/inscription')}>Demander un prêt <ArrowUpRight size={17}/></button>
     <button type="button" className="btn btnGhost" onClick={()=>go('/simulateur')}>Simuler mon prêt</button>
    </div>
    <div className="trust"><ShieldCheck/><span>Vos informations sont protégées et utilisées uniquement pour l’analyse de votre dossier.</span></div>
   </div>
   <div className="heroCard">
    <div className="heroCardTop"><span>Votre financement</span><WalletCards/></div>
    <div className="amount">{amount.toLocaleString()} <small>FC</small></div>
    <div className="miniGrid"><div><span>Durée</span><b>{days} jours</b></div><div><span>Remboursement</span><b>Échelonné</b></div><div><span>Échéance</span><b>{due.toLocaleString()} FC</b></div></div>
    <div className="cardLine"/>
    <div className="person"><div className="avatar">DE</div><div><b>Dossier DEFA</b><span>Simulation indicative</span></div><CheckCircle2 className="ok"/></div>
   </div>
  </section>

  <section className="stats"><div><b>100%</b><span>Processus transparent</span></div><div><b>24h+</b><span>Suivi de votre dossier</span></div><div><b>1</b><span>Espace client sécurisé</span></div><div><b>24/7</b><span>Consultation du prêt</span></div></section>

  <section className="section" id="fonctionnement"><div className="sectionHead"><span className="badge">Comment ça marche</span><h2>Du dossier au remboursement</h2><p>Chaque étape est conçue pour protéger le client et DEFA.</p></div><div className="steps">{[['01','Créer un compte',UserRound],['02','Compléter le dossier',FileCheck2],['03','Vérification',ShieldCheck],['04','Décision',ClipboardCheck],['05','Remboursement',WalletCards]].map(([n,t,I])=><button type="button" className="step" key={n} onClick={()=>n==='01'?go('/inscription'):n==='02'?go('/inscription'):n==='03'?go('/securite'):n==='04'?go('/app/statut-de-la-demande'):go('/connexion')}><span>{n}</span><I/><h3>{t}</h3><p>Informations vérifiées et suivi clair.</p></button>)}</div></section>

  <section className="simSection" id="simulateur"><div><span className="badge">Simulateur</span><h2>Estimez votre remboursement</h2><p>Modifiez le montant et la durée pour obtenir une estimation instantanée.</p></div><div className="simCard"><label>Montant souhaité <strong>{amount.toLocaleString()} FC</strong></label><input aria-label="Montant souhaité" type="range" min="5000" max="100000" step="5000" value={amount} onChange={e=>setAmount(Number(e.target.value))}/><label>Durée <strong>{days} jours</strong></label><input aria-label="Durée" type="range" min="7" max="60" value={days} onChange={e=>setDays(Number(e.target.value))}/><div className="simResult"><div><span>Total estimatif</span><b>{total.toLocaleString()} FC</b></div><div><span>Échéances indicatives</span><b>{due.toLocaleString()} FC × {installments}</b></div></div><small>Simulation indicative. Les conditions définitives sont déterminées après analyse.</small><button type="button" className="btn btnPrimary" onClick={()=>go('/inscription')}>Commencer ma demande <ArrowUpRight size={17}/></button></div></section>

  <section className="section" id="securite"><div className="securityGrid"><div><span className="badge green">Sécurité & confiance</span><h2>Nous préférons vérifier avant de prêter.</h2><p>Identité, revenus, activité, références et localisation consentie peuvent être vérifiés avant toute décision.</p><ul><li><CheckCircle2/> Vérification d’identité</li><li><CheckCircle2/> Analyse de capacité de remboursement</li><li><CheckCircle2/> Visite terrain si nécessaire</li><li><CheckCircle2/> Historique des paiements</li></ul><button type="button" className="btn btnPrimary" onClick={()=>go('/securite')}>Découvrir notre sécurité <ChevronRight size={16}/></button></div><div className="securityCard"><ShieldCheck size={48}/><h3>Crédit responsable</h3><p>Un score aide à analyser le risque, mais la décision finale reste soumise à une vérification humaine et aux règles applicables.</p></div></div></section>

  <section className="section homeCta"><div><span className="badge">Prêt à commencer ?</span><h2>Faites votre demande en quelques étapes.</h2><p>Créez votre compte et complétez votre dossier depuis votre espace sécurisé.</p></div><button type="button" className="btn btnPrimary" onClick={()=>go('/inscription')}>Créer mon compte <ArrowUpRight size={17}/></button></section>
 </>;
}
