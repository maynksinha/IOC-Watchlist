import { useDispatch } from 'react-redux'
import { deleteIOC } from '../store/iocSlice'
import TypeBadge from './TypeBadge'
import { theme } from '../theme/theme'

export default function IOCRow({ ioc }) {
  const dispatch = useDispatch()

  const handleDelete = () => {
    if (!window.confirm(`Delete IOC #${ioc.id}?`)) return
    dispatch(deleteIOC(ioc.id))
  }

  return (
    <tr id={`ioc-${ioc.id}`} className={theme.table.row}>
      <td className={`${theme.table.cell} whitespace-nowrap`}>
        <TypeBadge type={ioc.ioc_type} />
      </td>
      <td className={`${theme.table.cell} max-w-xs`}>
        <code className="text-xs break-all">{ioc.ioc_raw}</code>
      </td>
      <td className={theme.table.cell}>
        <div className="flex flex-wrap gap-1">
          {ioc.tags.map((t) => (
            <span key={t.id} className={theme.tag.chip}>{t.name}</span>
          ))}
        </div>
      </td>
      <td className={`${theme.table.cell} text-xs ${theme.text.subtle} max-w-xs truncate`}>
        {ioc.note || '—'}
      </td>
      <td className={`${theme.table.cell} text-xs ${theme.text.muted} whitespace-nowrap`}>
        {new Date(ioc.created_at).toLocaleDateString()}
      </td>
      <td className={theme.table.cell}>
        <button onClick={handleDelete} className={theme.button.danger}>Delete</button>
      </td>
    </tr>
  )
}
