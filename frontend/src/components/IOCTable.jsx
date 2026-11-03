import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { fetchIOCs } from '../store/iocSlice'
import IOCRow from './IOCRow'
import CircularLoader from '../utils/Loader'
import { theme } from '../theme/theme'

export default function IOCTable() {
  const dispatch = useDispatch()
  const { items, total, isLoading, error } = useSelector((s) => s.iocs)
  const { typeFilter, tagFilter } = useSelector((s) => s.filter)

  const load = () => dispatch(fetchIOCs({
    type: typeFilter || undefined,
    tag:  tagFilter  || undefined,
  }))

  useEffect(() => { load() }, [dispatch, typeFilter, tagFilter]) // eslint-disable-line react-hooks/exhaustive-deps

  if (isLoading && !items.length) return <CircularLoader size="lg" />

  if (error) {
    return (
      <div className={`${theme.card} text-center`}>
        <p className="text-sm text-slate-600 mb-3">
          {error.message || 'Failed to load IOCs.'}
        </p>
        <button onClick={load} className={theme.button.secondary}>Retry</button>
      </div>
    )
  }

  if (!items.length) {
    return (
      <div className={`${theme.card} text-center py-10`}>
        <p className="text-sm text-slate-500">No IOCs found.</p>
        <p className="text-xs text-slate-400 mt-1">
          {typeFilter || tagFilter ? 'Try clearing the filters.' : 'Add your first indicator above.'}
        </p>
      </div>
    )
  }

  return (
    <div className={theme.table.wrapper}>
      <table className="w-full text-sm">
        <thead className={theme.table.header}>
          <tr>
            <th className={`${theme.table.cell} text-left font-semibold`}>Type</th>
            <th className={`${theme.table.cell} text-left font-semibold`}>Value</th>
            <th className={`${theme.table.cell} text-left font-semibold`}>Tags</th>
            <th className={`${theme.table.cell} text-left font-semibold`}>Note</th>
            <th className={`${theme.table.cell} text-left font-semibold`}>Added</th>
            <th className={theme.table.cell}></th>
          </tr>
        </thead>
        <tbody>
          {items.map((ioc) => <IOCRow key={ioc.id} ioc={ioc} />)}
        </tbody>
      </table>
      <div className="flex items-center justify-between px-4 py-2.5 border-t border-slate-100">
        <span className={`text-xs ${theme.text.muted}`}>
          Showing {items.length} of {total}
        </span>
        {isLoading && <span className="text-xs text-indigo-500">Updating…</span>}
      </div>
    </div>
  )
}
