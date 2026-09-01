import React, { useState } from 'react';
import { submitApplication, validateApplication } from '../loanApplicationGuard';

const steps = [
  ['Identité', 'Vérifiez vos informations personnelles.'],
  ['Situation professionnelle', 'Indiquez votre activité et votre emploi.'],
  ['Revenus et charges', 'Déclarez vos revenus, dépenses et dettes.'],
  ['Commerce', 'Décrivez votre activité commerciale si applicable.'],
  ['Domicile', 'Indiquez votre adresse de résidence.'],
  ['Géolocalisation', 'Autorisez explicitement la localisation nécessaire au dossier.'],
  ['Références', 'Ajoutez des références vérifiables.'],
  ['Documents', 'Ajoutez les justificatifs demandés.'],
  ['Résumé', 'Relisez puis soumettez votre demande.'],
];

export default function LoanJourneyPage() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({ amount: '', purpose: '', employmentStatus: '', monthlyIncome: '', monthlyExpenses: '', existingDebt: '', businessName: '', homeAddress: '', locationConsent: false });
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const update = (key, value) => setForm((old) => ({ ...old, [key]: value }));
  const next = () => { setMessage(''); if (step < steps.length - 1) setStep(step + 1); };
  const back = () => { setMessage(''); if (step > 0) setStep(step - 1); };
  const submit = async () => {
    const errors = validateApplication(form);
    if (Object.keys(errors).length) { setMessage(Object.values(errors)[0]); return; }
    try { await submitApplication(form); setSubmitted(true); } catch (e) { setMessage(e.message); }
  };
  if (submitted) return <div className="journeyCard"><span className="badge green">Demande envoyée</span><h1>Votre dossier est en cours d’analyse</h1><p>DEFA a enregistré votre demande. Vous pourrez suivre son statut depuis votre espace client.</p><a className="btn btnPrimary" href="/app/statut-de-la-demande">Voir mon statut</a></div>;
  return <div className="journeyCard">
    <div className="journeyHeader"><span>Étape {step + 1} / {steps.length}</span><strong>{steps[step][0]}</strong><div className="journeyProgress"><i style={{ width: `${((step + 1) / steps.length) * 100}%` }} /></div></div>
    <h1>{steps[step][0]}</h1><p>{steps[step][1]}</p>
    {step === 0 && <div className="journeyGrid"><Field label="Montant demandé" value={form.amount} onChange={(v) => update('amount', v)} type="number"/><Field label="Motif du prêt" value={form.purpose} onChange={(v) => update('purpose', v)}/></div>}
    {step === 1 && <Field label="Situation professionnelle" value={form.employmentStatus} onChange={(v) => update('employmentStatus', v)} placeholder="Commerçant, salarié, indépendant…"/>}
    {step === 2 && <div className="journeyGrid"><Field label="Revenus mensuels" value={form.monthlyIncome} onChange={(v) => update('monthlyIncome', v)} type="number"/><Field label="Dépenses mensuelles" value={form.monthlyExpenses} onChange={(v) => update('monthlyExpenses', v)} type="number"/><Field label="Dettes existantes" value={form.existingDebt} onChange={(v) => update('existingDebt', v)} type="number"/></div>}
    {step === 3 && <div className="journeyGrid"><Field label="Nom du commerce" value={form.businessName} onChange={(v) => update('businessName', v)}/><Field label="Activité" value={form.businessType || ''} onChange={(v) => update('businessType', v)}/></div>}
    {step === 4 && <Field label="Adresse du domicile" value={form.homeAddress} onChange={(v) => update('homeAddress', v)} placeholder="Ville, commune, quartier, avenue…"/>}
    {step === 5 && <label className="consentBox"><input type="checkbox" checked={form.locationConsent} onChange={(e) => update('locationConsent', e.target.checked)}/><span>J’autorise DEFA à utiliser ma localisation uniquement pour les besoins déclarés du dossier et des vérifications associées.</span></label>}
    {step === 6 && <p>Ajoutez vos références depuis la section dédiée de votre dossier.</p>}
    {step === 7 && <p>Les justificatifs d’identité, revenus, domicile ou activité seront transmis dans votre espace sécurisé.</p>}
    {step === 8 && <pre className="journeySummary">{JSON.stringify(form, null, 2)}</pre>}
    {message && <div className="notice error">{message}</div>}
    <div className="journeyActions">{step > 0 && <button className="btn btnGhost" onClick={back}>Retour</button>}{step < steps.length - 1 ? <button className="btn btnPrimary" onClick={next}>Continuer</button> : <button className="btn btnPrimary" onClick={submit}>Soumettre la demande</button>}</div>
  </div>;
}

function Field({ label, value, onChange, type = 'text', placeholder = '' }) { return <label className="field"><span>{label}</span><input type={type} value={value || ''} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} /></label>; }
