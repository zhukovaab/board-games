import ReactMarkdown, { type Components } from 'react-markdown'
import remarkGfm from 'remark-gfm'

const components: Components = {
  p: ({ children }) => (
    <p className="mb-4 text-[15px] leading-relaxed text-slate-300 last:mb-0">{children}</p>
  ),
  a: ({ children, ...props }) => (
    <a
      {...props}
      target="_blank"
      rel="noopener noreferrer"
      className="text-accent-soft underline underline-offset-2 transition-colors hover:text-accent"
    >
      {children}
    </a>
  ),
  strong: ({ children }) => <strong className="font-semibold text-slate-100">{children}</strong>,
  h1: ({ children }) => (
    <h1 className="mb-3 mt-6 text-xl font-bold text-slate-50 first:mt-0">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="mb-3 mt-6 text-lg font-bold text-slate-50 first:mt-0">{children}</h2>
  ),
  h3: ({ children }) => (
    <h3 className="mb-2 mt-5 text-base font-bold text-slate-50 first:mt-0">{children}</h3>
  ),
  ul: ({ children }) => (
    <ul className="mb-4 list-disc space-y-1 pl-5 text-[15px] text-slate-300 marker:text-accent-soft">
      {children}
    </ul>
  ),
  ol: ({ children }) => (
    <ol className="mb-4 list-decimal space-y-1 pl-5 text-[15px] text-slate-300 marker:text-accent-soft">
      {children}
    </ol>
  ),
  li: ({ children }) => <li className="leading-relaxed">{children}</li>,
  blockquote: ({ children }) => (
    <blockquote className="mb-4 border-l-2 border-accent/50 pl-4 italic text-mist">
      {children}
    </blockquote>
  ),
  code: ({ children }) => (
    <code className="rounded bg-ink-800 px-1.5 py-0.5 text-[13px] text-accent-soft">
      {children}
    </code>
  ),
  pre: ({ children }) => (
    <pre className="mb-4 overflow-x-auto rounded-lg bg-ink-800 p-4 text-[13px] text-slate-300">
      {children}
    </pre>
  ),
  hr: () => <hr className="my-6 border-line" />,
  table: ({ children }) => (
    <div className="mb-4 overflow-x-auto">
      <table className="w-full border-collapse text-left text-[14px] text-slate-300">
        {children}
      </table>
    </div>
  ),
  th: ({ children }) => (
    <th className="border-b border-line px-3 py-2 font-semibold text-slate-100">{children}</th>
  ),
  td: ({ children }) => <td className="border-b border-line/60 px-3 py-2">{children}</td>,
}

export function Markdown({ children }: { children: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
      {children}
    </ReactMarkdown>
  )
}
