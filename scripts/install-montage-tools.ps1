# تثبيت أدوات المونتاج على Windows (شغّله من PowerShell)
# الأدوات: FFmpeg + Kdenlive + Shotcut + Audacity
$ErrorActionPreference = "Stop"

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Error "winget مش موجود. نزّل 'App Installer' من Microsoft Store وجرب تاني."
}

$apps = @("Gyan.FFmpeg", "KDE.Kdenlive", "Meltytech.Shotcut", "Audacity.Audacity")
foreach ($app in $apps) {
    Write-Host "==> جاري تثبيت $app"
    winget install --id $app -e --accept-source-agreements --accept-package-agreements
}

Write-Host ""
Write-Host "==> تم التثبيت. اقفل PowerShell وافتحه تاني، وبعدين اكتب: ffmpeg -version"
