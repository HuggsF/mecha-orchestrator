const { app, BrowserWindow, shell, ipcMain } = require('electron')
const path = require('path')
const fsp = require('fs/promises')
const { execFile } = require('child_process')

const isDev = !app.isPackaged

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 900,
    minHeight: 600,
    backgroundColor: '#0c0c0e',
    titleBarStyle: 'hiddenInset',
    trafficLightPosition: { x: 16, y: 16 },
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
    show: false,
  })

  win.once('ready-to-show', () => win.show())

  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })

  if (isDev) {
    win.loadURL('http://localhost:5173')
    win.webContents.openDevTools()
  } else {
    win.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

// ---- IPC: filesystem ------------------------------------------------------
ipcMain.handle('fs:readDir', async (_e, dirPath) => {
  const entries = await fsp.readdir(dirPath, { withFileTypes: true })
  return entries
    .map((d) => ({ name: d.name, path: path.join(dirPath, d.name), isDir: d.isDirectory() }))
    .sort((a, b) => (a.isDir === b.isDir ? a.name.localeCompare(b.name) : a.isDir ? -1 : 1))
})

ipcMain.handle('fs:readFile', async (_e, filePath) => {
  return await fsp.readFile(filePath, 'utf8')
})

// ---- IPC: git (system git via child_process) ------------------------------
function git(cwd, args) {
  return new Promise((resolve) => {
    execFile('git', args, { cwd, maxBuffer: 16 * 1024 * 1024 }, (err, stdout, stderr) => {
      resolve({ ok: !err, stdout: stdout || '', stderr: stderr || (err ? err.message : '') })
    })
  })
}

ipcMain.handle('git:isRepo', async (_e, cwd) => {
  const r = await git(cwd, ['rev-parse', '--is-inside-work-tree'])
  return r.ok && r.stdout.trim() === 'true'
})

ipcMain.handle('git:status', async (_e, cwd) => {
  const r = await git(cwd, ['status', '--porcelain'])
  if (!r.ok) return { ok: false, error: r.stderr, files: [] }
  const files = r.stdout
    .split('\n')
    .filter(Boolean)
    .map((line) => {
      const x = line[0]
      const y = line[1]
      const file = line.slice(3)
      return { x, y, file, status: (x + y).trim() }
    })
  return { ok: true, files }
})

ipcMain.handle('git:init', async (_e, cwd) => {
  const r = await git(cwd, ['init'])
  return { ok: r.ok, message: r.ok ? r.stdout.trim() || 'Repositorio criado.' : r.stderr }
})

ipcMain.handle('git:diff', async (_e, cwd, file) => {
  let r = await git(cwd, ['diff', '--', file])
  if (r.ok && r.stdout.trim()) return r.stdout
  r = await git(cwd, ['diff', '--cached', '--', file])
  if (r.ok && r.stdout.trim()) return r.stdout
  try {
    const content = await fsp.readFile(path.join(cwd, file), 'utf8')
    return content
      .split('\n')
      .map((l) => '+ ' + l)
      .join('\n')
  } catch {
    return '(sem diff disponivel)'
  }
})

ipcMain.handle('git:runQualityGate', async (_e, cwd) => {
  return new Promise((resolve) => {
    const { exec } = require('child_process')
    exec('node scripts/quality-gate.js', { cwd }, (err, stdout, stderr) => {
      resolve({ ok: !err, output: stdout || stderr || '' })
    })
  })
})

app.whenReady().then(() => {
  createWindow()
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
