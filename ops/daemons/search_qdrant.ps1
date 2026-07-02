# search_qdrant.ps1 — caça 'fudido' / 'pj fudido' nos payloads do Qdrant (READ-ONLY)
# Usa Invoke-RestMethod (sem curl). Varre todas as coleções de cada Qdrant publicado.
$ErrorActionPreference = "SilentlyContinue"

Write-Output "=== Qdrant containers no host ==="
docker ps --format "{{.Names}} :: {{.Ports}}" | Select-String -Pattern "qdrant"
Write-Output ""

$ports = 6333,6335,6334,6336,6337
$term  = 'fudido'   # pega 'fudido' e 'pj fudido edition'

foreach ($p in $ports) {
    $base = "http://localhost:$p"
    try { $cols = (Invoke-RestMethod "$base/collections" -TimeoutSec 5).result.collections.name }
    catch { continue }
    if (-not $cols) { continue }
    Write-Output "porta $p -> coleções: $($cols -join ', ')"
    foreach ($c in $cols) {
        $body = '{"limit":2000,"with_payload":true,"with_vector":false}'
        try { $r = Invoke-RestMethod -Method Post -Uri "$base/collections/$c/points/scroll" -ContentType 'application/json' -Body $body -TimeoutSec 20 }
        catch { Write-Output "  $c : erro no scroll"; continue }
        $pts = $r.result.points
        $hits = 0
        foreach ($pt in $pts) {
            $txt = ($pt.payload | ConvertTo-Json -Depth 8 -Compress)
            if ($txt -match "(?i)$term") {
                $hits++
                $snip = $txt.Substring(0, [Math]::Min(500, $txt.Length))
                Write-Output "  >>> HIT $p/$c  id=$($pt.id)"
                Write-Output "      $snip"
            }
        }
        if ($hits -eq 0) { Write-Output "  $c : 0 hits de '$term' em $($pts.Count) pontos" }
    }
}
Write-Output "=== fim da varredura ==="
