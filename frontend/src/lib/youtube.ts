export function youtubeVideoId(url: string): string | null {
  try {
    const parsed = new URL(url)
    const host = parsed.hostname.replace(/^www\./, '')

    if (host === 'youtu.be') {
      return parsed.pathname.slice(1) || null
    }

    if (host === 'youtube.com' || host === 'm.youtube.com' || host === 'music.youtube.com') {
      if (parsed.pathname === '/watch') {
        return parsed.searchParams.get('v')
      }
      const shortMatch = parsed.pathname.match(/^\/(?:embed|shorts|live)\/([^/]+)/)
      if (shortMatch) return shortMatch[1]
    }

    return null
  } catch {
    return null
  }
}

export function youtubeThumbnailUrl(url: string): string | null {
  const id = youtubeVideoId(url)
  return id ? `https://i.ytimg.com/vi/${id}/mqdefault.jpg` : null
}

interface YTPlayerOptions {
  videoId: string
  host?: string
  playerVars?: Record<string, unknown>
  events?: {
    onReady?: (event: unknown) => void
    onError?: (event: unknown) => void
  }
}

export interface YTPlayerInstance {
  destroy: () => void
}

interface YTNamespace {
  Player: new (elementId: string, options: YTPlayerOptions) => YTPlayerInstance
}

declare global {
  interface Window {
    YT?: YTNamespace
    onYouTubeIframeAPIReady?: () => void
  }
}

let apiPromise: Promise<void> | null = null

/**
 * iframe.onload срабатывает и на локальную страницу ошибки браузера, когда сеть
 * недоступна, — по нему нельзя понять, загрузился ли реально плеер YouTube.
 * Единственный надёжный сигнал — событие onReady/onError самого IFrame Player API,
 * поэтому грузим его официальный скрипт и слушаем эти события.
 */
export function loadYouTubeIframeApi(): Promise<void> {
  if (window.YT?.Player) return Promise.resolve()
  if (apiPromise) return apiPromise

  apiPromise = new Promise<void>((resolve, reject) => {
    const previous = window.onYouTubeIframeAPIReady
    window.onYouTubeIframeAPIReady = () => {
      previous?.()
      resolve()
    }
    const script = document.createElement('script')
    script.src = 'https://www.youtube.com/iframe_api'
    script.onerror = () => reject(new Error('Не удалось загрузить YouTube IFrame API'))
    document.head.appendChild(script)
  }).catch((err) => {
    apiPromise = null
    throw err
  })

  return apiPromise
}
