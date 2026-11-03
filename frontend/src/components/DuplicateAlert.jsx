import { theme } from '../theme/theme'

export default function DuplicateAlert({ existing, onDismiss }) {
  if (!existing) return null
  const date = new Date(existing.created_at).toLocaleDateString()
  return (
    <div className={`${theme.alert.warning} flex justify-between items-start`}>
      <span>
        Duplicate of IOC <strong>#{existing.id}</strong> ({existing.ioc_type} &middot; added {date})
        &nbsp;&mdash;&nbsp;
        <a href={`#ioc-${existing.id}`} className="underline">scroll to it</a>
      </span>
      <button onClick={onDismiss} className={`ml-4 ${theme.button.ghost}`}>&times;</button>
    </div>
  )
}
