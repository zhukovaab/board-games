import { AnimatePresence } from 'framer-motion'
import { Route, Routes, useLocation } from 'react-router-dom'

import { Layout } from './components/Layout'
import { CatalogPage } from './pages/CatalogPage'
import { GamePage } from './pages/GamePage'

export function App() {
  const location = useLocation()

  return (
    <Layout>
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<CatalogPage />} />
          <Route path="/game/:slug" element={<GamePage />} />
          <Route
            path="*"
            element={
              <div className="panel p-14 text-center text-sm text-mist">Страница не найдена</div>
            }
          />
        </Routes>
      </AnimatePresence>
    </Layout>
  )
}
