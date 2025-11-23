# 📦 Get_transform 构建指南

本文档详细说明如何为 Get_transform 项目构建可执行文件，支持 Windows、macOS 和 Linux 平台。

## 目录

- [快速开始](#快速开始)
- [系统要求](#系统要求)
- [构建方法](#构建方法)
- [安装方法（备选）](#安装方法备选)
- [常见问题](#常见问题)
- [技术细节](#技术细节)

---

## 快速开始

### 一键构建（推荐）

**Linux/macOS:**
```bash
# 方法 1: 使用 Makefile（推荐）
make build

# 方法 2: 使用构建脚本
./scripts/build.sh --install-deps

# 方法 3: 使用 Python 脚本
python3 scripts/build_executable.py --install-pyinstaller
```

**Windows:**
```powershell
# 方法 1: 使用构建脚本（推荐）
.\scripts\build.ps1 -InstallDeps

# 方法 2: 使用 Python 脚本
python scripts\build_executable.py --install-pyinstaller
```

### 快速安装（无需构建）

如果不想构建可执行文件，可以直接安装并运行：

**Linux/macOS:**
```bash
./scripts/install.sh
./run.sh
```

**Windows:**
```powershell
.\scripts\install.ps1
.\run.bat
```

---

## 系统要求

### 构建环境要求

#### 所有平台

- **Python**: 3.6 或更高版本
- **pip**: 最新版本
- **磁盘空间**: 至少 500MB（用于依赖和构建文件）
- **内存**: 至少 1GB RAM

#### Windows

- **操作系统**: Windows 10 或更高版本
- **PowerShell**: 5.1 或更高版本
- **可选**: Visual C++ Redistributable（某些依赖可能需要）

#### macOS

- **操作系统**: macOS 10.15 (Catalina) 或更高版本
- **Xcode Command Line Tools**: 
  ```bash
  xcode-select --install
  ```

#### Linux

- **操作系统**: Ubuntu 18.04+, Debian 10+, CentOS 7+, 或其他主流发行版
- **基础工具**: gcc, make（通常已预装）
  ```bash
  # Ubuntu/Debian
  sudo apt-get install build-essential
  
  # CentOS/RHEL
  sudo yum groupinstall "Development Tools"
  ```

### 运行环境要求（最终用户）

- **无需 Python**: 构建的可执行文件包含所有依赖
- **操作系统**: 
  - Windows 10/11 (64-bit)
  - macOS 10.15+ (Intel/Apple Silicon)
  - Linux (主流发行版)

---

## 构建方法

### 方法 1: Makefile（Linux/macOS 推荐）

Makefile 提供了最简便的构建方式：

```bash
# 查看所有可用命令
make help

# 首次构建（会自动安装 PyInstaller）
make build

# 清理后重新构建
make clean
make build

# 构建调试版本
make build-debug

# 构建并测试
make build
make test

# 完整发布流程
make dist
```

### 方法 2: Shell 脚本（跨平台）

#### Linux/macOS

```bash
# 基本构建
./scripts/build.sh

# 清理后构建
./scripts/build.sh --clean

# 构建并测试
./scripts/build.sh --test

# 安装依赖并构建
./scripts/build.sh --install-deps

# 调试模式
./scripts/build.sh --debug
```

#### Windows (PowerShell)

```powershell
# 基本构建
.\scripts\build.ps1

# 清理后构建
.\scripts\build.ps1 -Clean

# 构建并测试
.\scripts\build.ps1 -Test

# 安装依赖并构建
.\scripts\build.ps1 -InstallDeps

# 调试模式
.\scripts\build.ps1 -Debug
```

### 方法 3: Python 脚本（最灵活）

适用于所有平台，提供最多的自定义选项：

```bash
# 查看帮助
python scripts/build_executable.py --help

# 基本构建
python scripts/build_executable.py

# 自动安装 PyInstaller
python scripts/build_executable.py --install-pyinstaller

# 清理后构建
python scripts/build_executable.py --clean

# 调试模式
python scripts/build_executable.py --debug

# 构建并测试
python scripts/build_executable.py --test

# 完整流程
python scripts/build_executable.py --clean --install-pyinstaller --test
```

### 方法 4: 直接使用 PyInstaller

如果需要完全自定义构建：

```bash
# 安装 PyInstaller
pip install pyinstaller

# 使用 spec 文件构建
pyinstaller get_transform.spec --clean

# 或直接构建（不推荐，配置较少）
pyinstaller --onefile --console --name get_transform Get_transform/launch.py
```

---

## 安装方法（备选）

如果不想构建可执行文件，可以使用安装脚本创建开发环境：

### Linux/macOS

```bash
# 运行安装脚本
./scripts/install.sh

# 安装完成后，使用以下方式运行
./run.sh

# 或手动运行
source .venv/bin/activate
python Get_transform/launch.py
```

### Windows

```powershell
# 运行安装脚本
.\scripts\install.ps1

# 安装完成后，双击运行
run.bat

# 或手动运行
.\.venv\Scripts\Activate.ps1
python Get_transform\launch.py
```

---

## 常见问题

### 构建问题

#### Q1: PyInstaller 安装失败

**问题**: 
```
ERROR: Could not install packages due to an OSError
```

**解决方案**:
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用管理员权限安装
sudo pip install pyinstaller  # Linux/macOS
# 或以管理员身份运行 PowerShell (Windows)

# 使用虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.\.venv\Scripts\Activate.ps1  # Windows
pip install pyinstaller
```

#### Q2: 构建速度慢

**问题**: 构建过程需要很长时间

**原因**: 
- 首次构建需要分析所有依赖
- 网络速度影响依赖下载

**解决方案**:
- 使用本地 PyPI 镜像（中国用户推荐）:
  ```bash
  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  ```
- 等待首次构建完成后，后续构建会快很多

#### Q3: 构建失败 - 缺少模块

**问题**: 
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**:
1. 检查 `get_transform.spec` 中的 `hiddenimports` 列表
2. 添加缺失的模块：
   ```python
   hiddenimports=[
       'bs4',
       'beautifulsoup4',
       'soupsieve',
       'xxx',  # 添加缺失的模块
   ],
   ```
3. 重新构建

#### Q4: Windows Defender 阻止运行

**问题**: Windows 报告可执行文件可能不安全

**原因**: PyInstaller 构建的可执行文件没有数字签名

**解决方案**:
1. 将可执行文件添加到 Windows Defender 排除列表
2. 或从"Windows 安全中心"允许运行
3. 考虑为发布版本添加代码签名

#### Q5: macOS "无法打开，因为它来自身份不明的开发者"

**问题**: macOS 阻止运行未签名的应用

**解决方案**:
```bash
# 方法 1: 临时允许
xattr -d com.apple.quarantine dist/get_transform

# 方法 2: 系统设置
# 系统偏好设置 → 安全性与隐私 → 通用 → 点击"仍要打开"
```

#### Q6: Linux "Permission denied"

**问题**: 无法执行构建的文件

**解决方案**:
```bash
chmod +x dist/get_transform
```

### 运行问题

#### Q7: 可执行文件体积过大

**问题**: 可执行文件大小超过 50MB

**原因**: 包含了 Python 解释器和所有依赖

**优化方案**:
1. 使用 UPX 压缩（已在 spec 文件中启用）:
   ```bash
   # 安装 UPX
   # Ubuntu/Debian
   sudo apt-get install upx
   
   # macOS
   brew install upx
   
   # Windows: 从 https://upx.github.io/ 下载
   ```

2. 排除不必要的模块（编辑 `get_transform.spec`）:
   ```python
   excludes=[
       'tkinter',
       'matplotlib',
       # 添加其他不需要的大型库
   ],
   ```

3. 使用 `--onedir` 模式（生成文件夹而非单文件）

#### Q8: 启动缓慢

**问题**: 可执行文件启动需要几秒钟

**原因**: 
- `--onefile` 模式需要解压到临时目录
- 首次运行时的初始化

**优化方案**:
- 使用 `--onedir` 模式（修改 spec 文件）
- 这是正常现象，后续操作会很快

#### Q9: 配置文件丢失

**问题**: 可执行文件找不到配置文件

**原因**: 配置文件路径需要特殊处理

**解决方案**:
- 程序会自动在可执行文件所在目录或用户目录创建配置
- 首次运行会引导配置

---

## 技术细节

### 构建原理

1. **PyInstaller 工作流程**:
   ```
   Python 脚本 → 分析依赖 → 收集文件 → 打包 → 生成可执行文件
   ```

2. **文件结构**:
   ```
   Get_transform/
   ├── get_transform.spec     # PyInstaller 配置
   ├── scripts/
   │   ├── build_executable.py  # 构建脚本
   │   ├── build.sh             # Shell 脚本 (Unix)
   │   ├── build.ps1            # PowerShell 脚本 (Windows)
   │   ├── install.sh           # 安装脚本 (Unix)
   │   └── install.ps1          # 安装脚本 (Windows)
   ├── dist/                    # 构建输出目录
   │   └── get_transform[.exe]  # 可执行文件
   ├── build/                   # 临时构建文件
   └── Makefile                 # Make 构建文件
   ```

3. **依赖包含**:
   - Python 解释器（嵌入式）
   - beautifulsoup4
   - soupsieve
   - 标准库模块
   - 项目代码

### Spec 文件说明

`get_transform.spec` 是 PyInstaller 的配置文件，主要配置项：

```python
# 入口点
Analysis([str(get_transform_dir / 'launch.py')])

# 数据文件
datas=[
    (str(get_transform_dir / 'requirements.txt'), 'Get_transform'),
]

# 隐藏导入（不会自动检测的模块）
hiddenimports=['bs4', 'beautifulsoup4', 'soupsieve']

# 排除的模块（减小体积）
excludes=['tkinter', 'matplotlib', 'numpy', ...]

# 可执行文件配置
EXE(
    name='get_transform',
    console=True,    # 控制台应用
    upx=True,        # 启用 UPX 压缩
)
```

### 跨平台注意事项

#### 路径分隔符
- 使用 `pathlib.Path`（已实现）
- 避免硬编码路径分隔符

#### 文件名
- 避免特殊字符（已在 `sanitize_filename` 中处理）
- 遵守各平台的文件名规则

#### 编码
- 统一使用 UTF-8（已实现）
- Windows 控制台编码已处理

### 性能优化

1. **减小体积**:
   - 排除不必要的模块
   - 启用 UPX 压缩
   - 考虑使用 `--onedir` 而非 `--onefile`

2. **加快启动**:
   - 使用 `--onedir` 模式
   - 减少导入的模块数量
   - 延迟导入大型库

3. **提高兼容性**:
   - 在目标平台上构建
   - 测试各种系统版本
   - 处理平台特定的依赖

---

## 发布检查清单

在发布新版本前，请确保：

- [ ] 在 Windows 上构建并测试
- [ ] 在 macOS 上构建并测试（Intel 和 Apple Silicon）
- [ ] 在 Linux 上构建并测试
- [ ] 测试首次运行体验
- [ ] 测试配置持久化
- [ ] 测试文件操作（复制、重命名、删除）
- [ ] 检查日志输出
- [ ] 验证错误处理
- [ ] 更新版本号
- [ ] 更新 CHANGELOG
- [ ] 创建 GitHub Release
- [ ] 上传各平台的可执行文件

---

## 获取帮助

如果遇到构建问题：

1. **查看日志**: 构建过程的详细日志在 `build/` 目录
2. **检查文档**: 仔细阅读本文档和 README.md
3. **搜索问题**: 在 GitHub Issues 中搜索类似问题
4. **提交 Issue**: 附上完整的错误信息和系统信息
5. **联系支持**: yorickhui@gmail.com

---

## 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/)
- [Python 打包指南](https://packaging.python.org/)
- [跨平台开发最佳实践](https://docs.python.org/3/library/pathlib.html)

---

**最后更新**: 2025-01-27  
**维护者**: AI Assistant / Yorick
