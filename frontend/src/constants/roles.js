/**
 * Roles del sistema
 */

export const ROLES = {
  ADMIN: 'admin',
  VENDEDOR: 'vendedor',
  ALMACENERO: 'almacenero',
}

export const ROLE_NAMES = {
  [ROLES.ADMIN]: 'Administrador',
  [ROLES.VENDEDOR]: 'Vendedor',
  [ROLES.ALMACENERO]: 'Almacenero',
}

export const ROLE_PERMISSIONS = {
  [ROLES.ADMIN]: {
    inventory: true,
    sales: true,
    purchases: true,
    customers: true,
    suppliers: true,
    reports: true,
    users: true,
  },
  [ROLES.VENDEDOR]: {
    inventory: false,
    sales: true,
    purchases: false,
    customers: true,
    suppliers: false,
    reports: true,
    users: false,
  },
  [ROLES.ALMACENERO]: {
    inventory: true,
    sales: false,
    purchases: true,
    customers: false,
    suppliers: true,
    reports: true,
    users: false,
  },
}
