import { useEffect, useState } from 'react'

interface Props {
  value: string
  onChange: (value: string) => void
}

export function SearchBar({ value, onChange }: Props) {
  const [local, setLocal] = useState(value)

  useEffect(() => {
    setLocal(value)
  }, [value])

  useEffect(() => {
    if (local === value) return
    const timer = setTimeout(() => onChange(local), 300)
    return () => clearTimeout(timer)
  }, [local, value, onChange])

  return (
    <div className="relative flex-1">
      <span className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-mist">
        ⌕
      </span>
      <input
        type="search"
        value={local}
        onChange={(event) => setLocal(event.target.value)}
        placeholder="Название игры — на русском или в оригинале"
        className="field pl-9"
      />
    </div>
  )
}
