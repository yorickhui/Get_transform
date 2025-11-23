# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **打包分发系统**: 完整的可执行文件构建和分发方案
  - PyInstaller 配置文件 (`get_transform.spec`)
  - 自动化构建脚本 (`scripts/build_executable.py`)
  - Linux/macOS 构建脚本 (`scripts/build.sh`)
  - Windows PowerShell 构建脚本 (`scripts/build.ps1`)
  - Makefile 支持一键构建
  - 详细的构建文档 (`BUILD.md`)
  
- **安装脚本**: 为不想构建可执行文件的用户提供备选方案
  - Linux/macOS 安装脚本 (`scripts/install.sh`)
  - Windows PowerShell 安装脚本 (`scripts/install.ps1`)
  - 自动创建虚拟环境
  - 自动安装依赖
  - 生成便捷的启动脚本 (`run.sh` / `run.bat`)

- **用户文档**:
  - 快速开始指南 (`QUICKSTART.md`) - 面向非技术用户
  - 完整的构建说明 (`BUILD.md`) - 包含所有平台的详细说明
  - 更新的 README - 新增打包分发章节

- **构建功能**:
  - 支持 Windows、macOS、Linux 三大平台
  - 单文件可执行文件（无需 Python 环境）
  - 包含所有依赖（beautifulsoup4 等）
  - UPX 压缩支持（减小文件体积）
  - 调试模式构建选项
  - 构建后自动测试
  - 清理和重新构建支持

### Changed
- 更新 README.md，新增三种使用方式：
  1. 直接运行可执行文件（推荐，无需 Python）
  2. 使用 Python 运行（开发者）
  3. 自己构建可执行文件
- 更新 .gitignore，排除构建产物和生成的启动脚本

### Documentation
- 新增 `BUILD.md`: 详细的构建文档
  - 系统要求（所有平台）
  - 构建方法（4 种方式）
  - 常见问题（9+ 个问题及解决方案）
  - 技术细节和优化建议
  - 发布检查清单
  
- 新增 `QUICKSTART.md`: 非技术用户快速开始指南
  - 下载和运行说明
  - 首次配置指导
  - 详细的使用流程
  - 常见问题解答
  - 使用技巧

## [1.0.0] - 2025-01-27

### Added
- 初始发布
- 智能时间戳识别和版本排序
- 重复文件检测和删除
- 文件复制重命名功能
- 交互式配置向导
- 配置持久化
- 跨平台兼容性（Windows/macOS/Linux）
- 完整的测试套件
- 中文用户界面

### Features
- **目录初始化**: 自动创建必要的目录结构
- **配置管理**: JSON 配置文件持久化
- **依赖检查**: 自动检查并安装依赖
- **路径验证**: 智能路径验证和错误提示
- **日志记录**: 详细的操作日志
- **文件名清理**: 跨平台文件名安全处理
- **UTF-8 支持**: 完整的 Unicode 字符支持

## 版本说明

### 版本号格式
- **主版本号**: 重大架构变更或不兼容更新
- **次版本号**: 新功能添加
- **修订号**: Bug 修复和小改进

### 发布流程
1. 更新 CHANGELOG.md
2. 更新版本号
3. 在所有平台上构建和测试
4. 创建 GitHub Release
5. 上传可执行文件
6. 更新文档

## 链接

- [GitHub 仓库](https://github.com/yorickhui/Get_transform)
- [问题跟踪](https://github.com/yorickhui/Get_transform/issues)
- [发布页面](https://github.com/yorickhui/Get_transform/releases)

---

**维护者**: Yorick (yorickhui@gmail.com)
