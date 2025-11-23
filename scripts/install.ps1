# Get_transform 安装脚本 (Windows PowerShell)
# 自动创建虚拟环境并安装依赖

# 获取脚本目录
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🌀 Get_transform 安装向导" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "ℹ️  项目目录: $ProjectRoot" -ForegroundColor Blue
Write-Host "ℹ️  平台: Windows" -ForegroundColor Blue

# 检查 Python
try {
    $PythonVersion = & python --version 2>&1
    Write-Host "✅ Python: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 未安装或不在 PATH 中" -ForegroundColor Red
    Write-Host "ℹ️  请从 https://www.python.org 下载安装 Python 3.6+" -ForegroundColor Blue
    Write-Host "ℹ️  安装时请勾选 'Add Python to PATH' 选项" -ForegroundColor Blue
    pause
    exit 1
}

# 进入项目目录
Set-Location $ProjectRoot

# 检查虚拟环境是否已存在
if (Test-Path ".venv") {
    Write-Host "⚠️  虚拟环境已存在" -ForegroundColor Yellow
    $Response = Read-Host "是否删除并重新创建? (y/N)"
    if ($Response -eq "y" -or $Response -eq "Y") {
        Write-Host "ℹ️  删除旧的虚拟环境..." -ForegroundColor Blue
        Remove-Item -Recurse -Force .venv
    } else {
        Write-Host "ℹ️  使用现有虚拟环境" -ForegroundColor Blue
    }
}

# 创建虚拟环境
if (-not (Test-Path ".venv")) {
    Write-Host "ℹ️  创建虚拟环境..." -ForegroundColor Blue
    & python -m venv .venv
    Write-Host "✅ 虚拟环境创建成功" -ForegroundColor Green
}

# 激活虚拟环境
Write-Host "ℹ️  激活虚拟环境..." -ForegroundColor Blue
& .\.venv\Scripts\Activate.ps1

# 升级 pip
Write-Host "ℹ️  升级 pip..." -ForegroundColor Blue
& python -m pip install --upgrade pip

# 安装依赖
Write-Host "ℹ️  安装项目依赖..." -ForegroundColor Blue
$RequirementsFile = Join-Path $ProjectRoot "Get_transform\requirements.txt"
if (Test-Path $RequirementsFile) {
    & pip install -r $RequirementsFile
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "⚠️  未找到 requirements.txt" -ForegroundColor Yellow
}

# 创建启动脚本 (批处理文件)
Write-Host "ℹ️  创建启动脚本..." -ForegroundColor Blue
$RunBatContent = @'
@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo 启动 Get_transform...
call .venv\Scripts\activate.bat
python Get_transform\launch.py

pause
'@
Set-Content -Path "run.bat" -Value $RunBatContent -Encoding UTF8
Write-Host "✅ 启动脚本创建成功: run.bat" -ForegroundColor Green

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ 安装完成！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 使用方法:"
Write-Host ""
Write-Host "1. 运行程序（推荐）:"
Write-Host "   双击运行: run.bat"
Write-Host "   或在 PowerShell 中: .\run.bat"
Write-Host ""
Write-Host "2. 手动运行:"
Write-Host "   .\.venv\Scripts\Activate.ps1"
Write-Host "   python Get_transform\launch.py"
Write-Host ""
Write-Host "3. 构建可执行文件:"
Write-Host "   .\scripts\build.ps1 -InstallDeps"
Write-Host ""
Write-Host "ℹ️  首次运行会引导你配置导出路径" -ForegroundColor Blue
Write-Host "ℹ️  详细文档请查看 README.md" -ForegroundColor Blue
Write-Host ""
pause
