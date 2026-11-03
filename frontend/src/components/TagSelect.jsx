import { useEffect, useMemo, useRef, useState } from 'react'
import { theme } from '../theme/theme'
import { LIMITS } from '../constants'

export default function TagSelect({
  tags,
  onChange,
  options = [],
  max = LIMITS.MAX_TAGS,
  maxLen = LIMITS.MAX_TAG_LENGTH,
}) {
  const [input, setInput] = useState('')
  const [open, setOpen] = useState(false)
  const [highlight, setHighlight] = useState(0)
  const boxRef = useRef(null)

  const norm = input.trim().toLowerCase()
  const atMax = tags.length >= max

  const menu = useMemo(() => {
    const available = options.filter((o) => !tags.includes(o))
    const filtered = norm ? available.filter((o) => o.includes(norm)) : available
    const items = filtered.map((name) => ({ type: 'existing', name }))
    const exists = options.includes(norm) || tags.includes(norm)
    if (norm && !exists && norm.length <= maxLen) items.push({ type: 'create', name: norm })
    return items
  }, [options, tags, norm, maxLen])

  useEffect(() => { setHighlight(0) }, [input, open])

  useEffect(() => {
    const onDocClick = (e) => {
      if (boxRef.current && !boxRef.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', onDocClick)
    return () => document.removeEventListener('mousedown', onDocClick)
  }, [])

  const addTag = (name) => {
    const v = name.trim().toLowerCase()
    if (!v || v.length > maxLen || tags.includes(v) || tags.length >= max) return
    onChange([...tags, v])
    setInput('')
  }

  const removeTag = (name) => onChange(tags.filter((t) => t !== name))

  const onKeyDown = (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault(); setOpen(true); setHighlight((i) => Math.min(i + 1, menu.length - 1))
    } else if (e.key === 'ArrowUp') {
      e.preventDefault(); setHighlight((i) => Math.max(i - 1, 0))
    } else if (e.key === 'Enter') {
      e.preventDefault()
      if (menu[highlight]) addTag(menu[highlight].name)
      else if (norm) addTag(norm)
    } else if (e.key === ',') {
      e.preventDefault(); if (norm) addTag(norm)
    } else if (e.key === 'Escape') {
      setOpen(false)
    } else if (e.key === 'Backspace' && !input && tags.length) {
      removeTag(tags[tags.length - 1])
    }
  }

  return (
    <div className="relative" ref={boxRef}>
      <div className={theme.combobox.control} onClick={() => setOpen(true)}>
        {tags.map((tag) => (
          <span key={tag} className={theme.tag.inputChip}>
            {tag}
            <button
              type="button"
              onClick={(e) => { e.stopPropagation(); removeTag(tag) }}
              className="hover:text-red-600"
              aria-label={`Remove ${tag}`}
            >
              &times;
            </button>
          </span>
        ))}
        {!atMax ? (
          <input
            className="flex-1 outline-none text-sm min-w-[110px] bg-transparent"
            placeholder={tags.length ? 'Add another…' : 'Select or create tags…'}
            value={input}
            onChange={(e) => { setInput(e.target.value.slice(0, maxLen)); setOpen(true) }}
            onFocus={() => setOpen(true)}
            onKeyDown={onKeyDown}
          />
        ) : (
          <span className="text-xs text-slate-400 px-1 py-0.5">Max {max} tags reached</span>
        )}
      </div>

      {open && menu.length > 0 && (
        <ul className={theme.combobox.menu}>
          {menu.map((item, idx) => (
            <li
              key={item.type + item.name}
              onMouseDown={(e) => { e.preventDefault(); addTag(item.name) }}
              onMouseEnter={() => setHighlight(idx)}
              className={`${theme.combobox.option} ${idx === highlight ? theme.combobox.optionActive : ''}`}
            >
              {item.type === 'create'
                ? <span>+ Create <strong>&ldquo;{item.name}&rdquo;</strong></span>
                : <span>{item.name}</span>}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
