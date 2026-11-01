/**
 * Utilidades de validación
 */

/**
 * Validar DNI (8 dígitos)
 */
export const validateDNI = (dni) => {
  return /^\d{8}$/.test(dni)
}

/**
 * Validar RUC (11 dígitos)
 */
export const validateRUC = (ruc) => {
  return /^\d{11}$/.test(ruc)
}

/**
 * Validar email
 */
export const validateEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

/**
 * Validar teléfono peruano (9 dígitos)
 */
export const validatePhone = (phone) => {
  return /^9\d{8}$/.test(phone)
}

/**
 * Validar número positivo
 */
export const validatePositiveNumber = (value) => {
  return !isNaN(value) && Number(value) > 0
}

/**
 * Validar stock disponible
 */
export const validateStock = (current, requested) => {
  return Number(current) >= Number(requested)
}
