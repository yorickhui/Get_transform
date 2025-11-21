#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责读取、写入、验证和升级配置文件

作者: AI Assistant
创建时间: 2025-01-27
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


class ConfigManager:
    """配置管理器"""
    
    CONFIG_VERSION = "1.0"
    CONFIG_FILENAME = ".get_transform_config.json"
    
    DEFAULT_CONFIG = {
        "version": CONFIG_VERSION,
        "history_dir": None,
        "new_dir": None,
        "logs_dir": None,
        "default_mode": None
    }
    
    def __init__(self, script_dir: Path):
        """
        初始化配置管理器
        
        Args:
            script_dir: 脚本目录路径
        """
        self.script_dir = Path(script_dir)
        self.config_file = self.script_dir / self.CONFIG_FILENAME
        self.config = None
    
    def load_config(self) -> Tuple[bool, Optional[str]]:
        """
        加载配置文件
        
        Returns:
            (是否成功, 错误消息)
        """
        if not self.config_file.exists():
            return False, "配置文件不存在"
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            # 先尝试升级配置（补充缺失字段）
            self._upgrade_config()
            
            # 再验证配置结构
            is_valid, error_msg = self._validate_config_structure()
            if not is_valid:
                return False, f"配置文件结构无效: {error_msg}"
            
            return True, None
            
        except json.JSONDecodeError as e:
            return False, f"配置文件JSON格式错误: {e}"
        except Exception as e:
            return False, f"加载配置文件失败: {e}"
    
    def save_config(self) -> Tuple[bool, Optional[str]]:
        """
        保存配置文件
        
        Returns:
            (是否成功, 错误消息)
        """
        if self.config is None:
            return False, "配置为空，无法保存"
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True, None
        except Exception as e:
            return False, f"保存配置文件失败: {e}"
    
    def create_default_config(self) -> Dict[str, Any]:
        """
        创建默认配置
        
        Returns:
            默认配置字典
        """
        # 创建默认配置，使用脚本目录下的子目录
        default_config = self.DEFAULT_CONFIG.copy()
        default_config["history_dir"] = str(self.script_dir / "history")
        default_config["new_dir"] = str(self.script_dir / "new")
        default_config["logs_dir"] = str(self.script_dir / "logs")
        
        self.config = default_config
        return default_config
    
    def _validate_config_structure(self) -> Tuple[bool, Optional[str]]:
        """
        验证配置文件结构
        
        Returns:
            (是否有效, 错误消息)
        """
        if not isinstance(self.config, dict):
            return False, "配置不是字典类型"
        
        # 检查必需的键
        required_keys = ["version", "history_dir", "new_dir", "logs_dir", "default_mode"]
        for key in required_keys:
            if key not in self.config:
                return False, f"缺少必需的配置项: {key}"
        
        return True, None
    
    def _upgrade_config(self):
        """升级配置文件，补充缺失的字段"""
        updated = False
        
        # 检查并添加缺失的字段
        for key, default_value in self.DEFAULT_CONFIG.items():
            if key not in self.config:
                self.config[key] = default_value
                updated = True
        
        # 更新版本号
        if self.config.get("version") != self.CONFIG_VERSION:
            self.config["version"] = self.CONFIG_VERSION
            updated = True
        
        # 如果有更新，保存配置
        if updated:
            self.save_config()
    
    def validate_paths(self) -> Tuple[bool, Optional[str]]:
        """
        验证配置中的路径有效性
        
        Returns:
            (是否有效, 错误消息)
        """
        if self.config is None:
            return False, "配置未加载"
        
        # 验证history_dir
        history_dir = self.config.get("history_dir")
        if history_dir:
            path = Path(history_dir).expanduser()
            if not path.exists():
                return False, f"history目录不存在: {history_dir}"
            if not path.is_dir():
                return False, f"history路径不是目录: {history_dir}"
            if not os.access(path, os.R_OK):
                return False, f"history目录无读取权限: {history_dir}"
        
        return True, None
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        if self.config is None:
            return default
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        设置配置项
        
        Args:
            key: 配置键
            value: 配置值
        """
        if self.config is None:
            self.config = self.DEFAULT_CONFIG.copy()
        self.config[key] = value
    
    def get_history_dir(self) -> Optional[str]:
        """获取history目录路径"""
        return self.get("history_dir")
    
    def set_history_dir(self, path: str):
        """设置history目录路径"""
        self.set("history_dir", str(Path(path).expanduser().absolute()))
    
    def get_new_dir(self) -> Optional[str]:
        """获取new目录路径"""
        return self.get("new_dir")
    
    def set_new_dir(self, path: str):
        """设置new目录路径"""
        self.set("new_dir", str(Path(path).expanduser().absolute()))
    
    def get_logs_dir(self) -> Optional[str]:
        """获取logs目录路径"""
        return self.get("logs_dir")
    
    def set_logs_dir(self, path: str):
        """设置logs目录路径"""
        self.set("logs_dir", str(Path(path).expanduser().absolute()))
    
    def get_default_mode(self) -> Optional[str]:
        """获取默认运行模式"""
        return self.get("default_mode")
    
    def set_default_mode(self, mode: str):
        """设置默认运行模式"""
        self.set("default_mode", mode)
    
    def recover_from_corruption(self) -> Tuple[bool, str]:
        """
        从损坏的配置文件中恢复
        
        Returns:
            (是否成功, 消息)
        """
        try:
            # 备份损坏的配置文件
            if self.config_file.exists():
                backup_file = self.config_file.with_suffix('.json.bak')
                self.config_file.rename(backup_file)
            
            # 创建新的默认配置
            self.create_default_config()
            success, error = self.save_config()
            
            if success:
                return True, "已恢复为默认配置"
            else:
                return False, f"恢复失败: {error}"
                
        except Exception as e:
            return False, f"恢复过程中出错: {e}"
    
    def display_config(self):
        """显示当前配置"""
        if self.config is None:
            print("❌ 配置未加载")
            return
        
        print("\n📋 当前配置:")
        print("=" * 50)
        print(f"版本: {self.config.get('version', 'N/A')}")
        print(f"history目录: {self.config.get('history_dir', 'N/A')}")
        print(f"new目录: {self.config.get('new_dir', 'N/A')}")
        print(f"logs目录: {self.config.get('logs_dir', 'N/A')}")
        print(f"默认模式: {self.config.get('default_mode', 'N/A')}")
        print("=" * 50)
