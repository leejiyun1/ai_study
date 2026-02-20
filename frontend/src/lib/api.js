const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options)
  if (!response.ok) {
    let detail = 'API_ERROR'
    try {
      const data = await response.json()
      detail = data?.detail || detail
    } catch {
      // no-op
    }
    throw new Error(detail)
  }
  return response
}

export async function summarizeBatch(files) {
  const formData = new FormData()
  files.forEach((file) => formData.append('files', file))
  const res = await request('/summarize/batch', {
    method: 'POST',
    body: formData,
  })
  return res.json()
}

export async function fetchSummaries() {
  const res = await request('/summaries')
  return res.json()
}

export async function fetchSummaryDetail(id) {
  const res = await request(`/summaries/${id}`)
  return res.json()
}

export function getSummaryDownloadUrl(id) {
  return `${API_BASE}/summaries/${id}/download`
}
