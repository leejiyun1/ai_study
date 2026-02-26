import Header from '@/components/Header'
import { BrowserRouter, Route, Routes, useLocation } from 'react-router-dom'
import MainPage from './pages/MainPage'
import SearchPage from './pages/SearchPage'
import UploadPage from './pages/UploadPage'

function Layout() {
  const location = useLocation()
  const showBack = location.pathname !== '/'
  const isSearchPage = location.pathname === '/search'

  const titles = {
    '/': 'PDF 요약 및 검색',
    '/upload': 'PDF 업로드',
    '/search': '문서 검색',
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header title={titles[location.pathname]} showBack={showBack} />
      <div className="flex-1 flex justify-center">
        <div className={`w-full p-4 ${isSearchPage ? 'max-w-6xl' : 'max-w-2xl'}`}>
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/search" element={<SearchPage />} />
          </Routes>
        </div>
      </div>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  )
}

export default App
