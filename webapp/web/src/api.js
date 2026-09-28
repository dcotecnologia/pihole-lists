// Thin fetch wrapper around the FastAPI backend. Base URL is resolved at
// build/runtime via VITE_API_BASE_URL (defaults to same-origin "/api",
// which is what the nginx container proxies to the `api` service).
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api';

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail ?? detail;
    } catch {
      // response wasn't JSON - keep statusText
    }
    throw new Error(detail);
  }
  if (res.status === 204) return null;
  return res.json();
}

export function getLists() {
  return request('/lists');
}

export function createList(name) {
  return request('/lists', { method: 'POST', body: JSON.stringify({ name }) });
}

export function deleteList(name) {
  return request(`/lists/${encodeURIComponent(name)}`, { method: 'DELETE' });
}

export function getItems(name, { query = '', page = 1, pageSize = 50 } = {}) {
  const params = new URLSearchParams({ query, page, page_size: pageSize });
  return request(`/lists/${encodeURIComponent(name)}/items?${params}`);
}

export function addItem(name, domain) {
  return request(`/lists/${encodeURIComponent(name)}/items`, {
    method: 'POST',
    body: JSON.stringify({ domain }),
  });
}

export function removeItem(name, domain) {
  return request(`/lists/${encodeURIComponent(name)}/items/${encodeURIComponent(domain)}`, {
    method: 'DELETE',
  });
}
