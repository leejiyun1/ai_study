import { Button } from '@/components/ui/button'
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from '@/components/ui/empty'
import { Progress } from '@/components/ui/progress'
import { summarizeBatch } from '@/lib/api'
import { IconCloud } from '@tabler/icons-react'
import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

function UploadPage() {
  const [files, setFiles] = useState([])
  const [progress, setProgress] = useState(0)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const inputRef = useRef(null)
  const navigate = useNavigate()

  const handleUpload = async () => {
    if (files.length === 0 || uploading) return

    try {
      setUploading(true)
      setProgress(20)
      const result = await summarizeBatch(files)
      setProgress(100)

      const completed = result.results.filter((item) => item.status === 'COMPLETED').length
      const failed = result.results.filter((item) => item.status === 'FAILED').length
      setMessage(`완료 ${completed}건 / 실패 ${failed}건`)
      setFiles([])
      if (completed > 0) {
        setTimeout(() => {
          navigate('/search', { state: { refreshAt: Date.now() } })
        }, 500)
      }
    } catch (error) {
      setMessage(`업로드 실패: ${error.message}`)
    } finally {
      setUploading(false)
      setTimeout(() => setProgress(0), 600)
    }
  }

  return (
    <div className="flex flex-col items-center gap-4 w-full">

      {/* 파일 미선택시 Empty 영역 표시 */}
      {files.length === 0 ? (
        <Empty className="border border-dashed" onClick={() => inputRef.current.click()}>
          <EmptyHeader>
            <EmptyMedia variant="icon"><IconCloud /></EmptyMedia>
            <EmptyTitle>PDF 파일을 선택하세요</EmptyTitle>
            <EmptyDescription>클릭하여 파일을 업로드하세요</EmptyDescription>
          </EmptyHeader>
          <EmptyContent>
            <Button variant="outline" size="sm">파일 선택</Button>
          </EmptyContent>
        </Empty>
      ) : (
        <div className="w-full">
          {files.map((file, index) => (
            <p key={index}>{file.name}</p>
          ))}
        </div>
      )}

      {/* 숨겨진 파일 input */}
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        multiple
        className="hidden"
        onChange={(e) => setFiles(Array.from(e.target.files))}
      />

      {/* 업로드 진행률 */}
      {uploading && <Progress value={progress} />}

      {/* 업로드 버튼 */}
      <Button variant="outline" disabled={files.length === 0 || uploading} onClick={handleUpload}>
        업로드
      </Button>
      {message && <p className="text-sm text-muted-foreground">{message}</p>}
    </div>
  )
}

export default UploadPage
