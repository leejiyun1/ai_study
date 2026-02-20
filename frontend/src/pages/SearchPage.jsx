import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { fetchSummaries, fetchSummaryDetail, getSummaryDownloadUrl } from '@/lib/api'
import { useEffect, useMemo, useState } from 'react'
import { useLocation } from 'react-router-dom'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [items, setItems] = useState([])
  const [selectedSummary, setSelectedSummary] = useState('')
  const [error, setError] = useState('')
  const location = useLocation()

  const loadSummaries = async () => {
    try {
      setError('')
      const data = await fetchSummaries()
      setItems(data)
    } catch (e) {
      setError(`조회 실패: ${e.message}`)
    }
  }

  const handleView = async (id) => {
    try {
      setError('')
      const detail = await fetchSummaryDetail(id)
      setSelectedSummary(detail.summary || '(요약 없음)')
    } catch (e) {
      setError(`상세 조회 실패: ${e.message}`)
    }
  }

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return items
    return items.filter((item) => (
      `${item.title || ''} ${item.filename || ''}`.toLowerCase().includes(q)
    ))
  }, [items, query])

  useEffect(() => {
    loadSummaries()
  }, [location.state?.refreshAt])

  return (
    <div className="flex flex-col gap-4 w-full">

      {/* 검색창 - 상단 고정 */}
        <div className="flex gap-2 sticky top-0 bg-background py-2">
            <Input
            placeholder="검색어를 입력하세요"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            />
            <Button variant="outline" onClick={loadSummaries}>새로고침</Button>
        </div>

      {/* 검색 결과 테이블 */}
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>제목</TableHead>
            <TableHead>파일명</TableHead>
            <TableHead>날짜</TableHead>
            <TableHead>액션</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((item) => (
            <TableRow key={item.id}>
              <TableCell>{item.title || '-'}</TableCell>
              <TableCell>{item.filename}</TableCell>
              <TableCell>{new Date(item.created_at).toLocaleString()}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="sm">액션</Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuItem onClick={() => handleView(item.id)}>보기</DropdownMenuItem>
                    <DropdownMenuItem onClick={() => window.open(getSummaryDownloadUrl(item.id), '_blank')}>
                      다운로드
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {error && <p className="text-sm text-red-500">{error}</p>}
      {selectedSummary && (
        <div className="rounded-md border p-3 text-sm whitespace-pre-wrap">
          {selectedSummary}
        </div>
      )}

    </div>
  )
}

export default SearchPage
