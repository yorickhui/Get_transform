#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台兼容性工具模块
提供路径处理、文件名清理、编码处理等跨平台功能

作者: AI Assistant
创建时间: 2025-01-27
"""

import os
import sys
import platform
from pathlib import Path
from typing import Tuple, Optional


class PlatformUtils:
    """跨平台工具类"""
    
    @staticmethod
    def get_platform_info() -> dict:
        """
        获取平台信息
        
        Returns:
            包含平台信息的字典
        """
        return {
            'system': platform.system(),  # Windows, Linux, Darwin (macOS)
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'python_version': sys.version,
            'encoding': sys.getdefaultencoding(),
            'filesystem_encoding': sys.getfilesystemencoding()
        }
    
    @staticmethod
    def is_windows() -> bool:
        """检查是否为Windows平台"""
        return platform.system() == 'Windows'
    
    @staticmethod
    def is_macos() -> bool:
        """检查是否为macOS平台"""
        return platform.system() == 'Darwin'
    
    @staticmethod
    def is_linux() -> bool:
        """检查是否为Linux平台"""
        return platform.system() == 'Linux'
    
    @staticmethod
    def normalize_path(path: Path) -> Path:
        """
        规范化路径，处理不同平台的路径表示
        
        Args:
            path: 输入路径
            
        Returns:
            规范化后的路径
        """
        # 展开用户目录 (~)
        path = path.expanduser()
        
        # 解析为绝对路径
        path = path.resolve()
        
        return path
    
    @staticmethod
    def get_path_display(path: Path) -> str:
        """
        获取路径的显示字符串，确保跨平台一致性
        
        Args:
            path: 路径对象
            
        Returns:
            路径字符串
        """
        # 使用as_posix()获取统一的正斜杠格式（便于显示和日志）
        # 但在Windows上实际文件操作仍会使用反斜杠
        return path.as_posix()
    
    @staticmethod
    def check_path_length(path: Path) -> Tuple[bool, Optional[str]]:
        """
        检查路径长度是否超过平台限制
        
        Args:
            path: 路径对象
            
        Returns:
            (是否合法, 错误消息)
        """
        path_str = str(path)
        
        # Windows路径长度限制
        if PlatformUtils.is_windows():
            # Windows传统限制为260字符（MAX_PATH）
            # 新版Windows 10支持长路径，但需要特殊配置
            max_path_length = 260
            
            if len(path_str) > max_path_length:
                return False, f"路径长度({len(path_str)})超过Windows限制({max_path_length}字符)"
        
        # Unix/Linux/macOS通常限制为4096
        else:
            max_path_length = 4096
            if len(path_str) > max_path_length:
                return False, f"路径长度({len(path_str)})超过系统限制({max_path_length}字符)"
        
        return True, None
    
    @staticmethod
    def safe_path_exists(path: Path) -> bool:
        """
        安全地检查路径是否存在，处理编码问题
        
        Args:
            path: 路径对象
            
        Returns:
            路径是否存在
        """
        try:
            return path.exists()
        except (OSError, UnicodeEncodeError) as e:
            # 在某些平台上，包含特殊字符的路径可能导致编码错误
            return False
    
    @staticmethod
    def safe_mkdir(path: Path, parents: bool = True, exist_ok: bool = True) -> Tuple[bool, Optional[str]]:
        """
        安全地创建目录，处理权限和编码问题
        
        Args:
            path: 目录路径
            parents: 是否创建父目录
            exist_ok: 目录已存在时是否报错
            
        Returns:
            (是否成功, 错误消息)
        """
        try:
            path.mkdir(parents=parents, exist_ok=exist_ok)
            return True, None
        except PermissionError:
            return False, f"权限不足，无法创建目录: {path}"
        except OSError as e:
            return False, f"创建目录失败: {e}"
        except Exception as e:
            return False, f"未知错误: {e}"
    
    @staticmethod
    def get_safe_filename_length() -> int:
        """
        获取安全的文件名长度限制
        
        Returns:
            推荐的文件名最大长度
        """
        # 大多数文件系统的文件名长度限制：
        # - Windows (NTFS): 255字符
        # - Linux (ext4): 255字节
        # - macOS (HFS+/APFS): 255 UTF-16字符
        # 
        # 为了跨平台兼容，使用较保守的值
        # 考虑到UTF-8编码和路径总长度限制，200是一个安全的值
        return 200
    
    @staticmethod
    def encode_path_for_system(path: Path) -> str:
        """
        将路径编码为系统文件系统编码
        
        Args:
            path: 路径对象
            
        Returns:
            编码后的路径字符串
        """
        path_str = str(path)
        
        # 在Windows上，Python 3会自动处理UTF-16编码
        # 在Unix/Linux上，使用文件系统编码
        try:
            if PlatformUtils.is_windows():
                # Windows使用UTF-16LE存储文件名
                return path_str
            else:
                # Unix/Linux使用文件系统编码（通常是UTF-8）
                fs_encoding = sys.getfilesystemencoding()
                return path_str.encode(fs_encoding, errors='surrogateescape').decode(fs_encoding, errors='surrogateescape')
        except Exception:
            # 如果编码失败，返回原始字符串
            return path_str
    
    @staticmethod
    def test_write_permission(directory: Path) -> Tuple[bool, Optional[str]]:
        """
        测试目录是否有写入权限
        
        Args:
            directory: 目录路径
            
        Returns:
            (是否有权限, 错误消息)
        """
        if not directory.exists():
            return False, "目录不存在"
        
        if not directory.is_dir():
            return False, "路径不是目录"
        
        # 尝试创建临时文件来测试写入权限
        test_file = directory / '.write_test_tmp'
        try:
            test_file.touch()
            test_file.unlink()
            return True, None
        except PermissionError:
            return False, "没有写入权限"
        except Exception as e:
            return False, f"权限测试失败: {e}"


def print_platform_info():
    """打印平台信息（用于调试）"""
    info = PlatformUtils.get_platform_info()
    print("=" * 60)
    print("平台信息:")
    print("=" * 60)
    for key, value in info.items():
        print(f"{key}: {value}")
    print("=" * 60)


if __name__ == "__main__":
    # 测试和演示
    print_platform_info()
