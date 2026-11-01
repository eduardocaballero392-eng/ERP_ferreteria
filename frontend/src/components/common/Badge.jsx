/**
 * Componente Badge reutilizable
 */

import { clsx } from 'clsx'

const variants = {
  success: 'badge-success',
  warning: 'badge-warning',
  danger: 'badge-danger',
  info: 'badge-info',
}

export const Badge = ({ children, variant = 'info', className }) => {
  return (
    <span className={clsx('badge', variants[variant], className)}>
      {children}
    </span>
  )
}
