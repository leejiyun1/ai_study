// [Page] 메인 화면 - 업로드/검색 페이지로 이동
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useNavigate } from 'react-router-dom'

function MainPage() {
  const navigate = useNavigate()

  return (
    <div>
      <div className="flex gap-4 p-4 justify-center">
        <Card className="w-48 cursor-pointer" onClick={() => navigate('/upload')}>
          <CardHeader>
            <CardTitle className="text-sm">PDF 업로드</CardTitle>
            <CardDescription>카드를 누르시면 PDF 업로드 페이지로 넘어갑니다.</CardDescription>
          </CardHeader>
        </Card>
        <Card className="w-48 cursor-pointer" onClick={() => navigate('/search')}>
          <CardHeader>
            <CardTitle className="text-sm">문서 검색</CardTitle>
            <CardDescription>카드를 누르시면 문서 검색 페이지로 넘어갑니다.</CardDescription>
          </CardHeader>
        </Card>
      </div>
    </div>
  )
}

export default MainPage