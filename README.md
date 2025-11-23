# 🌀 Get_transform

![GitHub stars](https://img.shields.io/github/stars/yorickhui/Get_transform?style=for-the-badge&color=blue)
![GitHub forks](https://img.shields.io/github/forks/yorickhui/Get_transform?style=for-the-badge&color=green)
![GitHub issues](https://img.shields.io/github/issues/yorickhui/Get_transform?style=for-the-badge&color=orange)
![GitHub last commit](https://img.shields.io/github/last-commit/yorickhui/Get_transform?style=for-the-badge&color=purple)
![GitHub license](https://img.shields.io/github/license/yorickhui/Get_transform?style=for-the-badge&color=brightgreen)

<p align="center">
  <img src="/banner.png" width="600" alt="Get_transform banner">
</p>

# Get_transform
这是一款 Get 笔记导出文件处理工具，自动帮你从乱码命名的 HTML 导出中提取标题、删除重复内容，并输出可以直接导入 Notion/Obsidian 等应用的整洁文件。

> **一句话简介：** 导出 → 向导式初始化 → 智能清理 → 一键导入其他笔记平台。

---

## 目录
1. [核心功能](#核心功能)
2. [使用工作流](#使用工作流)
3. [首次运行向导](#首次运行向导)
4. [三种使用方式](#三种使用方式)
5. [交互菜单与工作模式](#交互菜单与工作模式)
6. [配置与自定义 (.get_transform_config.json)](#配置与自定义-get_transform_configjson)
7. [跨平台使用说明](#跨平台使用说明)
8. [打包 / 安装 / 构建](#打包--安装--构建)
9. [故障排查 FAQ](#故障排查-faq)
10. [文档索引](#文档索引)
11. [版本信息 & 支持](#版本信息--支持)

---

## 核心功能
- **智能时间戳识别**：自动解析 `voicenotes_YYYYMMDDHHMM_...` 文件夹，按时间排序版本。
- **重复文件检测**：比较最新导出与历史版本，精准定位重复 HTML。
- **安全操作模式**：试运行、正式运行、仅复制重命名三种模式，支持备份与日志。
- **自动依赖管理**：`launch.py` 会自动检测 Python/pip，提示或安装 `beautifulsoup4` 等依赖。
- **目录初始化向导**：首次运行自动创建 `history/`, `new/`, `logs/`，并验证自定义路径。
- **配置持久化**：`.get_transform_config.json` 保存所有路径及默认模式，可随时修改。
- **跨平台兼容**：使用 `pathlib`、UTF-8、文件名消毒算法，完整支持 Windows/macOS/Linux。
- **PyInstaller 打包**：官方提供单文件可执行程序以及 Makefile/脚本，方便自定义构建与发布。

---

## 使用工作流
```
┌─────────────────────────────────────────────────────────────┐
│ 1. 从 GET 笔记导出 HTML 并解压                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. 运行 Get_transform（可执行文件或 launch.py）               │
│    ├─ 自动检查 Python / pip                                   │
│    ├─ 自动安装 beautifulsoup4                                 │
│    └─ 初始化 history/new/logs 目录并保存配置                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. 将解压后的导出文件夹放入 history/                         │
│    示例：history/voicenotes_202511200930_getnotes_archive_xx │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. 选择运行模式                                             │
│    [1] 试运行 → 仅预览                                       │
│    [2] 正式运行 → 删除重复 + 复制新笔记                      │
│    [3] 仅复制重命名 → 最安全                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. 在 new/ 中获取已重命名的 HTML，直接导入其他应用           │
└─────────────────────────────────────────────────────────────┘
```

---

## 首次运行向导
1. **下载或克隆项目**
   - 非技术用户：从 [Releases](https://github.com/yorickhui/Get_transform/releases) 下载对应平台的可执行文件。
   - 开发者：`git clone https://github.com/yorickhui/Get_transform.git && cd Get_transform`。

2. **执行启动脚本/可执行文件**
   ```bash
   # Linux/macOS
   python Get_transform/launch.py

   # Windows
   py Get_transform\launch.py
   ```
   或在图形界面直接双击 `get_transform.exe`。

3. **自动依赖安装**
   - 检查 Python ≥ 3.6、pip 可用性。
   - 从 `Get_transform/requirements.txt` 读取依赖，并询问是否自动安装。
   - 失败时提供明确的手动安装命令和重试机制。

4. **目录初始化**
   - 自动创建脚本同级的 `history/`, `new/`, `logs/`。
   - 支持自定义 GET 导出存放位置并实时校验。

5. **配置向导**
   - 成功初始化后将设置写入 `.get_transform_config.json`。
   - 再次运行时会显示当前配置，并询问是否继续沿用。

6. **环境变量传递**
   - `GET_HISTORY_PATH / GET_NEW_PATH / GET_LOGS_PATH` 会传递到主程序，确保目录一致。

> **提示**：任何时候都可以删除配置文件重新执行向导，或通过 `launch.py --force`（后续计划）重新初始化。

---

## 三种使用方式

### 方式一：独立可执行文件（推荐）
**面向非技术用户，无需安装 Python。**

1. 前往 [Releases](https://github.com/yorickhui/Get_transform/releases) 下载：

| 平台 | 文件名 | 运行方式 |
|------|--------|----------|
| Windows 10/11 | `get_transform.exe` | 双击或 `PowerShell> .\get_transform.exe` |
| macOS 10.15+ | `get_transform_macos` | `chmod +x get_transform_macos && ./get_transform_macos` |
| Linux (Ubuntu/Debian/Fedora 等) | `get_transform_linux` | `chmod +x get_transform_linux && ./get_transform_linux` |

2. 首次运行即进入依赖检查和目录向导。
3. 将导出的文件夹复制到可执行文件旁的 `history/`，按菜单提示操作即可。

> **安全提示**：首次执行时若被 Windows Defender 或 macOS Gatekeeper 阻拦，请参见 [故障排查](#故障排查-faq)。

### 方式二：Python + 安装脚本（推荐给动手用户）
**脚本会自动创建虚拟环境、安装依赖并生成启动脚本。**

**Linux/macOS**
```bash
./scripts/install.sh   # 自动创建 .venv 并安装依赖
./run.sh               # 进入虚拟环境并执行 launch.py
```

**Windows**
```powershell
.\scripts\install.ps1  # 自动创建虚拟环境并安装依赖
.\run.bat              # 双击或在 PowerShell 中运行
```

> 也可直接运行 `python Get_transform/launch.py`（需手动安装依赖）。

### 方式三：源码构建与开发
**适合需要自定义或参与开发的用户。**

- **Makefile（Linux/macOS）**
  ```bash
  make help          # 查看所有命令
  make build         # 构建 PyInstaller 可执行文件
  make clean         # 清理 build/dist
  make test          # 运行测试（包括 cross-platform suite）
  make dist          # 构建 + 打包发布
  ```

- **Shell/PowerShell 脚本**
  ```bash
  ./scripts/build.sh --install-deps --test
  # 或
  .\scripts\build.ps1 -InstallDeps -Test
  ```

- **Python 构建脚本**
  ```bash
  python scripts/build_executable.py --clean --install-pyinstaller --test
  ```

- **手动运行**
  ```bash
  python Get_transform/duplicate_file_cleaner.py
  ```

详见 [BUILD.md](BUILD.md) 与 [PACKAGING.md](PACKAGING.md)。

---

## 交互菜单与工作模式
```text
🌀 Get_transform 主菜单
========================================
1. 试运行        ── 不删除文件，仅打印将执行的操作
2. 正式运行      ── 删除重复笔记 + 复制重命名
3. 仅复制重命名  ── 不触碰历史版本，最安全
4. 退出

> 日志: logs/file_cleaner_20251123_101530.log
> 默认模式: 可在配置中指定 default_mode
```

- **试运行**：推荐在每次导入新导出后先执行，确认将要删除的文件。
- **正式运行**：删除最新导出中的重复文件，保留唯一内容，并将所有新文件复制到 `new/`。
- **仅复制重命名**：跳过删除逻辑，适合只想重命名的场景或首次使用。
- **备份/跳过重复**：程序会在关键节点提供确认提示并写入日志。

---

## 配置与自定义 (.get_transform_config.json)
- **位置**：默认存放在 `Get_transform/.get_transform_config.json`。
- **自动生成**：首次运行 `launch.py` 或可执行文件时创建。

### 示例配置
```json
{
  "version": "1.0",
  "history_dir": "/Users/you/Get_transform/history",
  "new_dir": "/Users/you/Get_transform/new",
  "logs_dir": "/Users/you/Get_transform/logs",
  "default_mode": "copy_only"
}
```

| 字段 | 含义 | 允许值/示例 |
|------|------|-------------|
| `version` | 配置版本，会自动升级 | `"1.0"` |
| `history_dir` | GET 导出目录 | 绝对路径，需可读 |
| `new_dir` | 输出目录 | 默认与脚本同级 `new/` |
| `logs_dir` | 日志目录 | 默认 `logs/` |
| `default_mode` | 启动后默认选项 | `trial`, `run`, `copy_only` |

### 修改方式
1. **通过向导**：删除配置文件或在启动时选择“重新配置”。
2. **手动编辑**：直接修改 JSON，保存后重新运行即可。
3. **环境变量覆盖**：运行前设置 `GET_HISTORY_PATH` 等变量，可用于 CI/自定义脚本。

### 最佳实践
- 将 `history/` 设置在大容量磁盘，长期保留最近 2 次导出以便判重。
- `logs/` 可指向 Dropbox/OneDrive，同步留痕更容易回溯。
- 若需要多人共享，可将配置文件和 `history` 指向共享网络盘。

---

## 跨平台使用说明
### 已验证平台
| 平台 | 版本范围 | 备注 |
|------|----------|------|
| Windows | 10 / 11 (x64) | 支持长路径、Unicode，建议启用 UTF-8 Beta 功能 |
| macOS | 10.15+ (Intel & Apple Silicon) | 需授予终端完整磁盘访问权限 |
| Linux | Ubuntu 20.04+, Debian 10+, CentOS 7+, Arch, Fedora | 任何 UTF-8 locale 的主流发行版 |

### 平台差异与命令
- **Windows**
  - 运行：`get_transform.exe` 或 `py Get_transform\launch.py`
  - 建议通过 PowerShell 以管理员身份安装依赖。
  - 启用长路径：`gpedit.msc > 计算机配置 > 管理模板 > 系统 > 文件系统 > 启用 Win32 长路径`。

- **macOS**
  - 首次运行可执行文件前：`chmod +x get_transform_macos`。
  - 若提示“无法验证开发者”：系统设置 → 隐私与安全性 → 仍要打开。
  - 终端需拥有“完全磁盘访问”以读取下载目录。

- **Linux**
  - 确保 locale：`export LANG=en_US.UTF-8`。
  - 若提示 `Permission denied`：`chmod +x dist/get_transform`。
  - SELinux/ AppArmor 环境请允许运行自建可执行文件。

### 文件名与路径策略
- `sanitize_filename` 自动处理 Windows 保留名（CON/PRN/AUX/NUL/COM1-9/LPT1-9）、非法字符和尾部空格。
- 最长文件名限制 200 字节，保证在 UTF-8 下不截断字符。
- Windows 路径总长自动留白 60+ 字节，避免 260 字符限制。

---

## 打包 / 安装 / 构建
- **PyInstaller 单文件方案**：配置见 `get_transform.spec`，默认启用 UPX，支持 `--onefile`。
- **脚本与自动化**：
  - `scripts/build_executable.py`：Python 构建入口，支持 `--clean --debug --test --install-pyinstaller`。
  - `scripts/build.sh` / `scripts/build.ps1`：跨平台彩色输出脚本。
  - `scripts/install.sh` / `scripts/install.ps1`：创建虚拟环境 + 启动脚本。
  - `scripts/prepare_release.sh`：半自动发布流程（构建、测试、校验和、CHANGELOG 更新）。
- **Makefile**：`make build`, `make clean`, `make test`, `make dist` 等命令覆盖完整开发周期。
- **测试**：`python Get_transform/test_cross_platform.py` 验证文件名清理、平台工具。
- **文档**：
  - [BUILD.md](BUILD.md)：系统要求、四种构建方法、常见问题（>9 个场景）。
  - [PACKAGING.md](PACKAGING.md)：为何选择 PyInstaller、性能指标、未来改进。
  - [QUICKSTART.md](QUICKSTART.md)：面向非技术用户的下载、首次运行、FAQ 与技巧。

---

## 故障排查 FAQ
1. **Python 版本过低**
   - **症状**：启动脚本提示 “Python版本过低”。
   - **解决**：安装 Python 3.8+ 并勾选 “Add Python to PATH”，重新运行 `launch.py`。

2. **找不到 pip**
   - **症状**：启动脚本提示 “pip 不可用”。
   - **解决**：重新安装 Python 或运行 `python -m ensurepip --upgrade`，之后再次执行。

3. **依赖安装失败**
   - **症状**：`beautifulsoup4` 安装错误。
   - **解决**：手动运行 `python -m pip install -r Get_transform/requirements.txt`，或切换到管理员/ sudo 权限，并考虑更换为清华/阿里云镜像。

4. **无法创建 history/new/logs**
   - **症状**：初始化阶段出现权限错误。
   - **解决**：确保目录位于当前用户可写位置（如 `~/Get_transform`），必要时 `sudo chown -R $USER`。

5. **history 路径验证失败**
   - **症状**：输入自定义路径后提示“不存在/无法读取”。
   - **解决**：确认路径真实存在且包含导出的 `notes/` 与 `index.html`，或直接使用默认路径。

6. **index.html 丢失或被修改**
   - **症状**：重命名阶段日志提示 “未找到文件标题映射”。
   - **解决**：确保导出的目录完整无缺，并不要移动 `index.html`；必要时重新导出。

7. **文件名冲突或路径过长**
   - **症状**：复制阶段日志中出现 “文件名截断/冲突”。
   - **解决**：程序会自动追加 `_1/_2` 后缀；若仍失败，请将项目放在路径较短的位置（如 `C:\Get_transform`）。

8. **配置文件损坏**
   - **症状**：启动时提示 “配置文件结构无效”。
   - **解决**：系统会自动备份 `*.bak` 并生成默认配置；也可手动删除 `.get_transform_config.json` 重新运行。

9. **Windows Defender 阻止 exe**
   - **症状**：下载的可执行文件被标记为未知应用。
   - **解决**：点击 “更多信息 → 仍要运行”，或将文件所在目录加入白名单；发布版暂未签名，属正常现象。

10. **macOS “无法打开，因为来自未识别开发者”**
    - **解决**：在终端执行 `xattr -d com.apple.quarantine ./get_transform_macos` 或在系统设置中允许运行。

11. **Linux 权限不足**
    - **症状**：`Permission denied`。
    - **解决**：`chmod +x get_transform_linux` 或 `sudo chown -R $USER:$USER .` 并确认当前用户对 history/new 目录有写权限。

12. **日志或输出目录在网络盘上不可写**
    - **解决**：将 `logs_dir`/`new_dir` 指向本地磁盘，或在网络盘上授予写权限；可以通过配置文件/环境变量重定向。

> 更多常见问题与解决方案请查看 [BUILD.md](BUILD.md) 与 [QUICKSTART.md](QUICKSTART.md)。

---

## 文档索引
- [README](README.md)：项目概述（当前页面）。
- [QUICKSTART.md](QUICKSTART.md)：面向非技术用户的详细图文指南。
- [BUILD.md](BUILD.md)：构建/打包/安装的深度说明与常见问题。
- [PACKAGING.md](PACKAGING.md)：PyInstaller 方案、优化、未来计划。
- [CHANGELOG.md](CHANGELOG.md)：版本历史与升级指引。
- [CROSS_PLATFORM_CHANGES.md](CROSS_PLATFORM_CHANGES.md)：跨平台实现细节（开发者参考）。

---

## 版本信息 & 支持
- **当前版本**：1.1.0（详见 [CHANGELOG](CHANGELOG.md)）
- **许可证**：MIT
- **作者**：Yorick (yorickhui@gmail.com)
- **反馈渠道**：
  - [GitHub Issues](https://github.com/yorickhui/Get_transform/issues)
  - Email：yorickhui@gmail.com

如果这个工具对你有帮助，欢迎 ⭐Star、Fork、分享给朋友，也可以提交 PR 一起改进！
