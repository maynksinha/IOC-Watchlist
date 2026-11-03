import { useEffect } from 'react'
import { createPortal } from 'react-dom'
import { theme } from '../../theme/theme'

export default function ConfirmDialog({
  open,
  title = 'Are you sure?',
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  onConfirm,
  onCancel,
  loading = false,
  danger = true,
}) {
  useEffect(() => {
    if (!open) return
    const onKey = (e) => {
      if (e.key === 'Escape' && !loading) onCancel()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open, loading, onCancel])

  if (!open) return null

  return createPortal(
    <div className={theme.dialog.overlay} onMouseDown={() => !loading && onCancel()}>
      <div
        className={theme.dialog.panel}
        onMouseDown={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <h3 className={theme.dialog.title}>{title}</h3>
        {message && <p className={theme.dialog.message}>{message}</p>}
        <div className={theme.dialog.actions}>
          <button onClick={onCancel} disabled={loading} className={theme.button.secondary}>
            {cancelLabel}
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className={danger ? theme.button.dangerSolid : theme.button.primary}
          >
            {loading ? 'Working…' : confirmLabel}
          </button>
        </div>
      </div>
    </div>,
    document.body,
  )
}
