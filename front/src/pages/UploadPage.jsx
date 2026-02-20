import { Button } from '@/components/ui/button'
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from '@/components/ui/empty'
import { Progress } from '@/components/ui/progress'
import { IconCloud } from '@tabler/icons-react'
import { useRef, useState } from 'react'

function UploadPage() {
  const [files, setFiles] = useState([])
  const [progress, setProgress] = useState(0)
  const [uploading, setUploading] = useState(false)
  const inputRef = useRef(null)

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
      <Button variant="outline" disabled={files.length === 0 || uploading}>업로드</Button>
    </div>
  )
}

export default UploadPage