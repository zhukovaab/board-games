// Пять столбиков возрастающей высоты, как индикатор уровня сигнала — читается
// как «насколько сложны правила», а не как оценка «нравится / не нравится».
// Со звёздами была именно эта путаница: мало звёзд выглядело как «плохая игра».
const BAR_SCALE = [0.4, 0.58, 0.74, 0.88, 1]

interface ComplexityMeterProps {
  /** Значение сложности, 1–5. */
  value: number
  max?: number
  /** Цвет и размер — снаружи через className (text-lg, text-emerald-300…). */
  className?: string
}

export function ComplexityMeter({ value, max = 5, className = '' }: ComplexityMeterProps) {
  return (
    <span
      className={`inline-flex h-[1em] items-end gap-[0.12em] ${className}`}
      role="img"
      aria-label={`сложность ${value} из ${max}`}
    >
      {BAR_SCALE.map((scale, i) => {
        const fill = Math.max(0, Math.min(1, value - i))
        return (
          <span
            key={i}
            className="relative w-[0.2em] overflow-hidden rounded-[1px] bg-ink-600"
            style={{ height: `${scale * 100}%` }}
          >
            <span
              className="absolute inset-x-0 bottom-0 bg-current"
              style={{ height: `${fill * 100}%` }}
            />
          </span>
        )
      })}
    </span>
  )
}
