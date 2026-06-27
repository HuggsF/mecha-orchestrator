// File-type icons (inline SVG, no external dependency)

const EXT_COLOR: Record<string, string> = {
  ts: '#3178c6', tsx: '#3178c6',
  js: '#f1dd35', jsx: '#f1dd35', mjs: '#f1dd35', cjs: '#f1dd35',
  json: '#cbcb41',
  md: '#5b9bd5', mdx: '#5b9bd5',
  py: '#4b8bbe',
  css: '#7d6fff', scss: '#cf649a', sass: '#cf649a',
  html: '#e34c26', htm: '#e34c26',
  svg: '#ffb13b', png: '#a074c4', jpg: '#a074c4', jpeg: '#a074c4', gif: '#a074c4', webp: '#a074c4', ico: '#a074c4',
  toml: '#9c6b3f', yml: '#cb171e', yaml: '#cb171e',
  sh: '#89e051', ps1: '#3a6db5', bat: '#89e051',
  lock: '#6c7079', gitignore: '#6c7079', env: '#d8b430', txt: '#9aa0a6',
  vue: '#41b883', go: '#00add8', rs: '#dea584',
}

export function extOf(name: string): string {
  if (name.startsWith('.') && name.indexOf('.', 1) === -1) return name.slice(1).toLowerCase()
  const i = name.lastIndexOf('.')
  return i > 0 ? name.slice(i + 1).toLowerCase() : ''
}

export function Chevron({ open }: { open: boolean }) {
  return (
    <svg
      width="10" height="10" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"
      style={{ transform: open ? 'rotate(90deg)' : 'none', transition: 'transform .12s' }}
    >
      <polyline points="9 18 15 12 9 6" />
    </svg>
  )
}

export function FolderIcon({ open }: { open?: boolean }) {
  return open ? (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#d6a64a" strokeWidth="1.7"
      strokeLinecap="round" strokeLinejoin="round">
      <path d="M3.5 7.5a1.5 1.5 0 0 1 1.5-1.5h3.6l1.6 1.8h7.3a1.5 1.5 0 0 1 1.5 1.5v.7" />
      <path d="M3 18l1.9-7.2a1 1 0 0 1 1-.8h15.2a1 1 0 0 1 1 1.2L21 18a1.5 1.5 0 0 1-1.5 1.5H4.5A1.5 1.5 0 0 1 3 18z" />
    </svg>
  ) : (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#c9913a" strokeWidth="1.7"
      strokeLinecap="round" strokeLinejoin="round">
      <path d="M3.5 7a1.5 1.5 0 0 1 1.5-1.5h3.6l1.6 1.8h8.3A1.5 1.5 0 0 1 20.5 9v8.5A1.5 1.5 0 0 1 19 19H5a1.5 1.5 0 0 1-1.5-1.5z" />
    </svg>
  )
}

export function FileIcon({ name }: { name: string }) {
  const ext = extOf(name)
  const color = EXT_COLOR[ext] ?? '#7a828f'
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.6"
      strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2.5H6.5A1.5 1.5 0 0 0 5 4v16a1.5 1.5 0 0 0 1.5 1.5h11A1.5 1.5 0 0 0 19 20V7.5z" />
      <polyline points="14 2.5 14 8 19 8" />
    </svg>
  )
}
