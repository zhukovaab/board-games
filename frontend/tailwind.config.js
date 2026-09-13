/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          950: '#07080C',
          900: '#0C0E14',
          850: '#11141C',
          800: '#161A24',
          700: '#1E2331',
          600: '#2A3040',
        },
        line: '#252B3A',
        mist: '#8D94A8',
        accent: {
          DEFAULT: '#8B5CF6',
          soft: '#A78BFA',
          deep: '#6D28D9',
        },
        blush: '#F472B6',
      },
      fontFamily: {
        sans: ['Manrope', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        card: '0 1px 2px rgba(0,0,0,.4), 0 12px 32px -12px rgba(0,0,0,.7)',
        glow: '0 0 0 1px rgba(139,92,246,.35), 0 18px 50px -18px rgba(139,92,246,.55)',
      },
      backgroundImage: {
        'accent-gradient': 'linear-gradient(120deg, #A78BFA 0%, #F472B6 100%)',
      },
      keyframes: {
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        shimmer: 'shimmer 1.6s infinite',
        'fade-up': 'fade-up .35s ease-out both',
      },
    },
  },
  plugins: [],
}
