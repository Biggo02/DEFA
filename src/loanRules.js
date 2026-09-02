export const MIN_LOAN_AMOUNT = 100000;
export const LOAN_STEP = 100000;
export const FEE_RATE = 0.12;

export function isValidLoanAmount(value) {
  const amount = Number(value);
  return Number.isFinite(amount) && amount >= MIN_LOAN_AMOUNT && amount % LOAN_STEP === 0;
}

export function calculateLoanFee(value) {
  const amount = Number(value) || 0;
  return Math.round(amount * FEE_RATE);
}

export function calculateTotalRepayment(value) {
  const amount = Number(value) || 0;
  return amount + calculateLoanFee(amount);
}
