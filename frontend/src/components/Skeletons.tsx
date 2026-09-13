export function ShimmerBlock({ className = '' }: { className?: string }) {
  return (
    <div className={`relative overflow-hidden rounded-xl bg-ink-800 ${className}`}>
      <div className="absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-white/[0.06] to-transparent" />
    </div>
  )
}

export function GameCardSkeleton() {
  return (
    <div className="panel overflow-hidden p-3">
      <ShimmerBlock className="aspect-[3/4] w-full" />
      <div className="mt-3 space-y-2">
        <ShimmerBlock className="h-4 w-3/4 rounded-md" />
        <ShimmerBlock className="h-3 w-1/2 rounded-md" />
      </div>
    </div>
  )
}

export function GridSkeleton({ count = 12 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 2xl:grid-cols-5">
      {Array.from({ length: count }).map((_, index) => (
        <GameCardSkeleton key={index} />
      ))}
    </div>
  )
}
