// [Component] 공통 헤더
import { useNavigate } from 'react-router-dom'

function Header({ title, showBack = false }) {
  const navigate = useNavigate()

  return (
    <header className="w-full">
      <div className="flex items-center justify-center p-4 border-b">
        <h1 className="text-xl font-bold">{title}</h1>
      </div>
    </header>
  )
}

export default Header