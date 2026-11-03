import { theme } from '../theme/theme'

export default function TypeBadge({ type }) {
  const cls = theme.badge[type] || theme.badge.default
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs font-mono font-semibold ${cls}`}>
      {type}
    </span>
  )
}
