import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { defaApi } from '../api';
import { validateApplication } from '../loanApplicationGuard';

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

const emptyForm = { amount: '', purpose: '', employmentStatus: '', monthlyIncome: '', monthlyExpenses: '', existingDebt: '', businessName: '', businessType: '', businessAgeMonths: '', homeAddress: '', businessAddress: '', references: [], locationConsent: false, latitude: null, longitude: null };

export default function LoanJourneyPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [form, setForm] = useState(() => { try { return { ...emptyForm, ...JSON.parse(localStorage.getItem('defa_loan_draft') || '{}') }; } catch { return emptyForm; } });
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [saving, setSaving] = useState(false);
  const [locating, setLocating] = useState(false);

  useEffect(() => { localStorage.setItem('defa_loan_draft', JSON.stringify(form)); }, [form]);
  const update = (key, value) => setForm(old => ({ ...old, [key]: value }));
  const errors = useMemo(() => validateApplication(form), [form]);

  const next = () => {
    setMessage('');
    const requiredByStep = {
      0: ['amount', 'purpose'],
      1: ['employmentStatus'],
      2: [],
      4: ['homeAddress'],
      5: ['locationConsent'],
    };
    const missing = (requiredByStep[step] || []).find(k => errors[k]);
    if (missing) { setMessage(errors[missing]); return; }
    if (step < steps.length - 1) setStep(step + 1);
  };
  const back = () => { setMessage(''); if (step > 0) setStep(step - 1); };

  const getLocation = () => {
    setMessage('');
    if (!navigator.geolocation) { setMessage('La géolocalisation n’est pas disponible sur cet appareil.'); return; }
    if (!form.locationConsent) { setMessage('Cochez d’abord votre consentement de localisation.'); return; }
    setLocating(true);
    navigator.geolocation.getCurrentPosition(
      p => { update('latitude', p.coords.latitude); update('longitude', p.coords.longitude); setLocating(false); },
      () => { setLocating(false); setMessage('Impossible d’obtenir votre position. Autorisez la localisation puis réessayez.'); },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  };

  const submit = async () => {
    setMessage('');
    if (Object.keys(errors).length) { setMessage(Object.values(errors)[0]); return; }
    setSaving(true);
    try {
      await defaApi.createApplication({
        amount: Number(form.amount), purpose: form.purpose, employment_status: form.employmentStatus,
        monthly_income: Number(form.monthlyIncome || 0), monthly_expenses: Number(form.monthlyExpenses || 0),
        existing_debt: Number(form.existingDebt || 0), business_name: form.businessName || '', business_type: form.businessType || '',
        business_age_months: Number(form.businessAgeMonths || 0), home_address: form.homeAddress || '', business_address: form.businessAddress || '',
        references: form.references || [], location_consent: Boolean(form.locationConsent), latitude: form.latitude, longitude: form.longitude,
      });
      localStorage.removeItem('defa_loan_draft');
      setSubmitted(true);
    } catch (e) { setMessage(e.message || 'Impossible d’envoyer la demande.'); }
    finally { setSaving(false); }
  };

  if (submitted) return <div className="journeyCard"><span className="badge green">Demande envoyée</span><h1>Votre dossier est en cours d’analyse</h1><p>DEFA a enregistré votre demande. Vous pourrez suivre son statut depuis votre espace client.</p><button className="btn btnPrimary" onClick={() => navigate('/app/statut-de-la-demande')}>Voir mon statut</button></div>;

  return <div className="journeyCard">
    <div className="journeyHeader"><span>Étape {step + 1} / {steps.length}</span><strong>{steps[step][0]}</strong><div className="journeyProgress"><i style={{ width: `${((step + 1) / steps.length) * 100}%` }} /></div></div>
    <h1>{steps[step][0]}</h1><p>{steps[step][1]}</p>
    {step === 0 && <div className="journeyGrid"><Field label="Montant demandé" value={form.amount} onChange={v => update('amount', v)} type="number"/><Field label="Motif du prêt" value={form.purpose} onChange={v => update('purpose', v)} placeholder="Commerce, agriculture, éducation…"/></div>}
    {step === 1 && <Field label="Situation professionnelle" value={form.employmentStatus} onChange={v => update('employmentStatus', v)} placeholder="Commerçant, salarié, indépendant…"/>}
    {step === 2 && <div className="journeyGrid"><Field label="Revenus mensuels" value={form.monthlyIncome} onChange={v => update('monthlyIncome', v)} type="number"/><Field label="Dépenses mensuelles" value={form.monthlyExpenses} onChange={v => update('monthlyExpenses', v)} type="number"/><Field label="Dettes existantes" value={form.existingDebt} onChange={v => update('existingDebt', v)} type="number"/></div>}
    {step === 3 && <div className="journeyGrid"><Field label="Nom du commerce" value={form.businessName} onChange={v => update('businessName', v)}/><Field label="Activité" value={form.businessType} onChange={v => update('businessType', v)}/><Field label="Ancienneté (mois)" value={form.businessAgeMonths} onChange={v => update('businessAgeMonths', v)} type="number"/><Field label="Adresse du commerce" value={form.businessAddress} onChange={v => update('businessAddress', v)}/></div>}
    {step === 4 && <Field label="Adresse du domicile" value={form.homeAddress} onChange={v => update('homeAddress', v)} placeholder="Ville, commune, quartier, avenue…"/>}
    {step === 5 && <><label className="consentBox"><input type="checkbox" checked={form.locationConsent} onChange={e => update('locationConsent', e.target.checked)}/><span>J’autorise DEFA à utiliser ma localisation uniquement pour les besoins déclarés du dossier et des vérifications associées.</span></label><button type="button" className="btn btnGhost" onClick={getLocation} disabled={locating}>{locating ? 'Localisation…' : 'Obtenir ma position'}</button>{form.latitude != null && <p className="notice">Position enregistrée : {form.latitude.toFixed(5)}, {form.longitude.toFixed(5)}</p>}</>}
    {step === 6 && <><Field label="Référence 1" value={form.references?.[0]?.name || ''} onChange={v => update('references', [{ name: v, phone: form.references?.[0]?.phone || '' }])}/><Field label="Téléphone de la référence" value={form.references?.[0]?.phone || ''} onChange={v => update('references', [{ name: form.references?.[0]?.name || '', phone: v }])}/></>}
    {step === 7 && <p className="notice">Les justificatifs seront ajoutés depuis votre espace sécurisé. Vous pouvez enregistrer cette étape et revenir au dossier sans perdre les informations déjà saisies.</p>}
    {step === 8 && <div className="journeySummary"><p><b>Montant :</b> {Number(form.amount || 0).toLocaleString()} FC</p><p><b>Motif :</b> {form.purpose || '—'}</p><p><b>Profession :</b> {form.employmentStatus || '—'}</p><p><b>Revenus :</b> {Number(form.monthlyIncome || 0).toLocaleString()} FC</p><p><b>Dépenses :</b> {Number(form.monthlyExpenses || 0).toLocaleString()} FC</p><p><b>Domicile :</b> {form.homeAddress || '—'}</p><p><b>Localisation :</b> {form.latitude != null ? 'Enregistrée' : 'Consentement accordé, position non récupérée'}</p><p><b>Référence :</b> {form.references?.[0]?.name || '—'}</p></div>}
    {message && <div className="notice error">{message}</div>}
    <div className="journeyActions">{step > 0 && <button className="btn btnGhost" onClick={back}>Retour</button>}{step < steps.length - 1 ? <button className="btn btnPrimary" onClick={next}>Continuer</button> : <button className="btn btnPrimary" onClick={submit} disabled={saving}>{saving ? 'Envoi en cours…' : 'Soumettre la demande'}</button>}</div>
  </div>;
}

function Field({ label, value, onChange, type = 'text', placeholder = '' }) { return <label className="field"><span>{label}</span><input type={type} value={value || ''} placeholder={placeholder} onChange={e => onChange(e.target.value)} /></label>; }
