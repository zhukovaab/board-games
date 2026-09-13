interface Props {
  page: number
  pages: number
  onChange: (page: number) => void
}

export function Pagination({ page, pages, onChange }: Props) {
  if (pages <= 1) return null

  const numbers: (number | '…')[] = []
  for (let i = 1; i <= pages; i += 1) {
    if (i === 1 || i === pages || Math.abs(i - page) <= 1) {
      numbers.push(i)
    } else if (numbers.at(-1) !== '…') {
      numbers.push('…')
    }
  }

  return (
    <nav className="mt-10 flex items-center justify-center gap-2">
      <button
        type="button"
        onClick={() => onChange(page - 1)}
        disabled={page <= 1}
        className="chip disabled:cursor-not-allowed disabled:opacity-40"
      >
        Назад
      </button>
      {numbers.map((item, index) =>
        item === '…' ? (
          <span key={`gap-${index}`} className="px-1 text-mist">
            …
          </span>
        ) : (
          <button
            key={item}
            type="button"
            onClick={() => onChange(item)}
            className={`chip min-w-[38px] justify-center ${item === page ? 'chip-active' : 'hover:border-accent/40 hover:text-slate-100'}`}
          >
            {item}
          </button>
        ),
      )}
      <button
        type="button"
        onClick={() => onChange(page + 1)}
        disabled={page >= pages}
        className="chip disabled:cursor-not-allowed disabled:opacity-40"
      >
        Вперёд
      </button>
    </nav>
  )
}
