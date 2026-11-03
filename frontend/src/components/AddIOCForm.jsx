import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { createIOCAPI } from '../services/iocService'
import { fetchIOCs } from '../store/iocSlice'
import { fetchTags } from '../store/tagSlice'
import useApiQuery from '../hooks/useApiQuery'
import { useToast } from './ui/Toast'
import TagSelect from './TagSelect'
import { theme } from '../theme/theme'
import { LIMITS } from '../constants'

export default function AddIOCForm() {
  const dispatch = useDispatch()
  const toast = useToast()
  const { typeFilter, tagFilter } = useSelector((s) => s.filter)
  const existingTags = useSelector((s) => s.tags.items)

  const [value,     setValue]     = useState('')
  const [note,      setNote]      = useState('')
  const [tags,      setTags]      = useState([])
  const [fieldError, setFieldError] = useState('')

  const { isLoading, execute: submitCreate } = useApiQuery(createIOCAPI)

  const refreshList = () => {
    dispatch(fetchIOCs({ type: typeFilter || undefined, tag: tagFilter || undefined }))
    dispatch(fetchTags())
  }

  const validate = () => {
    const v = value.trim()
    if (!v) return 'IOC value is required.'
    if (v.length > LIMITS.MAX_VALUE_LENGTH) return `IOC value must be at most ${LIMITS.MAX_VALUE_LENGTH} characters.`
    if (note.length > LIMITS.MAX_NOTE_LENGTH) return `Note must be at most ${LIMITS.MAX_NOTE_LENGTH} characters.`
    return ''
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const err = validate()
    if (err) { setFieldError(err); return }
    setFieldError('')

    try {
      const res = await submitCreate({
        value: value.trim(),
        note: note.trim() || undefined,
        tags,
      })
      toast.success(res.message || 'IOC created')
      setValue('')
      setNote('')
      setTags([])
      refreshList()
    } catch (err) {
      // err: { status, message, error_code }
      toast.error(err.message || 'Failed to add IOC')
    }
  }

  return (
    <div className={theme.card}>
      <h2 className={theme.text.label}>Add IOC</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <div>
          <textarea
            className={`${theme.input.textarea} ${fieldError && !value.trim() ? theme.input.error : ''}`}
            rows={2}
            maxLength={LIMITS.MAX_VALUE_LENGTH}
            placeholder="Paste IOC value (URL, IP, domain, hash) — defanged OK"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
          <div className="flex justify-end mt-1">
            <span className={theme.text.muted + ' text-xs'}>{value.length}/{LIMITS.MAX_VALUE_LENGTH}</span>
          </div>
        </div>

        <input
          className={theme.input.base}
          maxLength={LIMITS.MAX_NOTE_LENGTH}
          placeholder="Note (optional)"
          value={note}
          onChange={(e) => setNote(e.target.value)}
        />

        <TagSelect tags={tags} onChange={setTags} options={existingTags} />

        {fieldError && <p className={theme.alert.error}>{fieldError}</p>}

        <button type="submit" disabled={isLoading} className={`self-start ${theme.button.primary}`}>
          {isLoading ? 'Adding…' : 'Add IOC'}
        </button>
      </form>
    </div>
  )
}
