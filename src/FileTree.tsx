import { useState, useEffect, useCallback } from 'react'
import { ide, type DirEntry } from './ide-api'
import { FolderIcon, FileIcon, Chevron } from './icons'

function TreeNode({
  entry,
  depth,
  onOpenFile,
}: {
  entry: DirEntry
  depth: number
  onOpenFile?: (p: string) => void
}) {
  const [open, setOpen] = useState(false)
  const [children, setChildren] = useState<DirEntry[] | null>(null)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState(false)

  const toggle = useCallback(async () => {
    if (!entry.isDir) {
      onOpenFile?.(entry.path)
      return
    }
    const next = !open
    setOpen(next)
    if (next && children === null && ide) {
      setLoading(true)
      setErr(false)
      try {
        setChildren(await ide.fs.readDir(entry.path))
      } catch {
        setErr(true)
        setChildren([])
      } finally {
        setLoading(false)
      }
    }
  }, [entry, open, children, onOpenFile])

  return (
    <div>
      <div
        onClick={toggle}
        style={{ paddingLeft: depth * 12 + 8 }}
        className="flex items-center gap-1.5 pr-2 py-[3px] text-[11px] text-slate-400 hover:text-slate-100 hover:bg-white/[0.03] cursor-pointer transition-colors select-none group"
        title={entry.name}
      >
        <span className="w-3 shrink-0 flex justify-center text-slate-600 group-hover:text-slate-400">
          {entry.isDir ? <Chevron open={open} /> : null}
        </span>
        <span className="shrink-0 flex items-center">
          {entry.isDir ? <FolderIcon open={open} /> : <FileIcon name={entry.name} />}
        </span>
        <span className="truncate">{entry.name}</span>
        {err && <span className="text-[8px] text-rose-600 ml-auto pr-1">sem acesso</span>}
      </div>

      {open && entry.isDir && (
        <div>
          {loading && (
            <div style={{ paddingLeft: (depth + 1) * 12 + 26 }} className="text-[10px] text-slate-700 py-0.5">
              carregando...
            </div>
          )}
          {children?.map((c) => (
            <TreeNode key={c.path} entry={c} depth={depth + 1} onOpenFile={onOpenFile} />
          ))}
          {children?.length === 0 && !loading && !err && (
            <div style={{ paddingLeft: (depth + 1) * 12 + 26 }} className="text-[10px] text-slate-700 py-0.5 italic">
              vazio
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export function FileTree({ root, onOpenFile }: { root: string; onOpenFile?: (p: string) => void }) {
  const [entries, setEntries] = useState<DirEntry[] | null>(null)
  const [err, setErr] = useState('')

  useEffect(() => {
    let alive = true
    if (!ide) {
      setErr('IPC indisponivel -- rode o app via Electron (npm run electron:dev)')
      return
    }
    ide.fs
      .readDir(root)
      .then((e) => alive && setEntries(e))
      .catch((e) => alive && setErr(e?.message ?? 'erro ao ler a pasta'))
    return () => {
      alive = false
    }
  }, [root])

  if (err) return <div className="px-4 py-3 text-[11px] text-rose-500/80 leading-relaxed">{err}</div>
  if (!entries) return <div className="px-4 py-3 text-[11px] text-slate-600">carregando arvore...</div>
  if (entries.length === 0) return <div className="px-4 py-3 text-[11px] text-slate-600">pasta vazia</div>

  return (
    <div className="py-1">
      {entries.map((e) => (
        <TreeNode key={e.path} entry={e} depth={0} onOpenFile={onOpenFile} />
      ))}
    </div>
  )
}
