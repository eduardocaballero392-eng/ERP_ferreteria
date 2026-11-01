/**
 * Componente Card reutilizable
 */

import { clsx } from 'clsx'

export const Card = ({ children, className, title, subtitle, actions }) => {
  return (
    <div className={clsx('card', className)}>
      {(title || subtitle || actions) && (
        <div className="flex items-center justify-between mb-4">
          <div>
            {title && <h3 className="text-lg font-semibold text-gray-900">{title}</h3>}
            {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
          </div>
          {actions && <div className="flex items-center gap-2">{actions}</div>}
        </div>
      )}
      {children}
    </div>
  )
}
