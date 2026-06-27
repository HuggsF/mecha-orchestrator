// Typed bridge to the Electron main process (exposed by preload.js)

export interface DirEntry {
  name: string
  path: string
  isDir: boolean
}

export interface GitFile {
  x: string
  y: string
  file: string
  status: string
}

export interface GitStatus {
  ok: boolean
  error?: string
  files: GitFile[]
}

interface AntigravityAPI {
  version: string
  platform: string
  fs: {
    readDir: (p: string) => Promise<DirEntry[]>
    readFile: (p: string) => Promise<string>
  }
  git: {
    isRepo: (cwd: string) => Promise<boolean>
    status: (cwd: string) => Promise<GitStatus>
    init: (cwd: string) => Promise<{ ok: boolean; message: string }>
    diff: (cwd: string, file: string) => Promise<string>
  }
}

declare global {
  interface Window {
    antigravity?: AntigravityAPI
  }
}

export const ide: AntigravityAPI | undefined =
  typeof window !== 'undefined' ? window.antigravity : undefined

export const hasIDE = !!ide?.fs
