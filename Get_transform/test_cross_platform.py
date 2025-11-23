#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台兼容性测试模块
测试文件名清理、路径处理、编码处理等功能

作者: AI Assistant
创建时间: 2025-01-27
"""

import sys
import unittest
from pathlib import Path
import tempfile
import shutil

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from duplicate_file_cleaner import DuplicateFileCleaner
from platform_utils import PlatformUtils


class TestFilenameSanitization(unittest.TestCase):
    """测试文件名清理功能"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.temp_dir = Path(tempfile.mkdtemp())
        self.history_dir = self.temp_dir / "history"
        self.new_dir = self.temp_dir / "new"
        self.logs_dir = self.temp_dir / "logs"
        
        self.history_dir.mkdir()
        
        # 创建清理器实例
        self.cleaner = DuplicateFileCleaner(
            str(self.history_dir),
            str(self.new_dir),
            str(self.logs_dir)
        )
    
    def tearDown(self):
        """测试后清理"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_illegal_characters(self):
        """测试非法字符替换"""
        test_cases = [
            ('file<name', 'file_name'),
            ('file>name', 'file_name'),
            ('file:name', 'file_name'),
            ('file"name', 'file_name'),
            ('file/name', 'file_name'),
            ('file\\name', 'file_name'),
            ('file|name', 'file_name'),
            ('file?name', 'file_name'),
            ('file*name', 'file_name'),
        ]
        
        for input_name, expected_output in test_cases:
            result = self.cleaner.sanitize_filename(input_name)
            self.assertEqual(result, expected_output,
                           f"Failed for input: {input_name}")
    
    def test_windows_reserved_names(self):
        """测试Windows保留名称"""
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL',
                         'COM1', 'COM2', 'COM3', 'COM4', 'COM5',
                         'COM6', 'COM7', 'COM8', 'COM9',
                         'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5',
                         'LPT6', 'LPT7', 'LPT8', 'LPT9']
        
        for name in reserved_names:
            # 测试大写
            result = self.cleaner.sanitize_filename(name)
            self.assertTrue(result.startswith('_'),
                          f"Reserved name {name} not handled correctly")
            
            # 测试小写
            result_lower = self.cleaner.sanitize_filename(name.lower())
            self.assertTrue(result_lower.startswith('_'),
                          f"Reserved name {name.lower()} not handled correctly")
            
            # 测试带扩展名的情况
            result_ext = self.cleaner.sanitize_filename(f"{name}.txt")
            self.assertTrue(result_ext.startswith('_'),
                          f"Reserved name with extension {name}.txt not handled correctly")
    
    def test_trailing_spaces_and_dots(self):
        """测试尾部空格和点的处理"""
        test_cases = [
            ('filename ', 'filename'),
            ('filename.', 'filename'),
            ('filename. ', 'filename'),
            ('filename  ', 'filename'),
            ('filename..', 'filename'),
            ('filename...', 'filename'),
        ]
        
        for input_name, expected_output in test_cases:
            result = self.cleaner.sanitize_filename(input_name)
            self.assertEqual(result, expected_output,
                           f"Failed for input: '{input_name}'")
    
    def test_multiple_spaces(self):
        """测试多余空格处理"""
        test_cases = [
            ('file  name', 'file name'),
            ('file   name', 'file name'),
            ('file\t\tname', 'file name'),
            ('  filename  ', 'filename'),
        ]
        
        for input_name, expected_output in test_cases:
            result = self.cleaner.sanitize_filename(input_name)
            self.assertEqual(result, expected_output,
                           f"Failed for input: '{input_name}'")
    
    def test_long_filename(self):
        """测试超长文件名处理"""
        # 创建一个超长的文件名（大于200字符）
        long_name = 'a' * 250
        result = self.cleaner.sanitize_filename(long_name)
        
        # 结果应该被截断
        self.assertLessEqual(len(result.encode('utf-8')), 200,
                           "Long filename not truncated properly")
    
    def test_utf8_characters(self):
        """测试UTF-8字符处理"""
        test_cases = [
            '中文文件名',
            '日本語ファイル名',
            '한국어파일명',
            'Файл на русском',
            'Émojis 🎉📁💾',
            '混合Chinese和English文件名'
        ]
        
        for name in test_cases:
            result = self.cleaner.sanitize_filename(name)
            self.assertTrue(len(result) > 0,
                          f"UTF-8 name '{name}' resulted in empty string")
            # 验证可以编码为UTF-8
            try:
                result.encode('utf-8')
            except UnicodeEncodeError:
                self.fail(f"Result cannot be encoded as UTF-8: {result}")
    
    def test_utf8_long_filename(self):
        """测试超长UTF-8文件名的截断"""
        # 中文字符通常占3字节
        long_chinese = '中' * 100  # 300字节
        result = self.cleaner.sanitize_filename(long_chinese, max_length=200)
        
        # 验证截断后的字节长度
        result_bytes = len(result.encode('utf-8'))
        self.assertLessEqual(result_bytes, 200,
                           f"UTF-8 filename too long: {result_bytes} bytes")
        
        # 验证截断后仍然是有效的UTF-8字符串
        try:
            result.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            self.fail("Truncated UTF-8 filename is not valid")
    
    def test_empty_filename(self):
        """测试空文件名处理"""
        test_cases = ['', '   ', '...', '. . .']
        
        for name in test_cases:
            result = self.cleaner.sanitize_filename(name)
            self.assertEqual(result, 'untitled',
                           f"Empty filename '{name}' not handled correctly")
    
    def test_control_characters(self):
        """测试控制字符处理"""
        # 测试各种控制字符
        for i in range(0x00, 0x20):
            name = f"file{chr(i)}name"
            result = self.cleaner.sanitize_filename(name)
            self.assertNotIn(chr(i), result,
                           f"Control character 0x{i:02x} not removed")


class TestPlatformUtils(unittest.TestCase):
    """测试平台工具类"""
    
    def test_platform_detection(self):
        """测试平台检测"""
        # 至少有一个平台应该返回True
        platforms = [
            PlatformUtils.is_windows(),
            PlatformUtils.is_macos(),
            PlatformUtils.is_linux()
        ]
        self.assertTrue(any(platforms),
                       "No platform detected")
        
        # 只能有一个平台返回True
        self.assertEqual(sum(platforms), 1,
                       "Multiple platforms detected")
    
    def test_platform_info(self):
        """测试平台信息获取"""
        info = PlatformUtils.get_platform_info()
        
        # 验证必需的键存在
        required_keys = ['system', 'python_version', 'encoding']
        for key in required_keys:
            self.assertIn(key, info,
                        f"Missing key in platform info: {key}")
    
    def test_normalize_path(self):
        """测试路径规范化"""
        # 测试相对路径转绝对路径
        relative_path = Path(".")
        normalized = PlatformUtils.normalize_path(relative_path)
        self.assertTrue(normalized.is_absolute(),
                       "Path not converted to absolute")
    
    def test_path_display(self):
        """测试路径显示格式"""
        test_path = Path("/home/user/documents")
        display = PlatformUtils.get_path_display(test_path)
        
        # 显示格式应该使用正斜杠
        self.assertIn('/', display)
        self.assertNotIn('\\', display)
    
    def test_path_length_check(self):
        """测试路径长度检查"""
        # 正常长度的路径
        normal_path = Path("/home/user/file.txt")
        is_valid, error = PlatformUtils.check_path_length(normal_path)
        self.assertTrue(is_valid, f"Normal path rejected: {error}")
        
        # 超长路径（模拟）
        if PlatformUtils.is_windows():
            long_path = Path("C:\\" + "a" * 300)
            is_valid, error = PlatformUtils.check_path_length(long_path)
            self.assertFalse(is_valid,
                           "Overlong path not detected on Windows")
    
    def test_safe_filename_length(self):
        """测试安全文件名长度"""
        max_length = PlatformUtils.get_safe_filename_length()
        
        # 应该返回一个合理的值
        self.assertGreater(max_length, 0)
        self.assertLessEqual(max_length, 255)


class TestPathOperations(unittest.TestCase):
    """测试路径操作"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """测试后清理"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_safe_mkdir(self):
        """测试安全创建目录"""
        new_dir = self.temp_dir / "test_dir"
        success, error = PlatformUtils.safe_mkdir(new_dir)
        
        self.assertTrue(success, f"Failed to create directory: {error}")
        self.assertTrue(new_dir.exists())
    
    def test_safe_mkdir_parents(self):
        """测试创建多级目录"""
        nested_dir = self.temp_dir / "level1" / "level2" / "level3"
        success, error = PlatformUtils.safe_mkdir(nested_dir, parents=True)
        
        self.assertTrue(success, f"Failed to create nested directory: {error}")
        self.assertTrue(nested_dir.exists())
    
    def test_safe_path_exists(self):
        """测试安全的路径存在检查"""
        # 存在的路径
        self.assertTrue(PlatformUtils.safe_path_exists(self.temp_dir))
        
        # 不存在的路径
        non_existent = self.temp_dir / "does_not_exist"
        self.assertFalse(PlatformUtils.safe_path_exists(non_existent))
    
    def test_write_permission(self):
        """测试写入权限检查"""
        # 临时目录应该有写入权限
        has_permission, error = PlatformUtils.test_write_permission(self.temp_dir)
        self.assertTrue(has_permission,
                       f"Temp directory should be writable: {error}")


class TestEncodingHandling(unittest.TestCase):
    """测试编码处理"""
    
    def test_utf8_path_handling(self):
        """测试UTF-8路径处理"""
        test_paths = [
            '中文路径',
            '日本語パス',
            'путь',
            'caminho',
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            
            for path_name in test_paths:
                test_path = base_path / path_name
                
                # 尝试创建目录
                try:
                    test_path.mkdir(exist_ok=True)
                    
                    # 验证目录创建成功
                    self.assertTrue(test_path.exists(),
                                  f"Failed to create UTF-8 path: {path_name}")
                    
                    # 创建文件
                    test_file = test_path / "test.txt"
                    test_file.write_text("test content", encoding='utf-8')
                    
                    # 验证文件创建成功
                    self.assertTrue(test_file.exists(),
                                  f"Failed to create file in UTF-8 path: {path_name}")
                    
                    # 读取文件
                    content = test_file.read_text(encoding='utf-8')
                    self.assertEqual(content, "test content")
                    
                except (OSError, UnicodeError) as e:
                    # 在某些文件系统上可能不支持某些字符
                    # 这不算失败，只是跳过
                    print(f"Skipping unsupported path: {path_name} ({e})")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestFilenameSanitization))
    suite.addTests(loader.loadTestsFromTestCase(TestPlatformUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestPathOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestEncodingHandling))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回是否所有测试都通过
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 70)
    print("跨平台兼容性测试")
    print("=" * 70)
    print()
    
    # 打印平台信息
    from platform_utils import print_platform_info
    print_platform_info()
    print()
    
    # 运行测试
    success = run_tests()
    
    # 退出码
    sys.exit(0 if success else 1)
