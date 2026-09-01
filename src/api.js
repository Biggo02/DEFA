const API_BASE = import.meta.env.VITE_API_URL || '/api';

async function request(path, options = {}) {
  const token = localStorage.getItem('defa_token');
  const headers = {'Content-Type':'application/json', ...(options.headers || {})};
  if (token) headers.Authorization = `Token ${token}`;
  const response = await fetch(`${API_BASE}${path}`, {...options, headers});
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || 'Une erreur est survenue.');
  return data;
}

export const defaApi = {
  health: () => request('/health/'),
  me: () => request('/me/'),
  login: async (payload) => { const data = await request('/auth/login/', {method:'POST', body:JSON.stringify(payload)}); localStorage.setItem('defa_token', data.token); return data; },
  register: async (payload) => { const data = await request('/auth/register/', {method:'POST', body:JSON.stringify(payload)}); localStorage.setItem('defa_token', data.token); return data; },
  applications: () => request('/applications/'),
  createApplication: (payload) => request('/applications/', {method:'POST', body:JSON.stringify(payload)}),
  submitApplication: (id) => request(`/applications/${id}/submit/`, {method:'POST'}),
  loans: () => request('/loans/'),
  payments: () => request('/payments/'),
};
