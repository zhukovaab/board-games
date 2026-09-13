import { useEffect, useId, useRef, useState, type ReactNode } from 'react'

const TRACK_EMPTY = '#1E2331'

function fill(percent: number): string {
  return `linear-gradient(to right, #A78BFA 0%, #F472B6 ${percent}%, ${TRACK_EMPTY} ${percent}%)`
}

function Head({
  label,
  onReset,
}: {
  label: ReactNode
  onReset: (() => void) | null
}) {
  return (
    <div className="flex items-baseline justify-between gap-2">
      <span className="text-sm font-semibold text-slate-100">{label}</span>
      {onReset && (
        <button
          type="button"
          onClick={onReset}
          className="text-xs font-medium text-blush transition-opacity hover:opacity-80"
        >
          сбросить
        </button>
      )}
    </div>
  )
}

interface SliderProps {
  value: number | null
  min: number
  max: number
  step?: number
  /** Подпись выбранного значения; при null показываем «не важно». */
  format: (value: number) => string
  onChange: (value: number | null) => void
  ariaLabel: string
}

/**
 * Ползунок с «нулевой» позицией слева: она на шаг ниже минимума и означает,
 * что фильтр не применён. Так фильтр можно выключить тем же движением.
 *
 * Во время протаскивания мышью фильтр не применяется на каждый пиксель —
 * только на отпускании. Иначе список под ним переезжает на каждое микро-
 * движение, и клик по карточке сразу после ползунка может попасть мимо:
 * браузер засчитывает клик, только если под курсором в момент нажатия и
 * отпускания оказался один и тот же элемент, а перестраивающаяся сетка
 * это условие ломает. Клавиатура (стрелки) по-прежнему применяет фильтр
 * сразу — там дёргать нечему.
 */
export function RangeSlider({
  value,
  min,
  max,
  step = 1,
  format,
  onChange,
  ariaLabel,
}: SliderProps) {
  const off = min - step
  const committed = value ?? off
  const [dragging, setDragging] = useState(false)
  const [local, setLocal] = useState(committed)
  const localRef = useRef(local)

  useEffect(() => {
    if (!dragging) {
      setLocal(committed)
      localRef.current = committed
    }
  }, [committed, dragging])

  const percent = ((local - off) / (max - off)) * 100
  const liveValue = local < min ? null : local

  const commit = () => {
    const next = localRef.current
    setDragging(false)
    onChange(next < min ? null : next)
  }

  return (
    <div className="space-y-2.5">
      <Head
        label={liveValue === null ? 'не важно' : format(liveValue)}
        onReset={value === null ? null : () => onChange(null)}
      />
      <input
        type="range"
        className="slider"
        style={{ background: fill(percent) }}
        min={off}
        max={max}
        step={step}
        value={local}
        aria-label={ariaLabel}
        aria-valuetext={liveValue === null ? 'не важно' : format(liveValue)}
        onPointerDown={() => setDragging(true)}
        onPointerUp={commit}
        onChange={(event) => {
          const next = Number(event.target.value)
          setLocal(next)
          localRef.current = next
          // Без активного протаскивания (клавиатура, клик-прыжок до pointerup) — применяем сразу.
          if (!dragging) onChange(next < min ? null : next)
        }}
      />
    </div>
  )
}

interface DualProps {
  from: number | null
  to: number | null
  min: number
  max: number
  step?: number
  /** Может вернуть не только текст, но и, например, шкалу сложности. */
  format: (from: number, to: number) => ReactNode
  onChange: (from: number | null, to: number | null) => void
  ariaLabel: string
}

/**
 * Двойной ползунок. Границы, совпадающие с краями шкалы, отдаём как null —
 * иначе бэкенд отсечёт игры без проставленной сложности. Коммит по тем же
 * правилам, что у RangeSlider выше: во время протаскивания фильтр не летит
 * на каждое движение, только на отпускании бегунка.
 */
export function DualRangeSlider({
  from,
  to,
  min,
  max,
  step = 1,
  format,
  onChange,
  ariaLabel,
}: DualProps) {
  const id = useId()
  const committedLo = from ?? min
  const committedHi = to ?? max
  const [dragging, setDragging] = useState(false)
  const [localLo, setLocalLo] = useState(committedLo)
  const [localHi, setLocalHi] = useState(committedHi)
  const localRef = useRef({ lo: localLo, hi: localHi })

  useEffect(() => {
    if (!dragging) {
      setLocalLo(committedLo)
      setLocalHi(committedHi)
      localRef.current = { lo: committedLo, hi: committedHi }
    }
  }, [committedLo, committedHi, dragging])

  const touched = localLo > min || localHi < max
  const toPercent = (value: number) => ((value - min) / (max - min)) * 100

  const commit = () => {
    const { lo, hi } = localRef.current
    setDragging(false)
    onChange(lo > min ? lo : null, hi < max ? hi : null)
  }

  const moveLo = (next: number, apply: boolean) => {
    const clamped = Math.min(next, localRef.current.hi)
    setLocalLo(clamped)
    localRef.current = { ...localRef.current, lo: clamped }
    if (apply) onChange(clamped > min ? clamped : null, localRef.current.hi < max ? localRef.current.hi : null)
  }

  const moveHi = (next: number, apply: boolean) => {
    const clamped = Math.max(next, localRef.current.lo)
    setLocalHi(clamped)
    localRef.current = { ...localRef.current, hi: clamped }
    if (apply) onChange(localRef.current.lo > min ? localRef.current.lo : null, clamped < max ? clamped : null)
  }

  return (
    <div className="space-y-2.5">
      <Head
        label={touched ? format(localLo, localHi) : 'не важно'}
        onReset={touched ? () => onChange(null, null) : null}
      />
      <div className="relative h-4">
        <div className="absolute inset-x-0 top-1/2 h-1.5 -translate-y-1/2 rounded-full bg-ink-700" />
        <div
          className="absolute top-1/2 h-1.5 -translate-y-1/2 rounded-full bg-accent-gradient"
          style={{ left: `${toPercent(localLo)}%`, right: `${100 - toPercent(localHi)}%` }}
        />
        <input
          type="range"
          id={`${id}-from`}
          className="slider-bare"
          min={min}
          max={max}
          step={step}
          value={localLo}
          aria-label={`${ariaLabel}: от`}
          onPointerDown={() => setDragging(true)}
          onPointerUp={commit}
          onChange={(event) => moveLo(Number(event.target.value), !dragging)}
        />
        <input
          type="range"
          id={`${id}-to`}
          className="slider-bare"
          min={min}
          max={max}
          step={step}
          value={localHi}
          aria-label={`${ariaLabel}: до`}
          onPointerDown={() => setDragging(true)}
          onPointerUp={commit}
          onChange={(event) => moveHi(Number(event.target.value), !dragging)}
        />
      </div>
    </div>
  )
}
