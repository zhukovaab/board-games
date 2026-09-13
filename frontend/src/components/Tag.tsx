import { Link } from 'react-router-dom'

type TagKind = 'cat' | 'theme' | 'mech'

const KIND_STYLE: Record<TagKind, string> = {
  cat: 'border-accent/40 bg-accent/10 text-accent-soft hover:bg-accent/20',
  theme: 'border-blush/35 bg-blush/10 text-blush hover:bg-blush/20',
  mech: 'border-sky-400/30 bg-sky-400/10 text-sky-300 hover:bg-sky-400/20',
}

interface Props {
  kind: TagKind
  slug: string
  name: string
}

export function Tag({ kind, slug, name }: Props) {
  return (
    <Link
      to={`/?${kind}=${encodeURIComponent(slug)}`}
      className={`rounded-full border px-2.5 py-1 text-xs font-medium transition-colors duration-200 ${KIND_STYLE[kind]}`}
    >
      {name}
    </Link>
  )
}
