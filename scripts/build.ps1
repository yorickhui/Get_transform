# Get_transform 构建脚本 (Windows PowerShell)
# 用法: .\scripts\build.ps1 [-Clean] [-Debug] [-Test] [-InstallDeps]

param(
    [switch]$Clean = $false,
    [switch]$Debug = $false,
    [switch]$Test = $false,
    [switch]$InstallDeps = $false,
    [switch]$Help = $false
)

# 显示帮助
if ($Help) {
    Write-Host ""
    Write-Host "Get_transform 构建工具 (Windows)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "用法: .\scripts\build.ps1 [选项]"
    Write-Host ""
    Write-Host "选项:"
    Write-Host "  -Clean         清理构建目录"
    Write-Host "  -Debug         启用调试模式"
    Write-Host "  -Test          构建后测试"
    Write-Host "  -InstallDeps   安装依赖包"
    Write-Host "  -Help          显示此帮助信息"
    Write-Host ""
    exit 0
}

# 获取脚本目录
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🌀 Get_transform 构建工具" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "ℹ️  项目目录: $ProjectRoot" -ForegroundColor Blue
Write-Host "ℹ️  平台: Windows" -ForegroundColor Blue

# 检查 Python
try {
    $PythonVersion = & python --version 2>&1
    Write-Host "✅ Python: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 未安装或不在 PATH 中" -ForegroundColor Red
    Write-Host "请从 https://www.python.org 下载安装 Python" -ForegroundColor Yellow
    exit 1
}

# 进入项目目录
Set-Location $ProjectRoot

# 安装依赖（如果需要）
if ($InstallDeps) {
    Write-Host "ℹ️  安装依赖包..." -ForegroundColor Blue
    & python -m pip install -r Get_transform\requirements.txt
    & python -m pip install pyinstaller
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
}

# 构建参数
$BuildArgs = @()
if ($Clean) {
    $BuildArgs += "--clean"
}
if ($Debug) {
    $BuildArgs += "--debug"
}
if ($Test) {
    $BuildArgs += "--test"
}

# 运行构建脚本
Write-Host "ℹ️  开始构建..." -ForegroundColor Blue
& python scripts\build_executable.py @BuildArgs

# 检查构建结果
$ExePath = Join-Path $ProjectRoot "dist\get_transform.exe"
if (Test-Path $ExePath) {
    Write-Host "✅ 构建成功！" -ForegroundColor Green
    Write-Host ""
    Write-Host "可执行文件位置: $ExePath"
    $FileSize = (Get-Item $ExePath).Length / 1MB
    Write-Host ("文件大小: {0:N2} MB" -f $FileSize)
    Write-Host ""
    Write-Host "使用方法: .\dist\get_transform.exe"
    Write-Host "或双击运行: dist\get_transform.exe"
} else {
    Write-Host "❌ 构建失败：未找到可执行文件" -ForegroundColor Red
    exit 1
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ 构建完成" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
