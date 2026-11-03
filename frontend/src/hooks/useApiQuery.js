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
      setData(res.data)
      return res
    } catch (err) {
      const errPayload = {
        status: err.response?.status,
        data:   err.response?.data ?? { detail: err.message },
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
