import { useSelector, useDispatch } from 'react-redux'
import { setTypeFilter, setTagFilter, clearFilters } from '../store/filterSlice'
import { theme } from '../theme/theme'

const IOC_TYPES = ['ipv4', 'domain', 'url', 'md5', 'sha1', 'sha256']

export default function FilterBar() {
  const dispatch = useDispatch()
  const { typeFilter, tagFilter } = useSelector((s) => s.filter)
  const tags = useSelector((s) => s.tags.items)

  return (
    <div className={`${theme.filter.bar} mb-4`}>
      <span className={`${theme.text.subtle} font-medium`}>Filter:</span>
      <select
        value={typeFilter}
        onChange={(e) => dispatch(setTypeFilter(e.target.value))}
        className={theme.filter.select}
      >
        <option value="">All types</option>
        {IOC_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
      </select>
      <select
        value={tagFilter}
        onChange={(e) => dispatch(setTagFilter(e.target.value))}
        className={theme.filter.select}
      >
        <option value="">All tags</option>
        {tags.map((t) => <option key={t} value={t}>{t}</option>)}
      </select>
      {(typeFilter || tagFilter) && (
        <button onClick={() => dispatch(clearFilters())} className={theme.button.ghost}>
          Clear
        </button>
      )}
    </div>
  )
}
