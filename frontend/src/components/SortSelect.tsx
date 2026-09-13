import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'

const OPTIONS = [
  { value: 'title', label: 'по названию А→Я' },
  { value: '-title', label: 'по названию Я→А' },
  { value: 'complexity', label: 'сначала простые' },
  { value: '-complexity', label: 'сначала сложные' },
  { value: 'playtime', label: 'сначала короткие' },
  { value: '-playtime', label: 'сначала долгие' },
  { value: 'new', label: 'сначала новые в коллекции' },
  { value: 'old', label: 'сначала старые в коллекции' },
]

interface Props {
  value: string
  onChange: (value: string) => void
}

export function SortSelect({ value, onChange }: Props) {
  const [open, setOpen] = useState(false)
  const selectedIndex = Math.max(
    OPTIONS.findIndex((option) => option.value === value),
    0,
  )
  const [activeIndex, setActiveIndex] = useState(selectedIndex)
  const rootRef = useRef<HTMLDivElement>(null)
  const optionRefs = useRef<(HTMLLIElement | null)[]>([])

  useEffect(() => {
    if (!open) return
    const onPointerDown = (event: MouseEvent) => {
      if (!rootRef.current?.contains(event.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', onPointerDown)
    return () => document.removeEventListener('mousedown', onPointerDown)
  }, [open])

  useEffect(() => {
    if (open) optionRefs.current[activeIndex]?.scrollIntoView({ block: 'nearest' })
  }, [open, activeIndex])

  const openWith = (index: number) => {
    setActiveIndex(index)
    setOpen(true)
  }

  const pick = (index: number) => {
    onChange(OPTIONS[index].value)
    setOpen(false)
  }

  const onKeyDown = (event: React.KeyboardEvent) => {
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault()
        if (!open) openWith(selectedIndex)
        else setActiveIndex((index) => Math.min(index + 1, OPTIONS.length - 1))
        break
      case 'ArrowUp':
        event.preventDefault()
        if (!open) openWith(selectedIndex)
        else setActiveIndex((index) => Math.max(index - 1, 0))
        break
      case 'Home':
        if (open) {
          event.preventDefault()
          setActiveIndex(0)
        }
        break
      case 'End':
        if (open) {
          event.preventDefault()
          setActiveIndex(OPTIONS.length - 1)
        }
        break
      case 'Enter':
      case ' ':
        event.preventDefault()
        if (open) pick(activeIndex)
        else openWith(selectedIndex)
        break
      case 'Escape':
        setOpen(false)
        break
      case 'Tab':
        setOpen(false)
        break
    }
  }

  return (
    <div ref={rootRef} className="relative min-w-0 flex-1 sm:w-60 sm:flex-none">
      <button
        type="button"
        role="combobox"
        aria-expanded={open}
        aria-haspopup="listbox"
        aria-label="Сортировка"
        aria-activedescendant={open ? `sort-option-${activeIndex}` : undefined}
        onClick={() => (open ? setOpen(false) : openWith(selectedIndex))}
        onKeyDown={onKeyDown}
        className="field flex cursor-pointer items-center justify-between gap-2 text-left"
      >
        <span className="truncate">{OPTIONS[selectedIndex].label}</span>
        <motion.span
          animate={{ rotate: open ? 180 : 0 }}
          transition={{ duration: 0.18 }}
          className="shrink-0 text-mist"
          aria-hidden
        >
          ▾
        </motion.span>
      </button>

      <AnimatePresence>
        {open && (
          <motion.ul
            role="listbox"
            aria-label="Сортировка"
            initial={{ opacity: 0, y: -6, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -6, scale: 0.98 }}
            transition={{ duration: 0.16, ease: 'easeOut' }}
            className="panel absolute left-0 right-0 top-full z-40 mt-2 max-h-[70vh] origin-top
                       overflow-y-auto p-1.5 shadow-card"
          >
            {OPTIONS.map((option, index) => {
              const isSelected = index === selectedIndex
              const isActive = index === activeIndex
              return (
                <li
                  key={option.value}
                  id={`sort-option-${index}`}
                  ref={(node) => {
                    optionRefs.current[index] = node
                  }}
                  role="option"
                  aria-selected={isSelected}
                  onMouseEnter={() => setActiveIndex(index)}
                  onClick={() => pick(index)}
                  className={`flex cursor-pointer items-center justify-between gap-2 rounded-lg px-3 py-2
                              text-sm transition-colors duration-150 ${
                                isActive ? 'bg-accent/15 text-slate-50' : 'text-mist'
                              } ${isSelected ? 'font-semibold text-accent-soft' : ''}`}
                >
                  <span className="truncate">{option.label}</span>
                  {isSelected && <span aria-hidden>✓</span>}
                </li>
              )
            })}
          </motion.ul>
        )}
      </AnimatePresence>
    </div>
  )
}
