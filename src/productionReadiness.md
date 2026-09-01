# DEFA production readiness checklist

## Client journey
- Register / login against Django
- Complete identity and KYC
- Provide employment, income, expenses, debt, business and address data
- Explicitly consent before location capture
- Submit loan application
- Track application status and requested information
- View approved loan, schedule, payments and balance

## Agent journey
- Authenticate with role enforced by Django
- View assigned verification/collection work
- Scan the loan QR only for an authorized dossier
- Confirm client identity before collection
- Record the cash payment through the collection endpoint
- Issue/store the server-confirmed receipt

## Admin / analyst journey
- Review KYC and verification evidence
- Review affordability/solvency information
- Request missing information
- Approve or reject with an auditable reason
- Monitor fraud alerts and field verification
- Never rely on frontend-only authorization

## Security rules
- No covert tracking or hidden location collection
- Do not expose identity documents publicly
- Do not trust balances calculated only in React
- Server validates payment amount and loan ownership
- Server-side role/permission checks are mandatory
- Use HTTPS, secure cookies/tokens and production secrets
- Configure CORS/CSRF and allowed hosts for deployment

## Deployment gate
Before accepting real borrowers, run the frontend production build and an end-to-end test against a staging database. The green Django CI proves backend checks/migrations, but it does not by itself prove browser/UI integration.
