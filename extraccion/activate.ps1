# Script de activación rápida del entorno virtual
# Uso: .\activate.ps1

Write-Host "🚀 Activando entorno virtual..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Comandos disponibles:" -ForegroundColor Cyan
Write-Host "  python extract_mt5_data.py  - Extraer datos de MT5" -ForegroundColor Yellow
Write-Host "  python query_mt5_data.py    - Consultar datos de la BD" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Para desactivar: deactivate" -ForegroundColor Cyan
