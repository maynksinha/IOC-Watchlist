import { useState } from 'react'
import { theme } from '../theme/theme'

export default function TagInput({ tags, onChange }) {
  const [input, setInput] = useState('')

  const addTag = () => {
    const val = input.trim().toLowerCase()
    if (val && !tags.includes(val)) onChange([...tags, val])
    setInput('')
  }

  const removeTag = (tag) => onChange(tags.filter((t) => t !== tag))

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); addTag() }
    if (e.key === 'Backspace' && !input && tags.length) removeTag(tags[tags.length - 1])
  }

  return (
    <div className={theme.input.chip}>
      {tags.map((tag) => (
        <span key={tag} className={theme.tag.inputChip}>
          {tag}
          <button type="button" onClick={() => removeTag(tag)} className={theme.button.ghost}>
            &times;
          </button>
        </span>
      ))}
      <input
        className="flex-1 outline-none text-sm min-w-[80px]"
        placeholder="Add tag, press Enter or comma"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        onBlur={addTag}
      />
    </div>
  )
}
