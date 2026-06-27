import { useState, useEffect, useCallback } from 'react'
import { ide, type GitFile } from './ide-api'

const STAT: Record<string, { label: string; cls: string }> = {
  M: { label: 'M', cls: 'text-amber-400' },
  A: { label: 'A', cls: 'text-emerald-400' },
  D: { label: 'D', cls: 'text-rose-400' },
  R: { label: 'R', cls: 'text-blue-400' },
  C: { label: 'C', cls: 'text-blue-400' },
  '?': { label: 'U', cls: 'text-slate-500' },
}

function badge(f: GitFile) {
  const code = f.status[0] ?? f.x ?? '?'
  return STAT[code] ?? STAT['?']
}

function parseAnsi(text: string) {
  const ansiRegex = /\x1b\[(0|1|31|32|33|35|36)m/g
  const parts = text.split(ansiRegex)
  let isBold = false
  let colorClass = ''
  
  return parts.map((part, index) => {
    if (index % 2 === 1) {
      const code = part
      if (code === '0') {
        isBold = false
        colorClass = ''
      } else if (code === '1') {
        isBold = true
      } else if (code === '31') {
        colorClass = 'text-rose-500'
      } else if (code === '32') {
        colorClass = 'text-emerald-400 font-semibold'
      } else if (code === '33') {
        colorClass = 'text-amber-400'
      } else if (code === '35') {
        colorClass = 'text-fuchsia-400'
      } else if (code === '36') {
        colorClass = 'text-cyan-400'
      }
      return null
    }
    
    if (!part) return null
    return (
      <span key={index} className={`${isBold ? 'font-bold' : ''} ${colorClass}`}>
        {part}
      </span>
    )
  })
}

export function GitPanel({ root }: { root: string }) {
  const [repo, setRepo] = useState<boolean | null>(null)
  const [files, setFiles] = useState<GitFile[]>([])
  const [busy, setBusy] = useState(false)
  const [openFile, setOpenFile] = useState<string | null>(null)
  const [diff, setDiff] = useState('')
  const [err, setErr] = useState('')
  
  const [qualityGateOutput, setQualityGateOutput] = useState<string | null>(null)
  const [gateRunning, setGateRunning] = useState(false)

  const refresh = useCallback(async () => {
    if (!ide?.git) {
      setErr('IPC indisponivel -- rode via Electron')
      setRepo(false)
      return
    }
    setErr('')
    const isRepo = await ide.git.isRepo(root).catch(() => false)
    setRepo(isRepo)
    if (isRepo) {
      const s = await ide.git.status(root).catch(() => ({ ok: false, files: [] as GitFile[] }))
      setFiles(s.files ?? [])
    }
  }, [root])

  useEffect(() => {
    refresh()
  }, [refresh])

  const doInit = useCallback(async () => {
    if (!ide?.git) return
    setBusy(true)
    const r = await ide.git.init(root).catch(() => ({ ok: false, message: 'falha ao iniciar' }))
    setBusy(false)
    if (r.ok) refresh()
    else setErr(r.message)
  }, [root, refresh])

  const showDiff = useCallback(
    async (file: string) => {
      if (openFile === file) {
        setOpenFile(null)
        return
      }
      setOpenFile(file)
      setDiff('')
      if (ide?.git) setDiff(await ide.git.diff(root, file).catch(() => '(erro ao obter diff)'))
    },
    [root, openFile],
  )

  const runGate = useCallback(async () => {
    if (!ide?.git) return
    setGateRunning(true)
    setQualityGateOutput('Processando auditoria do Quality Gate...')
    const r = await ide.git.runQualityGate(root).catch(() => ({ ok: false, output: 'Falha crítica ao iniciar auditoria.' }))
    setQualityGateOutput(r.output)
    setGateRunning(false)
  }, [root])

  return (
    <div className="flex-1 flex flex-col min-h-0">
      <div className="px-4 py-3 border-b border-white/[0.05] flex items-center justify-between">
        <span className="text-[11px] font-medium text-slate-300">Alterações</span>
        <div className="flex items-center gap-2">
          {repo === true && (
            <button
              onClick={runGate}
              disabled={gateRunning}
              title="Executar Quality Gate"
              className={`text-[9px] font-semibold px-2 py-0.5 rounded border transition-all ${
                gateRunning 
                  ? 'border-violet-500/20 text-violet-400 bg-violet-950/20'
                  : 'border-white/5 hover:border-violet-500/30 text-slate-400 hover:text-violet-300'
              }`}
            >
              {gateRunning ? 'Auditing...' : 'Quality Gate'}
            </button>
          )}
          <button
            onClick={refresh}
            title="atualizar"
            className="text-[12px] text-slate-600 hover:text-slate-200 transition-colors leading-none"
          >
            &#10227;
          </button>
        </div>
      </div>

      {repo === null && <div className="px-4 py-3 text-[11px] text-slate-600">verificando git...</div>}
      {err && <div className="px-4 py-2 text-[10px] text-rose-500/80 leading-relaxed">{err}</div>}

      {repo === false && !err && (
        <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
          <div className="text-xs font-semibold text-slate-200 mb-2">Criar um repositório Git</div>
          <p className="text-[11px] text-slate-500 mb-4 leading-relaxed max-w-[200px]">
            Rastreie, revise e desfaça alterações neste projeto
          </p>
          <button
            onClick={doInit}
            disabled={busy}
            className="px-3 py-1.5 bg-white/[0.06] hover:bg-white/10 disabled:opacity-40 text-slate-300 text-[11px] rounded-md transition-colors border border-white/[0.08] font-medium"
          >
            {busy ? 'Criando...' : 'Criar repositório Git'}
          </button>
        </div>
      )}

      {repo === true && (
        <div className="flex-1 flex flex-col min-h-0">
          
          {/* Quality Gate Console Output */}
          {qualityGateOutput && (
            <div className="mx-3 mt-3 p-3 bg-black/40 rounded-xl border border-white/[0.05] flex flex-col min-h-0 shrink-0">
              <div className="flex items-center justify-between pb-1.5 mb-1.5 border-b border-white/5 shrink-0">
                <span className="text-[9px] font-bold uppercase tracking-wider text-slate-500">DevOps Telemetry Output</span>
                <button 
                  onClick={() => setQualityGateOutput(null)}
                  className="text-[8px] text-slate-600 hover:text-slate-400 font-bold"
                >
                  FECHAR
                </button>
              </div>
              <pre className="text-[9.5px] font-mono leading-normal overflow-y-auto max-h-56 whitespace-pre-wrap select-text text-slate-400 scrollbar-none">
                {parseAnsi(qualityGateOutput)}
              </pre>
            </div>
          )}

          <div className="flex-1 overflow-y-auto">
            {files.length === 0 && (
              <div className="px-4 py-6 text-center text-[11px] text-slate-600">nenhuma alteração pendente</div>
            )}
            {files.map((f) => {
              const b = badge(f)
              const on = openFile === f.file
              return (
                <div key={f.file}>
                  <div
                    onClick={() => showDiff(f.file)}
                    className="flex items-center gap-2 px-4 py-[5px] text-[11px] hover:bg-white/[0.03] cursor-pointer transition-colors"
                  >
                    <span className={`w-3 text-center font-mono shrink-0 ${b.cls}`}>{b.label}</span>
                    <span className="truncate text-slate-400">{f.file}</span>
                    <span className="ml-auto text-[8px] text-slate-700 shrink-0">{on ? 'fechar' : 'diff'}</span>
                  </div>
                  {on && (
                    <pre className="mx-3 my-1 p-2 bg-black/40 rounded text-[10px] font-mono text-slate-400 overflow-x-auto max-h-52 overflow-y-auto whitespace-pre-wrap border border-white/5">
                      {diff || 'carregando diff...'}
                    </pre>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  )
}
