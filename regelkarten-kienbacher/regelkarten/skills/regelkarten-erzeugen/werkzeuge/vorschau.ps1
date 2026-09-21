# Exportiert die Folie einer Regelkarte als PNG, damit sie angesehen werden kann.
#
#   powershell -ExecutionPolicy Bypass -File vorschau.ps1 -Pptx "...\RK-010_...pptx"
#
# Nutzt die PowerPoint-Automatisierung. Zwei Dinge sind dabei wichtig und hier
# beruecksichtigt: Die Datei wird aus einer lokalen Kopie geoeffnet (aus OneDrive
# heraus landet sie sonst in der geschuetzten Ansicht), und eine bereits
# laufende PowerPoint-Sitzung des Benutzers wird nicht beendet.

param(
    [Parameter(Mandatory = $true)][string]$Pptx,
    [string]$Png = "",
    [int]$Breite = 1654,   # 200 dpi bei 210 mm
    [int]$Hoehe  = 2339    # 200 dpi bei 297 mm
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Pptx)) {
    Write-Error "Datei nicht gefunden: $Pptx"
    exit 1
}
if ([string]::IsNullOrWhiteSpace($Png)) {
    $Png = [IO.Path]::ChangeExtension((Resolve-Path -LiteralPath $Pptx).Path, '.png')
}

$lokal = Join-Path $env:TEMP ([IO.Path]::GetFileName($Pptx))
Copy-Item -LiteralPath $Pptx -Destination $lokal -Force
try { Unblock-File -LiteralPath $lokal } catch { }

# Lief PowerPoint schon? Dann am Ende nicht beenden - sonst schliesst dieses
# Skript dem Benutzer seine offene Arbeit weg.
$liefVorher = @(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count -gt 0

$app = $null
$pres = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    # Open(FileName, ReadOnly, Untitled, WithWindow)
    $pres = $app.Presentations.Open($lokal, $true, $true, $false)

    if ($pres.Slides.Count -ne 1) {
        throw "Erwartet genau eine Folie, gefunden $($pres.Slides.Count)"
    }
    $b = [math]::Round($pres.PageSetup.SlideWidth)
    $h = [math]::Round($pres.PageSetup.SlideHeight)
    if ($b -ne 595 -or $h -ne 842) {
        throw "Foliengroesse $b x $h pt statt 595 x 842 pt (A4 hoch)"
    }

    $pres.Slides.Item(1).Export($Png, 'PNG', $Breite, $Hoehe)
    Write-Output $Png
}
finally {
    if ($pres) {
        $pres.Close()
        [Runtime.InteropServices.Marshal]::ReleaseComObject($pres) | Out-Null
    }
    if ($app -and -not $liefVorher) { $app.Quit() }
    if ($app) { [Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null }
    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
    Remove-Item -LiteralPath $lokal -Force -ErrorAction SilentlyContinue
}
