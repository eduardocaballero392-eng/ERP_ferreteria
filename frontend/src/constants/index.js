/**
 * Constantes del sistema
 */

export const STOCK_STATUS = {
  OK: { value: 'OK', label: 'OK', color: 'success' },
  REPONER: { value: 'REPONER', label: 'Reponer', color: 'warning' },
  AGOTADO: { value: 'AGOTADO', label: 'Agotado', color: 'danger' },
}

export const DOCUMENT_TYPES = {
  DNI: { value: 'DNI', label: 'DNI', length: 8 },
  RUC: { value: 'RUC', label: 'RUC', length: 11 },
}

export const COMPROBANTE_TYPES = {
  BOLETA: { value: 'BOLETA', label: 'Boleta' },
  FACTURA: { value: 'FACTURA', label: 'Factura' },
}

export const PAYMENT_CONDITIONS = {
  CONTADO: { value: 'CONTADO', label: 'Contado' },
  CREDITO: { value: 'CREDITO', label: 'Crédito' },
}

export const STATUS = {
  COMPLETADA: { value: 'COMPLETADA', label: 'Completada', color: 'success' },
  ANULADA: { value: 'ANULADA', label: 'Anulada', color: 'danger' },
}

export const IGV_RATE = 0.18

export const CURRENCY = {
  SYMBOL: 'S/',
  CODE: 'PEN',
  NAME: 'Soles',
}

export const DATE_FORMATS = {
  DISPLAY: 'dd/MM/yyyy',
  DISPLAY_TIME: 'dd/MM/yyyy HH:mm',
  API: 'yyyy-MM-dd',
  API_TIME: "yyyy-MM-dd'T'HH:mm:ss",
}

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 25, 50, 100],
}
