import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { fetchSummaries, fetchSummaryDetail, getSummaryDownloadUrl } from '@/lib/api'
import { MoreHorizontal } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { useLocation } from 'react-router-dom'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [items, setItems] = useState([])
  const [selectedTitle, setSelectedTitle] = useState('')
  const [selectedSummary, setSelectedSummary] = useState('')
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const location = useLocation()
  const pageSize = 10

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
      setSelectedTitle(detail.title || '(제목 없음)')
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

  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize))

  const paged = useMemo(() => {
    const start = (page - 1) * pageSize
    return filtered.slice(start, start + pageSize)
  }, [filtered, page])

  useEffect(() => {
    loadSummaries()
  }, [location.state?.refreshAt])

  useEffect(() => {
    setPage(1)
  }, [query, items.length])

  useEffect(() => {
    if (page > totalPages) {
      setPage(totalPages)
    }
  }, [page, totalPages])

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
            <TableHead></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {paged.map((item) => (
            <TableRow key={item.id}>
              <TableCell>
                <div className="w-[28vw] min-w-[180px] max-w-[560px] truncate" title={item.title || '-'}>
                  {item.title || '-'}
                </div>
              </TableCell>
              <TableCell>
                <div className="w-[28vw] min-w-[180px] max-w-[560px] truncate" title={item.filename}>
                  {item.filename}
                </div>
              </TableCell>
              <TableCell>{new Date(item.created_at).toLocaleString()}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                      <span className="sr-only">Open menu</span>
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
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
      <div className="flex items-center justify-between">
        <p className="text-xs text-muted-foreground">
          {filtered.length === 0
            ? '0건'
            : `${filtered.length}건 중 ${(page - 1) * pageSize + 1}-${Math.min(page * pageSize, filtered.length)}건`}
        </p>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" disabled={page === 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>
            이전
          </Button>
          <span className="text-sm">{page} / {totalPages}</span>
          <Button
            variant="outline"
            size="sm"
            disabled={page >= totalPages}
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          >
            다음
          </Button>
        </div>
      </div>
      {error && <p className="text-sm text-red-500">{error}</p>}
      {selectedSummary && (
        <>
          <h2 className="text-center text-2xl font-bold">요약본</h2>
          <div className="rounded-md border p-3 text-sm whitespace-pre-wrap">
            <h3 className="mb-2 text-base font-semibold">{selectedTitle}</h3>
            {selectedSummary}
          </div>
        </>
      )}

    </div>
  )
}

export default SearchPage
