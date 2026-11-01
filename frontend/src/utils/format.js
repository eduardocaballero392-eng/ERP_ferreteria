/**
 * Utilidades de formato
 */

import { format, parseISO } from 'date-fns'
import { es } from 'date-fns/locale'
import { CURRENCY, DATE_FORMATS } from '@/constants'

/**
 * Formatear moneda
 */
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return `${CURRENCY.SYMBOL} 0.00`
  
  return `${CURRENCY.SYMBOL} ${Number(amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}`
}

/**
 * Formatear porcentaje
 */
export const formatPercentage = (value, decimals = 2) => {
  if (value === null || value === undefined) return '0%'
  return `${Number(value).toFixed(decimals)}%`
}

/**
 * Formatear fecha
 */
export const formatDate = (date, formatStr = DATE_FORMATS.DISPLAY) => {
  if (!date) return ''
  
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    return format(dateObj, formatStr, { locale: es })
  } catch (error) {
    console.error('Error al formatear fecha:', error)
    return ''
  }
}

/**
 * Formatear fecha con hora
 */
export const formatDateTime = (date) => {
  return formatDate(date, DATE_FORMATS.DISPLAY_TIME)
}

/**
 * Formatear número
 */
export const formatNumber = (number, decimals = 0) => {
  if (number === null || number === undefined) return '0'
  
  return Number(number).toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * Formatear documento (DNI/RUC)
 */
export const formatDocument = (type, number) => {
  if (!number) return ''
  return `${type}: ${number}`
}

/**
 * Obtener iniciales del nombre
 */
export const getInitials = (name) => {
  if (!name) return ''
  
  return name
    .split(' ')
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .substring(0, 2)
}
