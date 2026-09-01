export const ROLES = Object.freeze({ CLIENT: 'client', AGENT: 'agent', ANALYST: 'analyst', ADMIN: 'admin', SUPERADMIN: 'superadmin' });

export function isAuthenticated() {
  return Boolean(localStorage.getItem('defa_access_token'));
}

export function clearSession() {
  localStorage.removeItem('defa_access_token');
  localStorage.removeItem('defa_refresh_token');
  localStorage.removeItem('defa_user');
}
