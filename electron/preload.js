// Electron preload -- exposes safe IPC bridge to the renderer
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('antigravity', {
  version: '3.0.0',
  platform: process.platform,
  fs: {
    readDir: (p) => ipcRenderer.invoke('fs:readDir', p),
    readFile: (p) => ipcRenderer.invoke('fs:readFile', p),
  },
  git: {
    isRepo: (cwd) => ipcRenderer.invoke('git:isRepo', cwd),
    status: (cwd) => ipcRenderer.invoke('git:status', cwd),
    init: (cwd) => ipcRenderer.invoke('git:init', cwd),
    diff: (cwd, file) => ipcRenderer.invoke('git:diff', cwd, file),
  },
})
