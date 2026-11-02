/**
 * Configuración de la API
 */

export const API_CONFIG = {
  // En desarrollo se usa el proxy de Vite para mantener las llamadas en el mismo origen.
  // En producción, VITE_API_URL apunta directamente al servicio del backend.
  BASE_URL: import.meta.env.DEV
    ? ''
    : (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, ''),
  API_VERSION: '/api/v1',
  TIMEOUT: 30000,
}

export const API_ENDPOINTS = {
  // Auth
  AUTH: {
    LOGIN: '/auth/login/form',
    REGISTER: '/auth/register',
    SETUP_STATUS: '/auth/setup-status',
    SETUP: '/auth/setup',
    ME: '/auth/me',
    CHANGE_PASSWORD: '/auth/change-password',
  },
  
  // Categories
  CATEGORIES: {
    LIST: '/categories/',
    WITH_COUNT: '/categories/with-count',
    DETAIL: (id) => `/categories/${id}`,
    CREATE: '/categories/',
    UPDATE: (id) => `/categories/${id}`,
    DELETE: (id) => `/categories/${id}`,
  },
  
  // Products
  PRODUCTS: {
    LIST: '/products/',
    DETAILS: '/products/details',
    LOW_STOCK: '/products/low-stock',
    SEARCH: '/products/search',
    DETAIL: (id) => `/products/${id}`,
    CREATE: '/products/',
    UPDATE: (id) => `/products/${id}`,
    ADJUST_STOCK: (id) => `/products/${id}/adjust-stock`,
    DELETE: (id) => `/products/${id}`,
  },
  
  // Suppliers
  SUPPLIERS: {
    LIST: '/suppliers/',
    WITH_STATS: '/suppliers/with-stats',
    SEARCH: '/suppliers/search',
    DETAIL: (id) => `/suppliers/${id}`,
    CREATE: '/suppliers/',
    UPDATE: (id) => `/suppliers/${id}`,
    DELETE: (id) => `/suppliers/${id}`,
  },
  
  // Purchases
  PURCHASES: {
    LIST: '/purchases/',
    STATS: '/purchases/stats',
    DETAIL: (id) => `/purchases/${id}`,
    CREATE: '/purchases/',
    UPDATE: (id) => `/purchases/${id}`,
    DELETE: (id) => `/purchases/${id}`,
  },
  
  // Customers
  CUSTOMERS: {
    LIST: '/customers/',
    WITH_STATS: '/customers/with-stats',
    SEARCH: '/customers/search',
    DETAIL: (id) => `/customers/${id}`,
    CREATE: '/customers/',
    UPDATE: (id) => `/customers/${id}`,
    DELETE: (id) => `/customers/${id}`,
  },
  
  // Sales
  SALES: {
    LIST: '/sales/',
    STATS: '/sales/stats',
    DETAIL: (id) => `/sales/${id}`,
    CREATE: '/sales/',
    UPDATE: (id) => `/sales/${id}`,
    DELETE: (id) => `/sales/${id}`,
  },
  
  // Reports
  REPORTS: {
    DASHBOARD: '/reports/dashboard',
    INVENTORY: '/reports/inventory',
    SALES: '/reports/sales',
    PURCHASES: '/reports/purchases',
    MOVEMENTS: (id) => `/reports/movements/${id}`,
    AUDIT: '/reports/audit',
  },
}

export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${API_CONFIG.API_VERSION}${endpoint}`
}
