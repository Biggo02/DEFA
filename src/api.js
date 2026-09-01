const API_BASE = import.meta.env.VITE_API_URL || '/api';

async function request(path, options = {}) {
  const token = localStorage.getItem('defa_token');
  const isFormData = options.body instanceof FormData;
  const headers = {
    ...(isFormData ? {} : {'Content-Type': 'application/json'}),
    ...(options.headers || {}),
  };
  if (token) headers.Authorization = `Token ${token}`;

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => ({}));
  if (response.status === 401) {
    localStorage.removeItem('defa_token');
  }
  if (!response.ok) {
    const message = data.detail || data.error || data.message || 'Une erreur est survenue.';
    throw new Error(message);
  }
  return data;
}

const unwrapList = (data) => Array.isArray(data) ? data : (data.results || data.data || []);

export const defaApi = {
  health: () => request('/health/'),
  me: () => request('/me/'),

  login: async (payload) => {
    const data = await request('/auth/login/', { method: 'POST', body: JSON.stringify(payload) });
    if (data.token) localStorage.setItem('defa_token', data.token);
    return data;
  },

  register: async (payload) => {
    const data = await request('/auth/register/', { method: 'POST', body: JSON.stringify(payload) });
    if (data.token) localStorage.setItem('defa_token', data.token);
    return data;
  },

  logout: () => {
    localStorage.removeItem('defa_token');
  },

  applications: async () => unwrapList(await request('/applications/')),
  getApplication: (id) => request(`/applications/${id}/`),
  createApplication: (payload) => request('/applications/', { method: 'POST', body: JSON.stringify(payload) }),
  updateApplication: (id, payload) => request(`/applications/${id}/`, { method: 'PATCH', body: JSON.stringify(payload) }),
  submitApplication: (id) => request(`/applications/${id}/submit/`, { method: 'POST' }),

  loans: async () => unwrapList(await request('/loans/')),
  getLoan: (id) => request(`/loans/${id}/`),

  payments: async () => unwrapList(await request('/payments/')),
  getPayment: (id) => request(`/payments/${id}/`),
};
