# 🌀 Get_transform

![GitHub stars](https://img.shields.io/github/stars/yorickhui/Get_transform?style=for-the-badge&color=blue)
![GitHub forks](https://img.shields.io/github/forks/yorickhui/Get_transform?style=for-the-badge&color=green)
![GitHub issues](https://img.shields.io/github/issues/yorickhui/Get_transform?style=for-the-badge&color=orange)
![GitHub last commit](https://img.shields.io/github/last-commit/yorickhui/Get_transform?style=for-the-badge&color=purple)
![GitHub license](https://img.shields.io/github/license/yorickhui/Get_transform?style=for-the-badge&color=brightgreen)

<p align="center">
  <img src="/banner.png" width="600">
</p>

# Get_transform
这是一款Get笔记导出文件处理脚本，让导出的Get笔记命名不再是乱码，方便导入其他笔记软件

# 功能概述
GET笔记是一款优秀的国产AI笔记软件，在移动端收集小红书、抖音内容作为笔记体验非常优秀，但是他的导出功能比较弱，导出的为一串字符命名的html无法直接导入Notion等其他笔记。
为了方便自己同时使用GET和Notion笔记，方便在二者之间同步。我编写了这个脚本，有相同需求的同学可以复制使用


## 功能特性

- **智能时间戳识别**: 自动解析文件夹名中的时间戳格式 (YYYYMMDDHHMM)
- **版本排序**: 按时间戳自动排序，识别最新和历史版本
- **重复文件检测**: 精确识别最新文件夹中与历史版本重复的文件
- **安全删除机制**: 提供试运行、备份、确认等多重安全保障
- **智能文件复制重命名**: 解析index.html中的标题映射，将HTML文件复制到指定目录并重命名为有意义的标题


## 使用方法

### 方式一：直接运行可执行文件（推荐，无需安装 Python）

**适用于非技术用户，开箱即用！**

1. **下载预构建的可执行文件**
   - 前往 [Releases](https://github.com/yorickhui/Get_transform/releases) 页面
   - 根据你的操作系统下载对应的文件：
     - Windows: `get_transform.exe`
     - macOS: `get_transform` (macOS)
     - Linux: `get_transform` (Linux)

2. **准备笔记文件**
   - 从 GET笔记 导出笔记（导出为 HTML 格式）
   - 解压导出的文件包

3. **运行程序**
   - **Windows**: 双击 `get_transform.exe` 运行
   - **macOS/Linux**: 在终端中运行 `./get_transform`
   
4. **首次运行配置**
   - 程序会引导你配置导出路径
   - 按照提示完成设置即可

5. **开始使用**
   - 将导出的笔记文件夹放入 `history/` 目录
   - 运行程序，选择操作模式
   - 处理后的文件会保存在 `new/` 目录

> **提示**: 
> - 可执行文件包含所有依赖，无需安装 Python
> - 首次运行会自动创建必要的目录
> - 配置会自动保存，下次运行无需重新配置

### 方式二：使用 Python 运行（开发者）

**适用于技术用户和开发者**

#### 快速安装

**Linux/macOS:**
```bash
# 克隆仓库
git clone https://github.com/yorickhui/Get_transform.git
cd Get_transform

# 运行安装脚本
./scripts/install.sh

# 启动程序
./run.sh
```

**Windows:**
```powershell
# 克隆仓库
git clone https://github.com/yorickhui/Get_transform.git
cd Get_transform

# 运行安装脚本
.\scripts\install.ps1

# 启动程序（双击或在 PowerShell 中运行）
.\run.bat
```

#### 手动安装

**步骤1：准备工作**
- 安装 Python 3.6+: https://www.python.org/
- 克隆或下载本项目到你的电脑

**步骤2：进入项目目录**
```bash
cd /path/to/Get_transform
```

**步骤3：安装依赖**
```bash
# 使用 pip 安装
pip install -r Get_transform/requirements.txt
```

**步骤4：运行程序**
```bash
# 推荐：使用启动脚本（会自动检查依赖）
python Get_transform/launch.py

# 或直接运行主程序
python Get_transform/duplicate_file_cleaner.py
```

### 方式三：构建你自己的可执行文件

**适用于想要自己构建的用户**

详细的构建说明请参阅 [BUILD.md](BUILD.md)。

**快速构建:**

```bash
# Linux/macOS
make build

# 或使用脚本
./scripts/build.sh --install-deps

# Windows
.\scripts\build.ps1 -InstallDeps
```

构建完成后，可执行文件位于 `dist/` 目录。

### 2. 操作选项

运行后会显示菜单：

```
请选择操作:
1. 试运行 (查看将要删除的文件，不实际删除)
2. 正式运行 (实际删除重复文件)
3. 仅复制重命名 (不删除重复文件，仅将最新文件夹中的HTML文件复制到new目录并重命名)
4. 退出
```

### 3. 推荐流程

1. **先运行试运行模式**：选择选项 `1`，查看将要删除的文件列表
2. **确认无误后正式运行**：选择选项 `2`，执行实际删除操作
3. **仅需复制**：如果只想复制重命名文件而不删除重复文件，选择选项 `3`
4. **选择是否备份**：正式运行时可选择是否创建备份

### 文件复制重命名功能
- **自动解析**: 读取最新文件夹中的index.html，提取笔记标题与文件名的映射关系
- **智能重命名**: 将HTML文件从哈希文件名重命名为有意义的标题
- **目标目录**: 复制到脚本所在目录下的 `new` 文件夹
- **文件名清理**: 自动处理特殊字符，确保文件名符合Windows文件系统要求

#### 示例
原文件: `9323c2f00816d6a7cfffabb9b8ea1ad5.html`
重命名为: `太变态！这个AI工具从写代码到发推啥都能干.html`


## 工作原理

1. **时间戳识别**：从文件夹名称中提取时间戳（格式：`voicenotes_YYYYMMDDHHMM_...`）
2. **版本排序**：按时间戳对文件夹进行排序，识别最新和旧版本
3. **文件对比**：比较各版本 `notes/` 目录下的文件名
4. **重复删除**：删除最新版本中与任何旧版本重复的文件

## 技术细节

- **语言**：Python 3.6+
- **依赖**：beautifulsoup4（启动脚本会自动安装）
- **兼容性**：Windows/Linux/macOS
- **编码**：UTF-8，支持中文路径和文件名
- **启动方式**：
  - 推荐：`python Get_transform/launch.py`（自动检查环境和依赖）
  - 直接：`python Get_transform/duplicate_file_cleaner.py`（需手动安装依赖）
- **打包工具**：PyInstaller（用于构建独立可执行文件）

## 打包与分发

### 为非技术用户提供可执行文件

本项目使用 PyInstaller 支持将 Python 代码打包成独立的可执行文件，无需安装 Python 环境即可运行。

### 构建可执行文件

#### 快速构建

**Linux/macOS:**
```bash
# 使用 Makefile（最简单）
make build

# 或使用构建脚本
./scripts/build.sh --install-deps

# 或使用 Python 脚本
python3 scripts/build_executable.py --install-pyinstaller
```

**Windows:**
```powershell
# 使用 PowerShell 脚本（推荐）
.\scripts\build.ps1 -InstallDeps

# 或使用 Python 脚本
python scripts\build_executable.py --install-pyinstaller
```

#### 构建输出

构建成功后，可执行文件将位于 `dist/` 目录：
- **Windows**: `dist/get_transform.exe`
- **macOS/Linux**: `dist/get_transform`

可执行文件包含：
- Python 解释器（嵌入式）
- 所有依赖包（beautifulsoup4 等）
- 项目代码

用户只需运行这个文件即可，无需安装任何其他软件。

#### 详细构建文档

完整的构建说明、系统要求、常见问题等，请参阅 [BUILD.md](BUILD.md)。

### 构建选项

```bash
# 清理后构建
make clean && make build

# 构建调试版本（包含更多调试信息）
make build-debug

# 构建并测试
python3 scripts/build_executable.py --test

# 查看所有可用命令
make help
```

### 分发建议

1. **版本标记**: 在 GitHub Releases 中为每个版本创建标签
2. **多平台构建**: 分别在 Windows、macOS、Linux 上构建并上传
3. **命名规范**: 
   - `get_transform-v1.0-windows.exe`
   - `get_transform-v1.0-macos`
   - `get_transform-v1.0-linux`
4. **校验和**: 提供 SHA256 校验和文件
5. **使用说明**: 在 Release 说明中包含快速开始指南

## 跨平台兼容性

本工具已针对 Windows、macOS 和 Linux 平台进行全面优化，确保在不同操作系统上行为一致。

### 已验证平台

- ✅ **Windows 10/11**: 完整支持，包括长路径和 Unicode 文件名
- ✅ **macOS 10.15+**: 完整支持，包括 APFS 文件系统
- ✅ **Linux**: 完整支持各主流发行版（Ubuntu、Debian、CentOS 等）

### 跨平台特性

#### 1. 路径处理
- 统一使用 `pathlib.Path` 进行路径操作，自动适配不同系统的路径分隔符
- 支持用户目录扩展（`~`）和相对路径自动转换
- 正确处理 Windows UNC 路径和长路径（超过 260 字符）

#### 2. 文件名安全处理
- **Windows 保留名**: 自动处理 CON、PRN、AUX、NUL、COM1-9、LPT1-9 等保留设备名
- **非法字符过滤**: 移除或替换 `< > : " / \ | ? *` 和控制字符
- **尾部字符处理**: 自动移除 Windows 不支持的尾部空格和点号
- **路径长度限制**: 
  - Windows: 自动截断超过 260 字符的路径
  - macOS/Linux: 支持最长 4096 字符的路径
- **文件名长度**: 智能截断超长文件名（默认限制 200 字节，保留 UTF-8 完整性）

#### 3. 字符编码支持
- **UTF-8 编码**: 所有文件读写操作统一使用 UTF-8 编码
- **非 ASCII 字符**: 完整支持中文、日文、韩文、俄文等各种 Unicode 字符
- **字节安全截断**: 截断超长文件名时确保不破坏多字节 UTF-8 字符
- **Windows 编码**: 正确处理 Windows 控制台的 GBK/UTF-16LE 编码问题

#### 4. 权限和错误处理
- 自动检测和提示文件/目录权限问题
- 跨平台权限测试（读/写/执行权限）
- 友好的错误提示和修复建议

### 常见问题排查

#### Windows 平台

**问题：路径包含中文时出错**
- 解决：确保 Windows 系统区域设置支持 Unicode（控制面板 → 区域 → 管理 → 更改系统区域设置 → 勾选"使用 Unicode UTF-8 提供全球语言支持"）

**问题：提示路径过长**
- 解决：Windows 10 1607+ 可启用长路径支持
  1. 打开组策略编辑器（gpedit.msc）
  2. 计算机配置 → 管理模板 → 系统 → 文件系统
  3. 启用"启用 Win32 长路径"

**问题：无法创建某些文件名**
- 原因：文件名包含 Windows 保留名（如 CON、PRN）
- 解决：程序会自动添加下划线前缀（如 `_CON.html`）

#### macOS 平台

**问题：权限被拒绝**
- 解决：检查终端是否有完整磁盘访问权限
  - 系统偏好设置 → 安全性与隐私 → 隐私 → 完整磁盘访问权限
  - 添加终端应用

**问题：文件名大小写问题**
- 注意：APFS 文件系统默认不区分大小写但保留大小写
- 避免仅大小写不同的文件名

#### Linux 平台

**问题：权限不足**
- 解决：确保运行用户对目标目录有读写权限
  ```bash
  chmod -R u+rw /path/to/Get_transform
  ```

**问题：文件系统编码问题**
- 解决：确保系统 locale 设置为 UTF-8
  ```bash
  export LANG=en_US.UTF-8
  export LC_ALL=en_US.UTF-8
  ```

### 测试套件

本项目包含完整的跨平台兼容性测试套件，可以在不同平台上运行：

```bash
python Get_transform/test_cross_platform.py
```

测试覆盖：
- ✅ 文件名清理和安全化
- ✅ Windows 保留名处理
- ✅ UTF-8 编码支持
- ✅ 路径长度限制
- ✅ 控制字符过滤
- ✅ 权限检测
- ✅ 平台特定功能

## 版本信息

- **版本**：1.0
- **创建时间**：2025-10-24
- **作者**：Yorick
- **许可证**：MIT

## 联系支持
yorickhui@gmail.com
