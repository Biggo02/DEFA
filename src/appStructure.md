# DEFA Frontend Architecture

The existing `main.jsx` remains the compatibility entry point. New production code should be organized by responsibility:

- `pages/` — route-level screens
- `components/` — reusable UI
- `layouts/` — public/client/agent/admin shells
- `services/` — API and business workflows
- `hooks/` — React data/session hooks
- `routes/` — route configuration and guards

Current service modules already provide the first separation layer: `api.js`, `dashboardData.js`, `loanApplicationService.js`, `loanApplicationGuard.js`, `loanLifecycle.js`, `paymentReconciliation.js`, `paymentWorkflow.js`, `agentCollectionWorkflow.js`, and `adminLoanWorkflow.js`.

## Integration contract

1. Django/PostgreSQL is the source of truth.
2. React never fabricates balances, payment history, approval status, or credit decisions for an authenticated user.
3. Location is collected only with explicit consent and must never be implemented as covert tracking.
4. Client, agent, analyst, admin, and superadmin permissions are enforced server-side; frontend guards are only UX safeguards.
5. Payment recording must be idempotent and validated by Django before a receipt is considered final.
6. Rejection requires a reason; requests for more information require a message.
