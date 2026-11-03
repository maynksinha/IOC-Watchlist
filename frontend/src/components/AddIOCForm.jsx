import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { createIOCAPI } from '../services/iocService'
import { fetchIOCs } from '../store/iocSlice'
import { fetchTags } from '../store/tagSlice'
import useApiQuery from '../hooks/useApiQuery'
import TagInput from './TagInput'
import DuplicateAlert from './DuplicateAlert'
import { theme } from '../theme/theme'

export default function AddIOCForm() {
  const dispatch = useDispatch()
  const { typeFilter, tagFilter } = useSelector((s) => s.filter)

  const [value,     setValue]     = useState('')
  const [note,      setNote]      = useState('')
  const [tags,      setTags]      = useState([])
  const [duplicate, setDuplicate] = useState(null)
  const [formError, setFormError] = useState('')

  const { isLoading, execute: submitCreate } = useApiQuery(createIOCAPI)

  const refreshList = () => {
    dispatch(fetchIOCs({ type: typeFilter || undefined, tag: tagFilter || undefined }))
    dispatch(fetchTags())
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')
    setDuplicate(null)
    if (!value.trim()) return

    try {
      await submitCreate({ value: value.trim(), note: note.trim() || undefined, tags })
      setValue('')
      setNote('')
      setTags([])
      refreshList()
    } catch (err) {
      const { status, data } = err
      if (status === 409 && data?.detail?.existing) {
        setDuplicate(data.detail.existing)
      } else if (status === 400) {
        setFormError(data?.detail?.detail || 'Invalid IOC format')
      } else {
        setFormError('Unexpected error. Please try again.')
      }
    }
  }

  return (
    <div className={`${theme.card} mb-4`}>
      <h2 className={theme.text.label}>Add IOC</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <textarea
          className={theme.input.textarea}
          rows={2}
          placeholder="Paste IOC value (URL, IP, domain, hash) — defanged OK"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          required
        />
        <input
          className={theme.input.base}
          placeholder="Note (optional)"
          value={note}
          onChange={(e) => setNote(e.target.value)}
        />
        <TagInput tags={tags} onChange={setTags} />
        {formError && <p className={theme.alert.error}>{formError}</p>}
        <DuplicateAlert existing={duplicate} onDismiss={() => setDuplicate(null)} />
        <button type="submit" disabled={isLoading} className={`self-start ${theme.button.primary}`}>
          {isLoading ? 'Adding...' : 'Add IOC'}
        </button>
      </form>
    </div>
  )
}
