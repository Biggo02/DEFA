# DEFA smoke test plan

1. Create a test client account.
2. Login and confirm `/me/` returns the same client.
3. Create a draft loan application.
4. Submit it and confirm its status changes server-side.
5. Upload a KYC document and confirm it is visible only to authorized users.
6. Create/record location only after explicit consent.
7. Admin reviews the application and either requests information, approves, or rejects with a reason.
8. For approval, confirm a loan and repayment schedule exist server-side.
9. Agent scans the loan QR and sees only the authorized dossier.
10. Agent records a partial cash payment.
11. Confirm the payment is stored once, the receipt references it, and the loan balance decreases.
12. Confirm the client dashboard reflects the same balance and payment history after refresh.
13. Repeat a payment request with the same idempotency key and verify no duplicate payment is created.
14. Verify unauthorized client/agent/admin calls are rejected by Django.
15. Verify rejected applications cannot be paid/collected.
