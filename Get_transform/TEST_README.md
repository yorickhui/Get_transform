# 跨平台兼容性测试说明

## 测试概述

本项目包含全面的跨平台兼容性测试套件，用于验证 Get_transform 工具在 Windows、macOS 和 Linux 平台上的行为一致性。

## 运行测试

### 基本用法

```bash
# 进入项目目录
cd Get_transform

# 运行所有测试
python test_cross_platform.py
```

### 使用虚拟环境

```bash
# 使用项目虚拟环境运行测试
/path/to/.venv/bin/python test_cross_platform.py
```

## 测试覆盖

### 1. 文件名清理测试 (TestFilenameSanitization)

- **test_illegal_characters**: 测试非法字符替换（`< > : " / \ | ? *`）
- **test_windows_reserved_names**: 测试 Windows 保留名称（CON, PRN, AUX, NUL, COM1-9, LPT1-9）
- **test_trailing_spaces_and_dots**: 测试尾部空格和点的处理
- **test_multiple_spaces**: 测试多余空格的合并
- **test_long_filename**: 测试超长文件名截断
- **test_utf8_characters**: 测试 UTF-8 字符支持（中文、日文、韩文、俄文、表情符号）
- **test_utf8_long_filename**: 测试超长 UTF-8 文件名的安全截断
- **test_empty_filename**: 测试空文件名处理
- **test_control_characters**: 测试控制字符过滤

### 2. 平台工具测试 (TestPlatformUtils)

- **test_platform_detection**: 测试平台检测功能
- **test_platform_info**: 测试平台信息获取
- **test_normalize_path**: 测试路径规范化
- **test_path_display**: 测试路径显示格式
- **test_path_length_check**: 测试路径长度验证
- **test_safe_filename_length**: 测试安全文件名长度获取

### 3. 路径操作测试 (TestPathOperations)

- **test_safe_mkdir**: 测试安全创建目录
- **test_safe_mkdir_parents**: 测试创建多级目录
- **test_safe_path_exists**: 测试安全的路径存在检查
- **test_write_permission**: 测试写入权限检查

### 4. 编码处理测试 (TestEncodingHandling)

- **test_utf8_path_handling**: 测试 UTF-8 路径创建和读写

## 测试结果示例

```
======================================================================
跨平台兼容性测试
======================================================================

============================================================
平台信息:
============================================================
system: Linux
release: 6.12.35
version: #1 SMP Mon Sep 22 17:54:17 UTC 2025
machine: x86_64
python_version: 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0]
encoding: utf-8
filesystem_encoding: utf-8
============================================================

test_control_characters ... ok
test_empty_filename ... ok
test_illegal_characters ... ok
test_long_filename ... ok
test_multiple_spaces ... ok
test_trailing_spaces_and_dots ... ok
test_utf8_characters ... ok
test_utf8_long_filename ... ok
test_windows_reserved_names ... ok
... (更多测试)

----------------------------------------------------------------------
Ran 20 tests in 0.071s

OK
```

## 平台特定注意事项

### Windows

- 测试会验证 Windows 保留设备名处理
- 检查路径长度限制（260 字符）
- 验证 UTF-16LE 编码兼容性
- 测试反斜杠路径分隔符

### macOS

- 测试 APFS 文件系统特性
- 验证不区分大小写但保留大小写的行为
- 测试 Unicode 规范化 (NFD)
- 检查权限和沙盒限制

### Linux

- 测试各种文件系统（ext4, btrfs, xfs 等）
- 验证 UTF-8 编码支持
- 测试符号链接和硬链接
- 检查区分大小写的文件名

## 故障排除

### 测试失败：缺少依赖

```bash
# 安装 beautifulsoup4
pip install beautifulsoup4
```

### 测试失败：权限问题

```bash
# Linux/macOS: 确保测试目录有写入权限
chmod -R u+rw Get_transform

# Windows: 以管理员身份运行
```

### 测试失败：编码问题

```bash
# Linux/macOS: 设置 UTF-8 locale
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

## 扩展测试

如果需要添加新的测试：

1. 在 `test_cross_platform.py` 中创建新的测试类或方法
2. 使用 `unittest.TestCase` 作为基类
3. 使用 `setUp()` 和 `tearDown()` 进行测试前后的清理
4. 使用断言方法验证预期行为

示例：

```python
def test_custom_feature(self):
    """测试自定义功能"""
    result = self.cleaner.custom_function()
    self.assertEqual(result, expected_value)
```

## 持续集成

建议在 CI/CD 流程中运行这些测试：

```yaml
# GitHub Actions 示例
- name: Run cross-platform tests
  run: |
    python Get_transform/test_cross_platform.py
```

## 贡献

如果发现平台特定的问题或测试用例缺失，欢迎：

1. 提交 Issue 描述问题
2. 添加测试用例复现问题
3. 提交 Pull Request 修复问题

## 参考文档

- Python pathlib: https://docs.python.org/3/library/pathlib.html
- 文件系统限制: 
  - Windows: https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
  - POSIX: https://pubs.opengroup.org/onlinepubs/9699919799/
