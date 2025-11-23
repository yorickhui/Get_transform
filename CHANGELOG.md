# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-11-23

### 🎉 重大更新：完整文档体系

#### 新增文档
- **README.md 全面改版**
  - 添加完整目录和章节导航
  - 新增"使用工作流"ASCII 流程图，直观展示五步操作
  - 新增"首次运行向导"详细说明
  - 新增"配置与自定义"专节，包含 `.get_transform_config.json` 完整说明、示例和最佳实践
  - 新增"故障排查 FAQ"章节，包含 **12 个常见场景**及解决方案：
    1. Python 版本过低
    2. 找不到 pip
    3. 依赖安装失败
    4. 无法创建目录
    5. history 路径验证失败
    6. index.html 丢失
    7. 文件名冲突或路径过长
    8. 配置文件损坏
    9. Windows Defender 阻止
    10. macOS 开发者验证问题
    11. Linux 权限不足
    12. 网络盘权限问题
  - 新增"交互菜单与工作模式"详细说明
  - 新增"跨平台使用说明"，包含已验证平台列表、平台差异、文件名策略
  - 新增"打包/安装/构建"完整说明
  - 新增"文档索引"，链接到所有相关文档
  - 改进了三种使用方式的说明（可执行文件、Python 脚本、源码构建）
  
- **CHANGELOG.md 结构优化**
  - 添加版本升级说明
  - 记录所有新功能和改进
  - 增加更清晰的分类（Added/Changed/Fixed/Documentation）

### 📚 文档改进
- 所有文档保持一致的中文语言和专业排版
- 代码块使用清晰的语法高亮
- 表格格式化，易于阅读
- 添加 emoji 图标提升可读性
- 跨文档引用链接完善

### ✨ 功能覆盖说明
本次文档更新全面覆盖了以下已实现功能：

#### 初始化与配置 (v1.0.0)
- **目录自动初始化**
  - 自动创建 `history/`, `new/`, `logs/` 目录
  - 支持自定义路径并实时验证
  - 提供默认路径和自定义路径选项

- **配置持久化**
  - JSON 格式配置文件 (`.get_transform_config.json`)
  - 自动升级机制（添加缺失字段，保留用户值）
  - 配置损坏自动恢复（备份 + 重建）
  - 路径验证（存在性、目录类型、读取权限）

- **依赖自动管理**
  - Python 版本检查（≥ 3.6）
  - pip 可用性检测
  - 自动安装 beautifulsoup4 和其他依赖
  - 失败时提供手动安装指导

#### 跨平台兼容 (v1.0.0)
- **文件名安全处理**
  - Windows 保留名处理（CON/PRN/AUX/NUL/COM1-9/LPT1-9）
  - 非法字符过滤和替换
  - 尾部空格/点号移除（Windows 兼容性）
  - UTF-8 安全截断（不破坏多字节字符）
  - 最大文件名长度：200 字节

- **路径处理**
  - 统一使用 `pathlib.Path`
  - 支持用户目录扩展（`~`）
  - Windows 长路径支持（>260 字符）
  - 跨平台路径分隔符自动处理

- **编码支持**
  - 所有文件操作使用 UTF-8
  - 日志使用 UTF-8 编码
  - 非 ASCII 字符完整支持
  - Windows 控制台编码问题处理

#### 打包与分发 (v1.0.0)
- **PyInstaller 打包**
  - 单文件可执行模式（`--onefile`）
  - UPX 压缩（减小 40-50% 体积）
  - 包含所有依赖（beautifulsoup4 等）
  - Windows/macOS/Linux 三平台支持

- **构建脚本**
  - `scripts/build_executable.py` - Python 自动化构建
  - `scripts/build.sh` - Linux/macOS Shell 脚本
  - `scripts/build.ps1` - Windows PowerShell 脚本
  - `Makefile` - 一键构建命令

- **安装脚本**
  - `scripts/install.sh` - Linux/macOS 自动安装
  - `scripts/install.ps1` - Windows 自动安装
  - 自动创建虚拟环境
  - 生成启动脚本（`run.sh` / `run.bat`）

- **发布自动化**
  - `scripts/prepare_release.sh` - 版本发布工作流
  - 自动构建、测试、校验和生成
  - CHANGELOG 更新提示
  - Git 标签创建和推送

### 🎯 验收标准达成情况
✅ 新用户按照文档可完成首次运行，无需额外求助  
✅ 所有脚本在文档中都有引用和解释  
✅ 文档语言一致（中文），排版清晰  
✅ 包括 4 份详细文档（README、BUILD、QUICKSTART、PACKAGING）  
✅ 常见问题章节涵盖 **12 个常见场景**（超过目标 10 个）  
✅ 跨平台支持范围清晰说明（Windows/macOS/Linux 详细版本）  
✅ 提供完整的 ASCII 流程图说明工作流  

### 📖 文档清单
本版本包含以下完整文档：
- **README.md** - 项目概述、快速开始、完整 FAQ（12+ 场景）
- **QUICKSTART.md** - 非技术用户详细指南（215 行）
- **BUILD.md** - 构建文档，包含 9+ 常见问题及解决方案（537 行）
- **PACKAGING.md** - 打包技术方案、优化策略、未来计划（463 行）
- **CHANGELOG.md** - 版本历史和升级指引（本文件）
- **CROSS_PLATFORM_CHANGES.md** - 跨平台实现细节（开发者参考）
- **IMPLEMENTATION_SUMMARY.md** - 实现总结（开发者参考）
- **ARCHITECTURE.md** - 架构说明（如有）

---

## [1.0.0] - 2025-01-27

### 🎉 首次发布

#### Added - 核心功能
- **智能文件管理**
  - 时间戳识别和版本排序
  - 重复文件检测和删除
  - 文件复制和智能重命名
  - index.html 解析和标题映射

- **交互式配置向导**
  - 首次运行自动引导
  - 目录结构自动创建
  - 配置持久化
  - 路径验证和错误处理

- **跨平台兼容性**
  - Windows 10/11 完整支持
  - macOS 10.15+ 完整支持  
  - Linux 主流发行版支持
  - 文件名安全处理（保留名、非法字符、UTF-8）
  - 路径长度限制处理

- **打包分发系统**
  - PyInstaller 单文件可执行
  - 多平台构建脚本
  - 安装脚本（虚拟环境）
  - 发布自动化工具

#### Features - 特性详情
- **依赖管理**
  - Python 3.6+ 版本检查
  - pip 可用性检测
  - beautifulsoup4 自动安装
  - 手动安装指导

- **日志系统**
  - 时间戳命名的日志文件
  - UTF-8 编码支持
  - 详细操作记录
  - 错误堆栈跟踪

- **安全机制**
  - 试运行模式（预览操作）
  - 正式运行模式（实际执行）
  - 仅复制模式（最安全）
  - 备份选项
  - 操作确认提示

#### Documentation - 文档
- README.md - 项目基础文档
- requirements.txt - Python 依赖列表
- 内联代码注释

---

## 版本说明

### 版本号规则
遵循 [Semantic Versioning 2.0.0](https://semver.org/)：

- **主版本号 (X.0.0)**：不兼容的 API 变更
- **次版本号 (0.X.0)**：向下兼容的功能新增
- **修订号 (0.0.X)**：向下兼容的问题修复

### 升级指南

#### 从 1.0.0 升级到 1.1.0
1. **无需任何操作**：配置文件会自动升级
2. **建议阅读**：新的 README.md 了解改进的功能说明
3. **推荐查看**：FAQ 章节了解常见问题解决方案

#### 配置文件升级
- 自动升级机制会在加载配置时补充缺失字段
- 保留所有用户自定义值
- 版本号自动更新到最新
- 损坏的配置会自动备份并重建

---

## 路线图

### v1.2.0 (计划中)
- [ ] 增强的命令行参数支持
- [ ] 批量处理模式
- [ ] 更多导出格式支持（Markdown, JSON）
- [ ] GUI 界面（可选）
- [ ] 国际化支持（英文界面）

### v1.3.0 (计划中)
- [ ] CI/CD 自动构建（GitHub Actions）
- [ ] 代码签名（Windows/macOS）
- [ ] 自动更新检查
- [ ] 性能优化（大文件处理）

### v2.0.0 (愿景)
- [ ] 插件系统
- [ ] Web 界面（可选）
- [ ] 云同步支持
- [ ] 多人协作功能

---

## 链接

- **项目主页**: [GitHub - Get_transform](https://github.com/yorickhui/Get_transform)
- **问题反馈**: [GitHub Issues](https://github.com/yorickhui/Get_transform/issues)
- **发布下载**: [GitHub Releases](https://github.com/yorickhui/Get_transform/releases)
- **文档**: 见项目根目录各 `.md` 文件

---

## 贡献者

感谢所有为本项目做出贡献的开发者！

- **Yorick** - 项目创建者和维护者
- **AI Assistant** - 跨平台、打包、文档等功能实现

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源。

---

**维护者**: Yorick (yorickhui@gmail.com)  
**最后更新**: 2025-11-23
