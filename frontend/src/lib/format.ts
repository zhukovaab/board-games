export function plural(n: number, forms: [string, string, string]): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return forms[0]
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return forms[1]
  return forms[2]
}

export function playersLabel(min: number, max: number): string {
  return min === max ? `${min}` : `${min}–${max}`
}

export function playtimeLabel(minutes: number | null): string {
  if (!minutes) return '—'
  if (minutes < 60) return `${minutes} мин`
  const hours = Math.floor(minutes / 60)
  const rest = minutes % 60
  const hoursLabel = `${hours} ${plural(hours, ['час', 'часа', 'часов'])}`
  return rest ? `${hoursLabel} ${rest} мин` : hoursLabel
}

export function ageLabel(age: number | null): string {
  return age ? `${age}+` : '—'
}

const COMPLEXITY_STEPS: { limit: number; label: string; className: string }[] = [
  { limit: 1.5, label: 'очень просто', className: 'text-emerald-300' },
  { limit: 2.2, label: 'просто', className: 'text-lime-300' },
  { limit: 3.0, label: 'средне', className: 'text-amber-300' },
  { limit: 4.0, label: 'сложно', className: 'text-orange-300' },
  { limit: 5.1, label: 'хардкор', className: 'text-rose-300' },
]

export function complexityInfo(value: number | null) {
  if (value === null) return { label: '—', className: 'text-mist', value: 0 }
  const step = COMPLEXITY_STEPS.find((s) => value < s.limit) ?? COMPLEXITY_STEPS.at(-1)!
  return { label: step.label, className: step.className, value }
}

export function coverGradient(seed: string): string {
  let hash = 0
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash * 31 + seed.charCodeAt(i)) % 360
  }
  const second = (hash + 48) % 360
  return `linear-gradient(135deg, hsl(${hash} 45% 26%), hsl(${second} 42% 14%))`
}
