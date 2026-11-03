import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { deleteIOC } from '../store/iocSlice'
import { useToast } from './ui/Toast'
import ConfirmDialog from './ui/ConfirmDialog'
import TypeBadge from './TypeBadge'
import { theme } from '../theme/theme'

export default function IOCRow({ ioc }) {
  const dispatch = useDispatch()
  const toast = useToast()
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const handleConfirm = async () => {
    setDeleting(true)
    try {
      const res = await dispatch(deleteIOC(ioc.id)).unwrap()
      toast.success(res.message || 'IOC deleted')
      setConfirmOpen(false)
    } catch (err) {
      toast.error(err?.message || 'Failed to delete IOC')
    } finally {
      setDeleting(false)
    }
  }

  return (
    <>
      <tr id={`ioc-${ioc.id}`} className={theme.table.row}>
        <td className={`${theme.table.cell} whitespace-nowrap`}>
          <TypeBadge type={ioc.ioc_type} />
        </td>
        <td className={`${theme.table.cell} max-w-xs`}>
          <code className="text-xs break-all text-slate-700">{ioc.ioc_raw}</code>
        </td>
        <td className={theme.table.cell}>
          {ioc.tags.length ? (
            <div className="flex flex-wrap gap-1">
              {ioc.tags.map((t) => (
                <span key={t} className={theme.tag.chip}>{t}</span>
              ))}
            </div>
          ) : (
            <span className={theme.text.muted}>—</span>
          )}
        </td>
        <td className={`${theme.table.cell} text-xs ${theme.text.subtle} max-w-xs truncate`}>
          {ioc.note || '—'}
        </td>
        <td className={`${theme.table.cell} text-xs ${theme.text.muted} whitespace-nowrap`}>
          {new Date(ioc.created_at).toLocaleDateString()}
        </td>
        <td className={`${theme.table.cell} text-right`}>
          <button onClick={() => setConfirmOpen(true)} className={theme.button.danger}>Delete</button>
        </td>
      </tr>

      <ConfirmDialog
        open={confirmOpen}
        title="Delete IOC"
        message={`Delete "${ioc.ioc_canonical}"? This cannot be undone.`}
        confirmLabel="Delete"
        loading={deleting}
        onConfirm={handleConfirm}
        onCancel={() => setConfirmOpen(false)}
      />
    </>
  )
}
