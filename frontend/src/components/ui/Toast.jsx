import { createContext, useCallback, useContext, useMemo, useState } from 'react'
import { createPortal } from 'react-dom'
import { theme } from '../../theme/theme'

const ToastContext = createContext(null)
let _id = 0

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const dismiss = useCallback((id) => {
    setToasts((list) => list.filter((t) => t.id !== id))
  }, [])

  const push = useCallback((type, message) => {
    if (!message) return
    const id = ++_id
    setToasts((list) => [...list, { id, type, message }])
    setTimeout(() => dismiss(id), 4500)
  }, [dismiss])

  const api = useMemo(() => ({
    success: (m) => push('success', m),
    error:   (m) => push('error', m),
    info:    (m) => push('info', m),
  }), [push])

  return (
    <ToastContext.Provider value={api}>
      {children}
      {createPortal(
        <div className={theme.toast.viewport}>
          {toasts.map((t) => (
            <ToastItem key={t.id} toast={t} onDismiss={() => dismiss(t.id)} />
          ))}
        </div>,
        document.body,
      )}
    </ToastContext.Provider>
  )
}

function ToastItem({ toast, onDismiss }) {
  const tone = theme.toast[toast.type] || theme.toast.info
  return (
    <div className={`${theme.toast.base} ${tone}`} role="status">
      <span className="flex-1 break-words">{toast.message}</span>
      <button onClick={onDismiss} className="ml-2 shrink-0 opacity-70 hover:opacity-100" aria-label="Dismiss">
        &times;
      </button>
    </div>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within a ToastProvider')
  return ctx
}
