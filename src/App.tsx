import { useState, useRef, useEffect, useCallback } from 'react'
import { GitPanel } from './GitPanel'
import { FilesPanel } from './FilesPanel'

// ── Types ─────────────────────────────────────────────────────────────────────
type EventKind = 'boot' | 'rag_search' | 'rag_done' | 'wave_start' | 'agent_start' | 'agent_done' | 'pipeline_done' | 'error'

interface ChatItem {
  id: string
  kind: EventKind | 'user'
  agent?: string
  role?: string
  content?: string
  outputVar?: string
  stepId?: number
  ragChunks?: RagChunk[]
  waveAgents?: string[]
  parallel?: boolean
}

interface RagChunk { score: number; text: string; source: string }

interface SquadInfo {
  label: string; icon: string; workflow: string
  pipelines: string[]; input_key: string; color: string; agents: string[]
}

type SquadCatalog = Record<string, SquadInfo>

const API = 'http://localhost:8000'
const ROOT = 'C:/Users/huggs/OneDrive/Documentos/workspace/ai-lab/antigravity-ide'

// Workflow phase config — maps output_var → phase metadata
const PHASE_META: Record<string, { label: string; icon: string; color: string }> = {
  specification:  { label: 'Spec',   icon: '📋', color: 'text-violet-400 border-violet-800/40 bg-violet-950/20' },
  design:         { label: 'Design', icon: '🏗️',  color: 'text-blue-400   border-blue-800/40   bg-blue-950/20'   },
  task_list:      { label: 'Tasks',  icon: '✅',  color: 'text-emerald-400 border-emerald-800/40 bg-emerald-950/20' },
  hooks_and_mcps: { label: 'Hooks',  icon: '🔌',  color: 'text-amber-400  border-amber-800/40  bg-amber-950/20'  },
}

const AGENT_META: Record<string, { color: string; avatar: string }> = {
  'Planner':    { color: 'text-violet-400', avatar: '📋' },
  'Architect':  { color: 'text-blue-400',   avatar: '🏗️' },
  'Executor':   { color: 'text-emerald-400',avatar: '✅' },
  'Integrator': { color: 'text-amber-400',  avatar: '🔌' },
  'Uncle Bob':  { color: 'text-violet-400', avatar: '🏛️' },
  'Linus':      { color: 'text-cyan-400',   avatar: '🔧' },
  'Kent Beck':  { color: 'text-emerald-400',avatar: '🧪' },
  'Mitnick':    { color: 'text-rose-400',   avatar: '🔒' },
  'Sonar':      { color: 'text-amber-400',  avatar: '📡' },
  'Fowler':     { color: 'text-blue-400',   avatar: '🏗️' },
  'Locust':     { color: 'text-orange-400', avatar: '⚡' },
  'Warlock':    { color: 'text-red-400',    avatar: '⚔️' },
  'Amanda':     { color: 'text-pink-400',   avatar: '🛡️' },
  'Shura':      { color: 'text-yellow-400', avatar: '⚖️' },
  'Terraform':  { color: 'text-teal-400',   avatar: '🌍' },
  'Kubernetes': { color: 'text-sky-400',    avatar: '☸️' },
  'Gitlab':     { color: 'text-orange-300', avatar: '🦊' },
  'SRE':        { color: 'text-lime-400',   avatar: '📊' },
}

const SQUAD_COLORS: Record<string, { tab: string; dot: string }> = {
  cyan:    { tab: 'text-cyan-400 border-cyan-500',    dot: 'bg-cyan-500'    },
  emerald: { tab: 'text-emerald-400 border-emerald-500', dot: 'bg-emerald-500' },
  amber:   { tab: 'text-amber-400 border-amber-500',  dot: 'bg-amber-500'   },
  purple:  { tab: 'text-purple-400 border-purple-500', dot: 'bg-purple-500' },
  rose:    { tab: 'text-rose-400 border-rose-500',    dot: 'bg-rose-500'    },
}

function uid() { return Math.random().toString(36).slice(2) }

// ── Markdown renderer ─────────────────────────────────────────────────────────
function Md({ text }: { text: string }) {
  const parts = text.split(/(```[\s\S]*?```)/g)
  return (
    <div className="leading-relaxed">
      {parts.map((part, i) => {
        if (part.startsWith('```')) {
          const lines = part.split('\n')
          const lang  = lines[0].replace('```', '').trim()
          const code  = lines.slice(1, -1).join('\n')
          return (
            <div key={i} className="my-2.5 rounded-lg overflow-hidden border border-white/5">
              {lang && <div className="px-3 py-1 bg-black/40 text-[9px] text-slate-500 uppercase tracking-widest font-mono">{lang}</div>}
              <pre className="p-3.5 bg-black/30 text-[11px] text-slate-300 font-mono overflow-x-auto leading-6 whitespace-pre-wrap">
                <code>{code}</code>
              </pre>
            </div>
          )
        }
        return (
          <span key={i} className="text-[13px]" dangerouslySetInnerHTML={{
            __html: part
              .replace(/\*\*(.+?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>')
              .replace(/`([^`\n]+)`/g, '<code class="bg-black/30 text-cyan-300 px-1 py-px rounded text-[11px] font-mono">$1</code>')
              .replace(/^#{1,3} (.+)$/gm, '<div class="text-white font-semibold mt-3 mb-1 text-sm">$1</div>')
              .replace(/^- \[ \] (.+)$/gm, '<div class="flex items-start gap-2 my-0.5"><span class="text-slate-600 shrink-0 mt-px">□</span><span>$1</span></div>')
              .replace(/^- \[x\] (.+)$/gm, '<div class="flex items-start gap-2 my-0.5"><span class="text-emerald-500 shrink-0 mt-px">✓</span><span class="line-through text-slate-500">$1</span></div>')
              .replace(/^- (.+)$/gm, '<div class="flex items-start gap-2 my-0.5"><span class="text-slate-600 shrink-0">·</span><span>$1</span></div>')
              .replace(/\[APROVADO\]/g, '<span class="text-emerald-400 font-bold">✓ APROVADO</span>')
              .replace(/\[REPROVADO\]/g, '<span class="text-rose-400 font-bold">✗ REPROVADO</span>')
              .replace(/\n/g, '')
          }} />
        )
      })}
    </div>
  )
}

// ── Phase output card ─────────────────────────────────────────────────────────
function PhaseCard({ item }: { item: ChatItem }) {
  const [open, setOpen] = useState(true)
  const meta    = AGENT_META[item.agent ?? '']
  const phase   = item.outputVar ? PHASE_META[item.outputVar] : null
  const running = item.kind === 'agent_start'

  return (
    <div className={`rounded-xl border overflow-hidden ${
      running
        ? 'border-white/8 bg-white/[0.02]'
        : phase
          ? `${phase.color} border`
          : 'border-white/6 bg-white/[0.02]'
    }`}>
      {/* Header */}
      <button
        onClick={() => !running && setOpen(o => !o)}
        className={`w-full flex items-center gap-3 px-4 py-3 text-left transition-colors ${running ? 'cursor-default' : 'hover:bg-white/4'}`}
      >
        <span className="text-xl leading-none shrink-0">{meta?.avatar ?? '🤖'}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className={`text-xs font-semibold ${meta?.color ?? 'text-slate-300'}`}>{item.agent}</span>
            {phase && !running && (
              <span className="text-[10px] font-mono text-slate-600">→ {phase.icon} {phase.label}</span>
            )}
          </div>
          {item.role && <div className="text-[10px] text-slate-600 mt-px">{item.role}</div>}
        </div>
        {running ? (
          <div className="flex gap-1 shrink-0">
            {[0,1,2].map(i => (
              <span key={i} className="w-1 h-1 rounded-full bg-slate-500 animate-bounce"
                style={{animationDelay:`${i*120}ms`}}/>
            ))}
          </div>
        ) : (
          !running && <span className="text-[10px] text-slate-700 shrink-0">{open ? '▲' : '▼'}</span>
        )}
      </button>

      {/* Content */}
      {open && !running && item.content && (
        <div className="px-4 pb-4 pt-0.5 border-t border-white/5 text-slate-300">
          <Md text={item.content} />
        </div>
      )}
      {running && (
        <div className="px-4 pb-3 text-[11px] text-slate-600 italic border-t border-white/5 pt-2">
          {item.content ?? 'Processing…'}
        </div>
      )}
    </div>
  )
}

// ── RAG card ──────────────────────────────────────────────────────────────────
function RagCard({ chunks, searching }: { chunks?: RagChunk[]; searching?: boolean }) {
  const [open, setOpen] = useState(false)
  if (searching) return (
    <div className="flex items-center gap-2.5 text-[11px] text-slate-600 py-1 font-mono">
      <span className="flex gap-1">{[0,1,2].map(i => (
        <span key={i} className="w-1 h-1 rounded-full bg-violet-700 animate-bounce" style={{animationDelay:`${i*120}ms`}}/>
      ))}</span>
      Searching Antigravity KB…
    </div>
  )
  if (!chunks?.length) return null
  return (
    <div className="border border-violet-900/30 rounded-lg overflow-hidden bg-violet-950/10">
      <button onClick={() => setOpen(o=>!o)}
        className="w-full flex items-center gap-2 px-3 py-2 hover:bg-white/4 transition-colors text-left">
        <span className="text-[11px] text-violet-600">⬡</span>
        <span className="text-[11px] text-violet-500 flex-1">KB · {chunks.length} chunks retrieved</span>
        <span className="text-[9px] text-violet-800">{open ? '▲' : '▼'}</span>
      </button>
      {open && (
        <div className="px-3 pb-3 space-y-2 border-t border-violet-900/20">
          {chunks.map((c,i) => (
            <div key={i} className="mt-2">
              <div className="text-[9px] text-violet-700 font-mono mb-0.5">{c.source} · {(c.score*100).toFixed(0)}%</div>
              <p className="text-[10px] text-slate-500 font-mono leading-relaxed line-clamp-2">{c.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ── Workflow pipeline header ───────────────────────────────────────────────────
function PipelineHeader({ squad }: { squad?: SquadInfo }) {
  if (!squad) return null
  const isProduct = squad.agents.includes('Planner')
  if (!isProduct) return null
  const phases = [
    { key: 'specification',  icon: '📋', label: 'Spec'   },
    { key: 'design',         icon: '🏗️',  label: 'Design' },
    { key: 'task_list',      icon: '✅',  label: 'Tasks'  },
    { key: 'hooks_and_mcps', icon: '🔌',  label: 'Hooks'  },
  ]
  return (
    <div className="flex items-center gap-1 px-4 py-2.5 border-b border-white/[0.05] bg-white/[0.01] shrink-0 overflow-x-auto">
      {phases.map((p, i) => (
        <div key={p.key} className="flex items-center gap-1 shrink-0">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white/[0.03] border border-white/[0.06]">
            <span className="text-xs leading-none">{p.icon}</span>
            <span className="text-[10px] text-slate-500 font-medium">{p.label}</span>
          </div>
          {i < phases.length - 1 && (
            <span className="text-slate-800 text-xs mx-0.5">→</span>
          )}
        </div>
      ))}
    </div>
  )
}

// ── Main App ──────────────────────────────────────────────────────────────────
export default function App() {
  const [items, setItems] = useState<ChatItem[]>([])
  const [input, setInput] = useState('')
  const [streaming, setStreaming] = useState(false)
  const [selectedSquad, setSelectedSquad] = useState('product_squad')
  const [catalog, setCatalog] = useState<SquadCatalog>({})
  const [ragEnabled, setRagEnabled] = useState(true)
  const [spend, setSpend] = useState(0)
  
  const [leftW, setLeftW] = useState(320)
  const [reviewW, setReviewW] = useState(280)
  const [filesW, setFilesW] = useState(280)
  const widths = useRef({ left: 320, review: 280, files: 280 })
  const resizing = useRef<'left' | 'review' | 'files' | null>(null)

  const bottomRef   = useRef<HTMLDivElement>(null)
  const abortRef    = useRef<AbortController | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    function onMouseMove(e: MouseEvent) {
      if (!resizing.current) return
      if (resizing.current === 'left') {
        const w = Math.max(150, Math.min(e.clientX, 500))
        widths.current.left = w
        setLeftW(w)
      } else if (resizing.current === 'review') {
        const w = window.innerWidth - e.clientX - widths.current.files
        widths.current.review = Math.max(200, Math.min(w, 800))
        setReviewW(widths.current.review)
      } else if (resizing.current === 'files') {
        const w = window.innerWidth - e.clientX
        widths.current.files = Math.max(150, Math.min(w, 600))
        setFilesW(widths.current.files)
      }
    }
    function onMouseUp() {
      if (resizing.current) {
        resizing.current = null
        document.body.style.cursor = 'default'
      }
    }
    window.addEventListener('mousemove', onMouseMove)
    window.addEventListener('mouseup', onMouseUp)
    return () => {
      window.removeEventListener('mousemove', onMouseMove)
      window.removeEventListener('mouseup', onMouseUp)
    }
  }, [])

  const startResize = (pane: 'left' | 'review' | 'files') => (e: React.MouseEvent) => {
    e.preventDefault()
    resizing.current = pane
    document.body.style.cursor = 'col-resize'
  }

  useEffect(() => {
    fetch(`${API}/api/v1/squads`).then(r=>r.json()).then(setCatalog).catch(()=>{})
    fetch(`${API}/health`).then(r=>r.json()).then(d=>setSpend(d.telemetry?.spend??0)).catch(()=>{})
  }, [])

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [items])

  const push = useCallback((item: Omit<ChatItem,'id'>) => {
    setItems(p => [...p, { ...item, id: uid() }])
  }, [])

  const replaceStart = useCallback((agent: string, next: Omit<ChatItem,'id'>) => {
    setItems(prev => {
      const idx = [...prev].map((x,i)=>({x,i})).reverse()
        .find(({x})=>x.kind==='agent_start'&&x.agent===agent)?.i
      if (idx===undefined) return [...prev,{...next,id:uid()}]
      const a=[...prev]; a[idx]={...next,id:a[idx].id}; return a
    })
  }, [])

  const send = useCallback(async () => {
    const prompt = input.trim()
    if (!prompt || streaming) return
    setInput('')
    push({ kind: 'user', content: prompt })
    setStreaming(true)
    abortRef.current = new AbortController()

    try {
      const res = await fetch(`${API}/api/v1/compose`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ squad_name: selectedSquad, user_prompt: prompt, use_rag: ragEnabled }),
        signal: abortRef.current.signal,
      })
      if (!res.body) return
      const reader  = res.body.getReader()
      const decoder = new TextDecoder()
      let buf = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buf += decoder.decode(value, { stream: true })
        const blocks = buf.split('\n\n'); buf = blocks.pop() ?? ''

        for (const raw of blocks) {
          if (!raw.trim()) continue
          const lines = raw.split('\n')
          const ev   = lines.find(l=>l.startsWith('event:'))?.replace('event:','').trim() as EventKind
          const data = lines.find(l=>l.startsWith('data:'))?.replace('data:','').trim()
          if (!ev||!data) continue
          let d: Record<string,any>={}
          try { d=JSON.parse(data) } catch { continue }

          if (ev==='boot')     push({ kind:'boot', content:d.message })
          if (ev==='rag_search') push({ kind:'rag_search' })
          if (ev==='rag_done') {
            setItems(prev=>{
              const idx=[...prev].map((x,i)=>({x,i})).reverse().find(({x})=>x.kind==='rag_search')?.i
              if(idx===undefined) return prev
              const a=[...prev]; a[idx]={kind:'rag_done',ragChunks:d.chunks,id:a[idx].id}; return a
            })
          }
          if (ev==='wave_start') push({ kind:'wave_start', waveAgents:d.agents, parallel:d.parallel })
          if (ev==='agent_start') push({ kind:'agent_start', agent:d.agent, role:d.role, stepId:d.step_id, content:d.description })
          if (ev==='agent_done')  replaceStart(d.agent,{ kind:'agent_done', agent:d.agent, role:d.role, stepId:d.step_id, outputVar:d.output_var, content:d.content })
          if (ev==='pipeline_done') {
            push({ kind:'pipeline_done', content:d.message })
            setSpend(p=>p+0.001)
          }
          if (ev==='error') push({ kind:'error', content:d.message })
        }
      }
    } catch(e:any) {
      if(e.name!=='AbortError') push({ kind:'error', content:e.message })
    } finally { setStreaming(false) }
  }, [input, streaming, selectedSquad, ragEnabled, push, replaceStart])

  const squad = catalog[selectedSquad]
  const squadColor = squad ? (SQUAD_COLORS[squad.color] ?? SQUAD_COLORS.cyan) : SQUAD_COLORS.cyan

  function renderItem(item: ChatItem) {
    if (item.kind === 'user') return (
      <div className="flex justify-end">
        <div className="max-w-[80%] bg-white/[0.06] border border-white/[0.08] rounded-2xl rounded-tr-md px-4 py-2.5 text-sm text-slate-200 leading-relaxed">
          {item.content}
        </div>
      </div>
    )
    if (item.kind === 'rag_search') return <RagCard searching />
    if (item.kind === 'rag_done')   return <RagCard chunks={item.ragChunks} />
    if (item.kind === 'wave_start') return (
      <div className="flex items-center gap-2 py-0.5">
        <div className="flex-1 h-px bg-white/[0.04]"/>
        <span className="flex items-center gap-1 shrink-0">
          {item.waveAgents?.map(a => <span key={a} title={a} className="text-sm">{AGENT_META[a]?.avatar ?? '🤖'}</span>)}
          {item.parallel && <span className="text-[9px] text-slate-700 font-mono ml-1">parallel</span>}
        </span>
        <div className="flex-1 h-px bg-white/[0.04]"/>
      </div>
    )
    if (item.kind === 'agent_start' || item.kind === 'agent_done') return <PhaseCard item={item} />
    if (item.kind === 'pipeline_done') return (
      <div className="flex items-center gap-2.5 px-4 py-2.5 rounded-xl bg-emerald-950/20 border border-emerald-900/30 text-emerald-400 text-xs font-mono">
        <span>✓</span><span className="flex-1">{item.content}</span>
      </div>
    )
    if (item.kind === 'error') return (
      <div className="flex items-center gap-2.5 px-4 py-2.5 rounded-xl bg-rose-950/20 border border-rose-900/30 text-rose-400 text-xs font-mono">
        <span>✗</span><span>{item.content}</span>
      </div>
    )
    if (item.kind === 'boot') return (
      <div className="flex items-center gap-2 py-0.5">
        <div className="flex-1 h-px bg-white/[0.04]"/>
        <span className="text-[10px] text-slate-700 font-mono shrink-0 px-2">{item.content}</span>
        <div className="flex-1 h-px bg-white/[0.04]"/>
      </div>
    )
    return null
  }

  return (
    <div className="flex h-screen bg-[#0c0c0e] text-slate-300 antialiased overflow-hidden">

      {/* ── Sidebar Container ── */}
      <div style={{ width: leftW }} className="border-r border-white/[0.05] flex shrink-0 bg-[#121216] relative group h-full">
        <div onMouseDown={startResize('left')} className="absolute -right-1 top-0 bottom-0 w-2 cursor-col-resize hover:bg-violet-500/50 z-20 group-hover:bg-white/[0.05] transition-colors" />
        
        {/* Activity Bar */}
        <div className="w-12 border-r border-white/[0.05] flex flex-col items-center py-3 gap-4 shrink-0 bg-[#0c0c0e]">
          <div className="text-slate-400 hover:text-white cursor-pointer"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
          <div className="text-violet-500 hover:text-violet-400 cursor-pointer bg-violet-500/10 p-1.5 rounded-xl"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>
          <div className="text-slate-400 hover:text-white cursor-pointer"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><path d="M18 9v6"/><path d="M6 9v2.5a3.5 3.5 0 0 0 3.5 3.5h5"/></svg></div>
          <div className="text-slate-400 hover:text-white cursor-pointer"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
          <div className="text-slate-400 hover:text-white cursor-pointer"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg></div>
          <div className="text-slate-400 hover:text-white cursor-pointer"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M12 2a9 9 0 0 0-9 9v11a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V11a9 9 0 0 0-9-9z"/><circle cx="9" cy="11" r="1"/><circle cx="15" cy="11" r="1"/></svg></div>

          <div className="mt-auto flex flex-col gap-4 items-center mb-2">
            <div className="text-slate-400 hover:text-white cursor-pointer relative">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              <div className="absolute -bottom-1 -right-1 w-3.5 h-3.5 bg-violet-500 rounded-full flex items-center justify-center border border-[#1e1e1e]"><span className="text-[8px] text-white font-bold">✓</span></div>
            </div>
            <div className="text-slate-400 hover:text-white cursor-pointer"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></div>
          </div>
        </div>

        {/* Primary Sidebar */}
        <div className="flex-1 flex flex-col min-w-0 bg-[#16161a]">
          <div className="px-4 py-[13px] flex items-center justify-between text-[11px] font-semibold text-slate-200 uppercase tracking-widest border-b border-white/[0.05]">
            <span>KIRO</span>
            <span className="text-slate-500 hover:text-slate-300 cursor-pointer">•••</span>
          </div>
          
          <div className="flex-1 overflow-y-auto">
            
            {/* SPECS Section */}
            <div className="border-b border-white/[0.05]">
              <div className="px-3 py-2.5 flex items-center gap-1.5 text-[10px] font-bold text-slate-200 cursor-pointer hover:bg-white/[0.02]">
                <span className="text-slate-500">▼</span> SPECS
              </div>
              <div className="px-5 pb-4 pt-2 text-center">
                <p className="text-[11px] text-slate-300 mb-3 leading-relaxed">Create a project plan to develop complex features and services</p>
                <button className="w-full py-1.5 bg-[#2d2d31]/50 hover:bg-[#2d2d31] border border-white/5 rounded-md text-[11px] font-medium text-slate-200 transition-colors flex items-center justify-center gap-1.5 shadow-sm">
                  <span className="text-sm leading-none">+</span> Create New Spec
                </button>
              </div>
            </div>

            {/* AGENT HOOKS Section */}
            <div className="border-b border-white/[0.05]">
              <div className="px-3 py-2.5 flex items-center gap-1.5 text-[10px] font-bold text-slate-200 cursor-pointer hover:bg-white/[0.02]">
                <span className="text-slate-500">▼</span> AGENT HOOKS
              </div>
              <div className="px-5 pb-4 pt-2 text-center">
                <p className="text-[11px] text-slate-300 mb-3 leading-relaxed">Automate tasks like documentation, code cleanup, or language localization</p>
                <button className="w-full py-1.5 bg-[#2d2d31]/50 hover:bg-[#2d2d31] border border-white/5 rounded-md text-[11px] font-medium text-slate-200 transition-colors flex items-center justify-center gap-1.5 shadow-sm">
                  <span className="text-sm leading-none">+</span> Create New Hook
                </button>
              </div>
            </div>

            {/* AGENT STEERING & SKILLS Section */}
            <div className="border-b border-white/[0.05]">
              <div className="px-3 py-2.5 flex items-center gap-1.5 text-[10px] font-bold text-slate-200 cursor-pointer hover:bg-white/[0.02]">
                <span className="text-slate-500">▼</span> AGENT STEERING & SKILLS
              </div>
              <div className="px-5 pb-4 pt-2 text-center">
                <p className="text-[11px] text-slate-300 mb-3 leading-relaxed">Guide agent behavior and responses</p>
                <button className="w-full py-1.5 bg-[#2d2d31]/50 hover:bg-[#2d2d31] border border-white/5 rounded-md text-[11px] font-medium text-slate-200 transition-colors shadow-sm">
                  Generate Steering Docs
                </button>
              </div>
            </div>

            {/* MCP SERVERS Section */}
            <div className="">
              <div className="px-3 py-2.5 flex items-center gap-1.5 text-[10px] font-bold text-slate-200 cursor-pointer hover:bg-white/[0.02]">
                <span className="text-slate-500">▼</span> MCP SERVERS
              </div>
              <div className="px-4 py-1 space-y-2 pb-4">
                
                <div className="flex items-center gap-2 group">
                  <span className="text-rose-400 shrink-0"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg></span>
                  <span className="text-[11px] text-slate-300 truncate">power-postman-postman</span>
                  <span className="text-[10px] text-slate-500 shrink-0">Unauthenticated</span>
                  <span className="text-[10px] text-violet-400 hover:text-violet-300 cursor-pointer ml-auto shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">Authenticate</span>
                </div>

                <div className="flex items-center gap-2 group">
                  <span className="text-rose-400 shrink-0"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg></span>
                  <span className="text-[11px] text-slate-300 truncate">power-supabase-local</span>
                  <span className="text-[10px] text-slate-500 shrink-0">Connection Failed</span>
                  <span className="text-[10px] text-violet-400 hover:text-violet-300 cursor-pointer ml-auto shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">Retry</span>
                </div>

                <div className="flex items-center gap-2 group">
                  <span className="text-rose-400 shrink-0"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg></span>
                  <span className="text-[11px] text-slate-300 truncate">power-ssh-machine-mana...</span>
                  <span className="text-[10px] text-slate-500 shrink-0">Connecti...</span>
                  <span className="text-[10px] text-violet-400 hover:text-violet-300 cursor-pointer ml-auto shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">Retry</span>
                </div>

              </div>
            </div>

          </div>
        </div>
      </div>

      {/* ── Chat ── */}
      <div className="flex-1 flex flex-col min-w-0">

        {/* Top bar */}
        <div className="flex items-center justify-between px-5 py-[13px] border-b border-white/[0.05] shrink-0 bg-[#0c0c0e]">
          <div className="flex items-center gap-3">
            <span className="text-lg leading-none">🧠</span>
            <div className="flex flex-col">
              <span className="text-sm font-semibold text-slate-200 tracking-tight">Mecha Orquestrator</span>
              <span className="text-[10px] text-slate-500">Autonomous Squad Routing Active</span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setRagEnabled(r => !r)}
              className={`flex items-center gap-1.5 text-[10px] px-2.5 py-1.5 rounded-lg border transition-all ${
                ragEnabled
                  ? 'border-violet-800/50 text-violet-400 bg-violet-950/30'
                  : 'border-white/[0.06] text-slate-600 hover:text-slate-400'
              }`}
            >
              <span className="text-xs">⬡</span>
              <span>KB</span>
            </button>
            <button onClick={() => setItems([])}
              className="text-[10px] text-slate-700 hover:text-slate-400 transition-colors px-1.5">
              Clear
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-5 py-5 space-y-3">
          {items.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center select-none opacity-80 mt-[-5vh]">
              <div className="font-mono text-[10px] text-violet-500/30 whitespace-pre mb-6 leading-[1.6] select-none tracking-widest">
{`M E C H A   N O D E
 S U P E R   P R O M P T S
  K N O T   O R C H E S T R A T O R
X O R I G I N   Z E R O`}
              </div>
              <div className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-b from-slate-100 to-slate-500 mb-2 tracking-widest uppercase">
                Mecha
              </div>
              <div className="text-[10px] uppercase tracking-[0.4em] text-slate-500 font-bold mb-8">
                Super Prompts Knot
              </div>
              
              <div className="flex flex-col items-center gap-2 text-[11px] text-slate-600 font-medium mb-8">
                <div className="flex items-center gap-1.5">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>
                  <span>System Initialized</span>
                </div>
                <div>Awaiting <span className="text-violet-400 font-semibold">telemetry</span></div>
              </div>

              {/* Prompt Cards Grid */}
              <div className="grid grid-cols-3 gap-3 w-full max-w-2xl mx-auto px-4">
                {[
                  { 
                    id: 'vanessa', 
                    icon: '🐺', 
                    title: 'Vanessa (Anúbis)', 
                    skills: ['Systemic Analysis', 'Lore Auditing', 'RAG Alignment'],
                    strengths: 'Uncovers hidden flow dependencies, manages RSD check-sums, and secures raw narrative logic.',
                    prompt: '---\nMETADATA:\n  Active Skills: [front-end-system-design, mecha-backend-engineering, mecha-agentic-workflow]\n  Commit Standard: Conventional Commits with Quality Gate v2.0\n  Squad Focus: Vanessa (Anúbis - Lore / Control)\n---\n/knot vanessa:\n\nFocus: Systemic Analysis & Lore\nContext: \nQuery: ' 
                  },
                  { 
                    id: 'hugo', 
                    icon: '📡', 
                    title: 'Hugo (Thoth)', 
                    skills: ['Telemetry/SMS', 'System Arch', 'Improbability Tuning'],
                    strengths: 'Secures architectural alignment, constructs clean APIs, and designs robust database schemas.',
                    prompt: '---\nMETADATA:\n  Active Skills: [front-end-system-design, mecha-backend-engineering, mecha-agentic-workflow]\n  Commit Standard: Conventional Commits with Quality Gate v2.0\n  Squad Focus: Hugo (Thoth - Telemetry / SMS)\n---\n/knot hugo:\n\nFocus: Architecture & Telemetry\nFeature: \nQuery: ' 
                  },
                  { 
                    id: 'amanda', 
                    icon: '📦', 
                    title: 'Amanda (Maat)', 
                    skills: ['Product Design', 'Flow Safety', 'UX Strategy'],
                    strengths: 'Acts as the compliance and quality gatekeeper, smoothing user flows and proving business value.',
                    prompt: '---\nMETADATA:\n  Active Skills: [front-end-system-design, mecha-backend-engineering, mecha-agentic-workflow]\n  Commit Standard: Conventional Commits with Quality Gate v2.0\n  Squad Focus: Amanda (Maat - Product / UX Flow)\n---\n/knot amanda:\n\nFocus: Product & UX Flow\nFeature: \nQuery: ' 
                  },
                  { 
                    id: 'rodolfo', 
                    icon: '⚒️', 
                    title: 'Rodolfo (Hefesto)', 
                    skills: ['.NET Engineering', 'Forja de Estrutura', 'Code Review'],
                    strengths: 'Constructs highly resilient, enterprise-grade backend microservices and reviews complex logic.',
                    prompt: '---\nMETADATA:\n  Active Skills: [front-end-system-design, mecha-backend-engineering, mecha-agentic-workflow]\n  Commit Standard: Conventional Commits with Quality Gate v2.0\n  Squad Focus: Rodolfo (Hefesto - .NET Engineering / Code Review)\n---\n/knot rodolfo:\n\nFocus: .NET Engineering & Code Review\nService: \nQuery: ' 
                  },
                  { 
                    id: 'henrique', 
                    icon: '⚡', 
                    title: 'Henrique (Hermes)', 
                    skills: ['DevOps Pipeline', 'DBA & Queries', 'Husky Automation'],
                    strengths: 'Optimizes database query bottlenecks, streamlines CI/CD environments, and automates pre-commits.',
                    prompt: '---\nMETADATA:\n  Active Skills: [front-end-system-design, mecha-backend-engineering, mecha-agentic-workflow]\n  Commit Standard: Conventional Commits with Quality Gate v2.0\n  Squad Focus: Henrique (Hermes - DevOps / DBA)\n---\n/knot henrique:\n\nFocus: DevOps & DBA\nInfrastructure: \nQuery: ' 
                  },
                  { 
                    id: 'felipe', 
                    icon: '🛡️', 
                    title: 'Felipe (Prometeu)', 
                    skills: ['CyberSec Audits', 'Alpha Security', 'Threat Hunting'],
                    strengths: 'Hardens authentication protocols, scans code vulnerabilities, and deploys strict containment shield firewalls.',
                    prompt: '---\nMETADATA:\n  Active Skills: [front-end-system-design, mecha-backend-engineering, mecha-agentic-workflow]\n  Commit Standard: Conventional Commits with Quality Gate v2.0\n  Squad Focus: Felipe (Prometeu - CyberSec / AlphaTM)\n---\n/knot felipe:\n\nFocus: CyberSec & AlphaTM\nComponent: \nQuery: ' 
                  },
                ].map(card => (
                  <button
                    key={card.id}
                    onClick={() => {
                      setInput(card.prompt)
                      setTimeout(() => textareaRef.current?.focus(), 10)
                    }}
                    className="flex flex-col items-start gap-2 p-3.5 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/[0.06] hover:border-violet-500/40 transition-all text-left group relative"
                  >
                    {/* Tooltip Hover Box (Detailed Skills & Strengths) */}
                    <div className="absolute bottom-[108%] mb-1.5 left-1/2 -translate-x-1/2 w-64 p-3.5 bg-[#121216]/98 border border-white/10 rounded-xl shadow-2xl opacity-0 scale-95 pointer-events-none group-hover:opacity-100 group-hover:scale-100 transition-all duration-200 z-50 flex flex-col gap-2.5 backdrop-blur-md">
                      <div className="text-[9px] font-bold uppercase tracking-wider text-slate-500 border-b border-white/5 pb-1">Skills & Core Strengths</div>
                      <div className="flex flex-wrap gap-1">
                        {card.skills.map(s => (
                          <span key={s} className="text-[8.5px] font-mono px-2 py-0.5 rounded bg-white/5 border border-white/10 text-slate-300">
                            {s}
                          </span>
                        ))}
                      </div>
                      <div className="p-2 rounded bg-emerald-500/5 border border-emerald-500/10 text-emerald-400 text-[9.5px] leading-relaxed">
                        <div className="font-bold uppercase tracking-wider text-[8px] text-emerald-300 mb-0.5">Core Advantage</div>
                        {card.strengths}
                      </div>
                    </div>

                    <div className="flex items-center gap-2 w-full">
                      <span className="text-base grayscale group-hover:grayscale-0 transition-all">{card.icon}</span>
                      <span className="text-[11px] font-semibold text-slate-300 group-hover:text-violet-300 transition-colors">{card.title}</span>
                    </div>
                    <span className="text-[10px] text-slate-600 line-clamp-2 leading-relaxed opacity-60 group-hover:opacity-100 transition-opacity">
                      {card.prompt.replace(/\n/g, ' ')}
                    </span>
                  </button>
                ))}
              </div>

            </div>
          )}
          {items.map(item => (
            <div key={item.id}>{renderItem(item)}</div>
          ))}
          <div ref={bottomRef}/>
        </div>

        {/* Input */}
        <div className="px-5 pb-5 pt-3 border-t border-white/[0.05] shrink-0">
          <div className="relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send()} }}
              disabled={streaming}
              placeholder={
                streaming
                  ? `${squad?.agents[0] ?? 'Agent'} is working…`
                  : squad?.agents.includes('Planner')
                    ? 'Describe what you want to build…'
                    : `Ask ${squad?.label ?? 'a squad'}…`
              }
              rows={3}
              className="w-full bg-white/[0.04] border border-white/[0.08] rounded-2xl px-4 py-3.5 pr-12 text-sm text-slate-200 placeholder-slate-700 focus:outline-none focus:border-white/[0.15] focus:bg-white/[0.05] transition-all resize-none disabled:opacity-40 leading-relaxed"
            />
            <div className="absolute right-3 bottom-3 flex gap-2">
              {streaming ? (
                <button onClick={() => abortRef.current?.abort()}
                  className="p-2 rounded-xl bg-rose-950/60 hover:bg-rose-900/60 text-rose-500 transition-colors border border-rose-900/30">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor">
                    <rect x="5" y="5" width="14" height="14" rx="2"/>
                  </svg>
                </button>
              ) : (
                <button onClick={send} disabled={!input.trim()}
                  className="p-2 rounded-xl bg-white/[0.07] hover:bg-white/[0.12] disabled:opacity-20 text-slate-400 transition-colors border border-white/[0.08]">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="22" y1="2" x2="11" y2="13"/>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                  </svg>
                </button>
              )}
            </div>
          </div>
          <div className="flex items-center justify-between mt-2 px-1">
            <div className="flex items-center gap-4">
              <select className="bg-transparent text-[11px] font-medium text-slate-400 hover:text-slate-200 focus:outline-none cursor-pointer transition-colors" defaultValue="Build">
                <option value="Build">Build</option>
                <option value="Plan">Plan</option>
                <option value="Debug">Debug</option>
              </select>
              <select className="bg-transparent text-[11px] text-slate-500 hover:text-slate-300 focus:outline-none cursor-pointer transition-colors">
                <option>DeepSeek V4 Flash Free</option>
                <option>Antigravity Omni</option>
              </select>
              <select className="bg-transparent text-[11px] text-slate-500 hover:text-slate-300 focus:outline-none cursor-pointer transition-colors">
                <option>Padrão</option>
              </select>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-[9px] text-slate-700">
                <kbd className="bg-white/5 px-1 rounded border border-white/8">↵</kbd> send ·
                <kbd className="bg-white/5 px-1 rounded border border-white/8 ml-1">⇧↵</kbd> newline
              </span>
              <span className="text-[9px] text-slate-700 font-mono">v3 · RAG {ragEnabled ? 'on' : 'off'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* ── Review Sidebar ── */}
      <aside style={{ width: reviewW }} className="border-l border-white/[0.05] flex flex-col shrink-0 bg-[#0c0c0e] relative group">
        <div onMouseDown={startResize('review')} className="absolute -left-1 top-0 bottom-0 w-2 cursor-col-resize hover:bg-violet-500/50 z-20 group-hover:bg-white/[0.05] transition-colors" />
        <div className="flex items-center px-4 py-[9px] border-b border-white/[0.05]">
          <div className="flex items-center gap-4 text-[11px] font-medium">
            <button className="text-white border-b-2 border-white pb-1 -mb-[10px]">Revisão</button>
            <button className="text-slate-500 hover:text-slate-300 pb-1 -mb-[10px] text-sm leading-none">+</button>
          </div>
        </div>
        <GitPanel root={ROOT} />
      </aside>

      {/* ── Files Sidebar ── */}
      <aside style={{ width: filesW }} className="border-l border-white/[0.05] flex flex-col shrink-0 bg-[#0c0c0e] relative group">
        <div onMouseDown={startResize('files')} className="absolute -left-1 top-0 bottom-0 w-2 cursor-col-resize hover:bg-violet-500/50 z-20 group-hover:bg-white/[0.05] transition-colors" />
        <FilesPanel root={ROOT} />
      </aside>

    </div>
  )
}
