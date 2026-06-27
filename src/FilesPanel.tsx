import { useState, useEffect, useCallback } from 'react'
import { ide, type GitFile } from './ide-api'
import { FileTree } from './FileTree'

export function FilesPanel({ root }: { root: string }) {
  const [tab, setTab] = useState<'changes' | 'all'>('all')
  const [count, setCount] = useState(0)
  const [changes, setChanges] = useState<GitFile[]>([])

  const loadStatus = useCallback(async () => {
    if (!ide?.git) return
    const isRepo = await ide.git.isRepo(root).catch(() => false)
    if (!isRepo) {
      setCount(0)
      setChanges([])
      return
    }
    const s = await ide.git.status(root).catch(() => ({ ok: false, files: [] as GitFile[] }))
    setChanges(s.files ?? [])
    setCount(s.files?.length ?? 0)
  }, [root])

  useEffect(() => {
    loadStatus()
  }, [loadStatus])

  const tabCls = (active: boolean) =>
    `flex-1 py-1.5 text-[10px] font-medium rounded-md transition-colors ${
      active
        ? 'bg-[#2d2d31]/50 text-slate-200 shadow-sm border border-white/5'
        : 'bg-transparent text-slate-400 hover:text-slate-300'
    }`

  return (
    <>
      <div className="flex p-2 gap-1 border-b border-white/[0.05] bg-[#0c0c0e]">
        <button onClick={() => setTab('changes')} className={tabCls(tab === 'changes')}>
          {count} {count === 1 ? 'Alteração' : 'Alterações'}
        </button>
        <button onClick={() => setTab('all')} className={tabCls(tab === 'all')}>
          Todos os arquivos
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {tab === 'all' && <FileTree root={root} />}
        {tab === 'changes' && (
          <div className="py-2">
            {changes.length === 0 && (
              <div className="px-4 py-6 text-center text-[11px] text-slate-600">nenhuma alteração</div>
            )}
            {changes.map((f) => (
              <div
                key={f.file}
                className="flex items-center gap-2 px-4 py-[3px] text-[11px] text-slate-400 hover:bg-white/[0.03] transition-colors"
              >
                <span className="w-3 text-center font-mono text-amber-400 shrink-0">{f.status[0] ?? '?'}</span>
                <span className="truncate">{f.file}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  )
}
