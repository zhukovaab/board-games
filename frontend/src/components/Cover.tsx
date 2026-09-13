import { mediaUrl } from '../api/client'
import { coverGradient } from '../lib/format'

interface Props {
  src: string | null
  title: string
  className?: string
  rounded?: string
}

export function Cover({ src, title, className = '', rounded = 'rounded-xl' }: Props) {
  const url = mediaUrl(src)
  if (url) {
    return (
      <img
        src={url}
        alt={title}
        loading="lazy"
        className={`h-full w-full object-cover ${rounded} ${className}`}
      />
    )
  }
  return (
    <div
      className={`flex h-full w-full items-center justify-center ${rounded} ${className}`}
      style={{ background: coverGradient(title) }}
      aria-label={title}
    >
      <span className="px-4 text-center text-lg font-bold uppercase tracking-widest text-white/25">
        {title.slice(0, 2)}
      </span>
    </div>
  )
}
