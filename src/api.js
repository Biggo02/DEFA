const API_BASE = import.meta.env.VITE_API_URL || '/api';

async function request(path, options = {}) {
  const token = localStorage.getItem('defa_token');
  const isFormData = options.body instanceof FormData;
  const headers = {
    ...(isFormData ? {} : {'Content-Type': 'application/json'}),
    ...(options.headers || {}),
  };
  if (token) headers.Authorization = `Token ${token}`;

  const response = await fetch(`${API_BASE}${path}`, {...options, headers});
  const data = await response.json().catch(() => ({}));
  if (response.status === 401) localStorage.removeItem('defa_token');
  if (!response.ok) {
    const message = data.detail || data.error || data.message || 'Une erreur est survenue.';
    throw new Error(message);
  }
  return data;
}

const unwrapList = (data) => Array.isArray(data) ? data : (data?.results || data?.data || []);

export const defaApi = {
  health: () => request('/health/'),
  me: () => request('/me/'),

  // Auth: paths aligned with backend/core/urls.py
  login: async (payload) => {
    const data = await request('/login/', {method:'POST', body:JSON.stringify(payload)});
    if (data.token) localStorage.setItem('defa_token', data.token);
    return data;
  },
  register: async (payload) => {
    const data = await request('/register/', {method:'POST', body:JSON.stringify(payload)});
    if (data.token) localStorage.setItem('defa_token', data.token);
    return data;
  },
  logout: () => localStorage.removeItem('defa_token'),

  applications: async () => unwrapList(await request('/applications/')),
  getApplication: (id) => request(`/applications/${id}/`),
  createApplication: (payload) => request('/applications/', {method:'POST', body:JSON.stringify(payload)}),
  updateApplication: (id,payload) => request(`/applications/${id}/`, {method:'PATCH', body:JSON.stringify(payload)}),
  submitApplication: (id) => request(`/applications/${id}/submit/`, {method:'POST'}),
  decideApplication: (id, payload) => request(`/applications/${id}/decision/`, {method:'POST', body:JSON.stringify(payload)}),

  loans: async () => unwrapList(await request('/loans/')),
  getLoan: (id) => request(`/loans/${id}/`),
  loanByQr: (token) => request(`/qr/${encodeURIComponent(token)}/`),

  payments: async () => unwrapList(await request('/payments/')),
  getPayment: (id) => request(`/payments/${id}/`),
  collectPayment: (payload) => request('/payments/collect/', {method:'POST', body:JSON.stringify(payload)}),

  documents: async () => unwrapList(await request('/documents/')),
  createDocument: (formData) => request('/documents/', {method:'POST', body:formData}),
  verifyDocument: (id, payload = {}) => request(`/documents/${id}/verify/`, {method:'POST', body:JSON.stringify(payload)}),

  assignments: async () => unwrapList(await request('/assignments/')),
  createAssignment: (payload) => request('/assignments/', {method:'POST', body:JSON.stringify(payload)}),

  verificationVisits: async () => unwrapList(await request('/verification-visits/')),
  createVerificationVisit: (payload) => request('/verification-visits/', {method:'POST', body:JSON.stringify(payload)}),
  completeVerificationVisit: (id, payload) => request(`/verification-visits/${id}/complete/`, {method:'POST', body:JSON.stringify(payload)}),

  locationConsents: async () => unwrapList(await request('/location-consents/')),
  createLocationConsent: (payload) => request('/location-consents/', {method:'POST', body:JSON.stringify(payload)}),
  locations: async () => unwrapList(await request('/locations/')),
  createLocation: (payload) => request('/locations/', {method:'POST', body:JSON.stringify(payload)}),

  contracts: async () => unwrapList(await request('/contracts/')),
  getContract: (id) => request(`/contracts/${id}/`),
  signContract: (id) => request(`/contracts/${id}/sign/`, {method:'POST'}),

  collections: async () => unwrapList(await request('/collections/')),
  createCollection: (payload) => request('/collections/', {method:'POST', body:JSON.stringify(payload)}),
  completeCollection: (id, payload) => request(`/collections/${id}/complete/`, {method:'POST', body:JSON.stringify(payload)}),

  notifications: async () => unwrapList(await request('/notifications/')),
  markNotificationRead: (id) => request(`/notifications/${id}/read/`, {method:'POST'}),

  fraudAlerts: async () => unwrapList(await request('/fraud-alerts/')),
  resolveFraudAlert: (id, payload = {}) => request(`/fraud-alerts/${id}/resolve/`, {method:'POST', body:JSON.stringify(payload)}),

  dashboard: () => request('/dashboard/'),
};
