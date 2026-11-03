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

  useEffect(() => {
    dispatch(fetchIOCs({
      type: typeFilter || undefined,
      tag:  tagFilter  || undefined,
    }))
  }, [dispatch, typeFilter, tagFilter])

  if (isLoading) return <CircularLoader />
  if (error)     return <p className={theme.alert.error}>Failed to load IOCs.</p>
  if (!items.length) return <p className={`${theme.text.muted} text-sm`}>No IOCs found.</p>

  return (
    <div className={theme.table.wrapper}>
      <table className="w-full text-sm">
        <thead className={theme.table.header}>
          <tr>
            <th className={`${theme.table.cell} text-left`}>Type</th>
            <th className={`${theme.table.cell} text-left`}>Value</th>
            <th className={`${theme.table.cell} text-left`}>Tags</th>
            <th className={`${theme.table.cell} text-left`}>Note</th>
            <th className={`${theme.table.cell} text-left`}>Added</th>
            <th className={theme.table.cell}></th>
          </tr>
        </thead>
        <tbody>
          {items.map((ioc) => <IOCRow key={ioc.id} ioc={ioc} />)}
        </tbody>
      </table>
      <p className={`text-xs px-3 py-2 ${theme.text.muted}`}>Total: {total}</p>
    </div>
  )
}
