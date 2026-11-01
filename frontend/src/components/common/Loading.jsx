/**
 * Componente Loading reutilizable
 */

export const Loading = ({ size = 'md', text }) => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
  }

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <div
        className={`animate-spin rounded-full border-b-2 border-primary-600 ${sizes[size]}`}
      />
      {text && <p className="text-sm text-gray-500">{text}</p>}
    </div>
  )
}
