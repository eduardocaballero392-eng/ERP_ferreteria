/**
 * Componente SearchBar reutilizable
 */

import { Search } from 'lucide-react'

export const SearchBar = ({
  value,
  onChange,
  placeholder = 'Buscar...',
  className,
}) => {
  return (
    <div className={`relative ${className}`}>
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Search className="h-5 w-5 text-gray-400" />
      </div>
      <input
        type="text"
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="input pl-10"
      />
    </div>
  )
}
