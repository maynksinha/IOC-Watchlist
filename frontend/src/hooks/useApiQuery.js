import { useState, useCallback } from 'react'

export default function useApiQuery(apiFn) {
  const [data,      setData]      = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error,     setError]     = useState(null)

  const execute = useCallback(async (...args) => {
    setIsLoading(true)
    setError(null)
    try {
      const res = await apiFn(...args)
      // Full envelope: { success, message, error_code, data }
      const envelope = res.data ?? {}
      setData(envelope.data ?? null)
      return envelope
    } catch (err) {
      const body = err.response?.data ?? {}
      const errPayload = {
        status:     err.response?.status,
        message:    body.message    ?? err.message,
        error_code: body.error_code ?? 'UNKNOWN_ERROR',
      }
      setError(errPayload)
      throw errPayload
    } finally {
      setIsLoading(false)
    }
  }, [apiFn])

  const reset = useCallback(() => {
    setData(null)
    setError(null)
    setIsLoading(false)
  }, [])

  return { data, isLoading, error, execute, reset }
}
