# 📦 Get_transform 打包分发方案

## 概述

本项目实现了完整的打包分发系统，使非技术用户可以无需安装 Python 环境即可使用 Get_transform。

## 方案选择

### 评估结果

我们评估了以下打包方案：

| 方案 | 优点 | 缺点 | 评分 |
|------|------|------|------|
| **PyInstaller** ✅ | • 跨平台<br>• 成熟稳定<br>• 单文件模式<br>• 广泛使用 | • 文件较大<br>• 启动稍慢 | ⭐⭐⭐⭐⭐ |
| shiv | • 文件小<br>• 启动快 | • 需要 Python<br>• 跨平台有限 | ⭐⭐⭐ |
| zipapp | • 简单轻量 | • 需要 Python<br>• 功能有限 | ⭐⭐ |

### 最终选择：PyInstaller

**原因**:
1. **完全独立**: 不需要用户安装 Python
2. **跨平台**: Windows、macOS、Linux 全支持
3. **成熟稳定**: 大量项目使用，问题少
4. **单文件模式**: 便于分发和使用
5. **依赖打包**: 自动处理所有依赖

## 实现内容

### 1. 核心文件

#### `get_transform.spec`
PyInstaller 配置文件，定义构建参数：

```python
# 入口点
Analysis([str(get_transform_dir / 'launch.py')])

# 数据文件
datas=[
    (str(get_transform_dir / 'requirements.txt'), 'Get_transform'),
]

# 隐藏导入
hiddenimports=['bs4', 'beautifulsoup4', 'soupsieve']

# 可执行文件配置
EXE(
    name='get_transform',
    console=True,
    upx=True,
)
```

**特点**:
- 使用 `launch.py` 作为入口点（包含依赖检查和初始化）
- 自动包含 beautifulsoup4 和相关依赖
- 启用 UPX 压缩（减小文件大小）
- 控制台模式（适合 CLI 应用）
- 排除不必要的大型库（tkinter, matplotlib 等）

### 2. 构建脚本

#### `scripts/build_executable.py`
Python 构建脚本，提供以下功能：

**主要特性**:
- 自动检查 PyInstaller 是否已安装
- 提供交互式安装选项
- 清理构建目录
- 调试模式支持
- 构建后测试
- 详细的进度显示和错误提示

**命令行选项**:
```bash
python scripts/build_executable.py --help
  --clean               # 清理构建目录
  --debug               # 启用调试模式
  --test                # 构建后测试
  --install-pyinstaller # 自动安装 PyInstaller
```

#### `scripts/build.sh` (Linux/macOS)
Shell 构建脚本：

```bash
./scripts/build.sh [选项]
  --clean       # 清理构建目录
  --debug       # 启用调试模式
  --test        # 构建后测试
  --install-deps # 安装依赖包
```

**特点**:
- 彩色输出（提高可读性）
- 错误处理（set -e）
- 自动检查 Python 版本
- 显示文件大小

#### `scripts/build.ps1` (Windows)
PowerShell 构建脚本：

```powershell
.\scripts\build.ps1 [选项]
  -Clean        # 清理构建目录
  -Debug        # 启用调试模式
  -Test         # 构建后测试
  -InstallDeps  # 安装依赖包
```

**特点**:
- 彩色输出（PowerShell）
- 参数化（PowerShell 风格）
- 友好的错误提示

### 3. Makefile

提供便捷的构建命令：

```makefile
make build        # 构建可执行文件
make build-debug  # 构建调试版本
make clean        # 清理构建文件
make test         # 运行测试
make dist         # 构建并打包发布
make help         # 显示帮助
```

**优点**:
- 一键构建
- 标准化的开发流程
- 易于集成 CI/CD

### 4. 安装脚本（备选方案）

对于不想或无法使用可执行文件的用户，提供安装脚本：

#### `scripts/install.sh` (Linux/macOS)
```bash
./scripts/install.sh
```

**功能**:
- 创建虚拟环境
- 安装依赖
- 生成启动脚本 `run.sh`

#### `scripts/install.ps1` (Windows)
```powershell
.\scripts\install.ps1
```

**功能**:
- 创建虚拟环境
- 安装依赖
- 生成启动脚本 `run.bat`

### 5. 发布准备脚本

#### `scripts/prepare_release.sh`
自动化发布流程：

```bash
./scripts/prepare_release.sh
```

**功能**:
- 检查 Git 状态
- 询问版本号
- 运行测试
- 构建可执行文件
- 创建发布目录
- 生成 SHA256 校验和
- 更新 CHANGELOG
- 生成发布说明
- 创建 Git 标签
- 推送到远程仓库

## 构建流程

### 开发者构建流程

```bash
# 1. 克隆仓库
git clone https://github.com/yorickhui/Get_transform.git
cd Get_transform

# 2. 构建可执行文件
make build
# 或
./scripts/build.sh --install-deps
# 或
python3 scripts/build_executable.py --install-pyinstaller

# 3. 测试可执行文件
./dist/get_transform

# 4. 发布（可选）
./scripts/prepare_release.sh
```

### 最终用户使用流程

```bash
# 1. 下载可执行文件
# 从 GitHub Releases 下载

# 2. 运行（Linux/macOS）
chmod +x get_transform
./get_transform

# 2. 运行（Windows）
# 双击 get_transform.exe
```

## 构建输出

### 文件大小

预期可执行文件大小：
- **Linux**: ~15-25 MB
- **macOS**: ~15-25 MB
- **Windows**: ~15-25 MB

**大小说明**:
- 包含 Python 解释器（~10 MB）
- 包含 beautifulsoup4 和依赖（~2 MB）
- 包含项目代码（~1 MB）
- UPX 压缩后体积（~40-50% 压缩率）

### 目录结构

```
dist/
├── get_transform           # Linux/macOS 可执行文件
└── get_transform.exe       # Windows 可执行文件

build/
└── get_transform/          # 临时构建文件
```

## 跨平台支持

### 平台差异处理

1. **路径处理**: 使用 `pathlib.Path`（已实现）
2. **文件名**: `sanitize_filename` 函数处理平台差异（已实现）
3. **编码**: 统一使用 UTF-8（已实现）
4. **可执行文件扩展名**: 
   - Windows: `.exe`
   - Linux/macOS: 无扩展名

### 构建平台要求

**重要**: 必须在目标平台上构建可执行文件
- Windows 可执行文件必须在 Windows 上构建
- macOS 可执行文件必须在 macOS 上构建
- Linux 可执行文件必须在 Linux 上构建

**原因**: PyInstaller 打包的是平台特定的二进制文件，不能跨平台使用。

## 依赖管理

### 自动包含的依赖

```python
hiddenimports=[
    'bs4',                 # BeautifulSoup4
    'beautifulsoup4',      # BeautifulSoup4 主模块
    'soupsieve',           # CSS 选择器（BS4 依赖）
    'html.parser',         # HTML 解析器
    'pathlib',             # 路径处理
]
```

### 排除的模块（减小体积）

```python
excludes=[
    'tkinter',      # GUI 框架
    'matplotlib',   # 绘图库
    'numpy',        # 数值计算
    'pandas',       # 数据分析
    'PIL',          # 图像处理
    'PyQt5',        # GUI 框架
    'PyQt6',        # GUI 框架
    'PySide2',      # GUI 框架
    'PySide6',      # GUI 框架
    'wx',           # GUI 框架
]
```

## 优化建议

### 减小文件大小

1. **UPX 压缩**（已启用）:
   ```bash
   # 安装 UPX
   # Ubuntu/Debian
   sudo apt-get install upx
   
   # macOS
   brew install upx
   
   # Windows
   # 从 https://upx.github.io/ 下载
   ```

2. **排除不必要的模块**:
   - 编辑 `get_transform.spec` 中的 `excludes` 列表
   - 添加不需要的大型库

3. **使用 `--onedir` 模式**:
   - 文件夹模式，不需要每次解压
   - 启动更快，但分发不便

### 提高启动速度

1. **使用 `--onedir` 模式**（推荐用于本地使用）
2. **减少导入**: 延迟导入大型模块
3. **预编译**: PyInstaller 已自动预编译

### 提高兼容性

1. **在目标平台构建**: 确保兼容性
2. **测试多个系统版本**: 旧版本系统的兼容性
3. **静态链接**: PyInstaller 默认静态链接

## 测试策略

### 构建测试

```bash
# 1. 构建
make build

# 2. 基本测试
./dist/get_transform --help

# 3. 功能测试
# 手动运行程序，测试各项功能
```

### 平台测试清单

- [ ] **Windows 10**: 测试运行
- [ ] **Windows 11**: 测试运行
- [ ] **macOS 10.15+**: 测试运行（Intel）
- [ ] **macOS 11+**: 测试运行（Apple Silicon）
- [ ] **Ubuntu 20.04**: 测试运行
- [ ] **Ubuntu 22.04**: 测试运行
- [ ] **Debian 11**: 测试运行
- [ ] **CentOS 7**: 测试运行

### 功能测试清单

- [ ] 首次运行配置向导
- [ ] 目录创建
- [ ] 配置持久化
- [ ] 文件操作（复制、重命名、删除）
- [ ] 日志记录
- [ ] 错误处理
- [ ] 中文字符支持
- [ ] 路径包含空格

## 分发方式

### 1. GitHub Releases（推荐）

**优点**:
- 免费托管
- 版本管理
- 下载统计
- Release notes

**发布流程**:
1. 在所有平台上构建
2. 生成 SHA256 校验和
3. 创建 GitHub Release
4. 上传文件并添加说明

### 2. 直接分发

**适用场景**:
- 企业内部使用
- 小规模分发
- 测试版本

**方式**:
- 压缩包（ZIP/tar.gz）
- 网盘分享
- 局域网文件服务器

### 3. 包管理器（未来）

**可能的方案**:
- **Windows**: Chocolatey, Scoop
- **macOS**: Homebrew
- **Linux**: APT, YUM, Snap, Flatpak

## 常见问题

### Q: 可执行文件太大？
**A**: 这是正常的，因为包含了 Python 解释器。可以：
1. 启用 UPX 压缩（已启用）
2. 排除不必要的模块
3. 使用 `--onedir` 模式

### Q: 启动很慢？
**A**: `--onefile` 模式需要解压到临时目录。可以：
1. 使用 `--onedir` 模式（更快但分发不便）
2. 这是正常现象，后续操作会很快

### Q: 杀毒软件报警？
**A**: PyInstaller 打包的文件没有数字签名，可能被误报。解决：
1. 添加到杀毒软件白名单
2. 为发布版本添加代码签名

### Q: 能否跨平台使用？
**A**: 不能。必须在目标平台上构建。

### Q: 如何减小依赖？
**A**: 
1. 检查 `hiddenimports` 列表
2. 移除不必要的导入
3. 使用 `excludes` 排除大型库

## 未来改进

### 短期（v1.1）

- [ ] 添加版本信息到可执行文件
- [ ] 优化文件大小（目标 <20 MB）
- [ ] 添加自动更新检查
- [ ] 生成安装包（.msi, .dmg, .deb）

### 中期（v1.2）

- [ ] CI/CD 自动构建（GitHub Actions）
- [ ] 代码签名（Windows/macOS）
- [ ] 多语言支持
- [ ] GUI 界面（可选）

### 长期（v2.0）

- [ ] 包管理器分发
- [ ] 自动更新功能
- [ ] 插件系统
- [ ] Web 界面（可选）

## 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/)
- [Python 打包指南](https://packaging.python.org/)
- [跨平台开发最佳实践](https://docs.python.org/3/library/pathlib.html)

---

**文档维护**: Yorick (yorickhui@gmail.com)  
**最后更新**: 2025-01-27
