#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式向导模块
为首次用户提供引导式配置体验

作者: AI Assistant
创建时间: 2025-01-27
"""

import os
from pathlib import Path
from typing import Tuple, Optional
from config_manager import ConfigManager


class UIFormatter:
    """UI格式化工具类"""
    
    @staticmethod
    def print_header(title: str, width: int = 60):
        """打印标题头部"""
        print("\n" + "=" * width)
        print(f" {title} ".center(width, "="))
        print("=" * width)
    
    @staticmethod
    def print_section(title: str, width: int = 50):
        """打印节标题"""
        print(f"\n{'─' * width}")
        print(f"  {title}")
        print(f"{'─' * width}")
    
    @staticmethod
    def print_box(content: str, width: int = 60):
        """打印内容框"""
        lines = content.split('\n')
        print("┌" + "─" * (width - 2) + "┐")
        for line in lines:
            # 处理中文和英文混排的宽度计算
            line_width = len(line.encode('utf-8')) - len(line)
            actual_width = len(line) + line_width // 2
            padding = max(0, width - 4 - actual_width)
            print(f"│ {line}{' ' * padding} │")
        print("└" + "─" * (width - 2) + "┘")
    
    @staticmethod
    def print_menu_option(number: int, description: str, details: str = ""):
        """打印菜单选项"""
        print(f"  {number}. {description}")
        if details:
            print(f"     {details}")
    
    @staticmethod
    def print_success(message: str):
        """打印成功信息"""
        print(f"✅ {message}")
    
    @staticmethod
    def print_warning(message: str):
        """打印警告信息"""
        print(f"⚠️  {message}")
    
    @staticmethod
    def print_error(message: str):
        """打印错误信息"""
        print(f"❌ {message}")
    
    @staticmethod
    def print_info(message: str):
        """打印信息"""
        print(f"ℹ️  {message}")
    
    @staticmethod
    def get_valid_input(prompt: str, valid_options: list = None, 
                       allow_empty: bool = False, error_msg: str = None) -> str:
        """获取有效输入"""
        while True:
            try:
                user_input = input(prompt).strip()
                
                if not user_input and not allow_empty:
                    if error_msg:
                        UIFormatter.print_error(error_msg)
                    else:
                        UIFormatter.print_error("输入不能为空")
                    continue
                
                if valid_options and user_input not in valid_options:
                    if error_msg:
                        UIFormatter.print_error(error_msg)
                    else:
                        UIFormatter.print_error(f"请输入有效选项: {', '.join(valid_options)}")
                    continue
                
                return user_input
                
            except EOFError:
                # 处理EOF (Ctrl+D)
                if allow_empty:
                    return ""
                else:
                    UIFormatter.print_error("输入被中断，请重试")
                    continue
            except KeyboardInterrupt:
                print("\n")
                UIFormatter.print_warning("操作被用户取消")
                raise


class InteractiveWizard:
    """交互式向导类"""
    
    def __init__(self, script_dir: Path, config_manager: ConfigManager):
        self.script_dir = script_dir
        self.config_manager = config_manager
        self.ui = UIFormatter()
        
        # 默认路径
        self.default_history_dir = self.script_dir / "history"
        self.default_new_dir = self.script_dir / "new"
        self.default_logs_dir = self.script_dir / "logs"
    
    def show_welcome(self):
        """显示欢迎界面"""
        self.ui.print_header("欢迎使用 Get_transform 智能文件清理工具")
        
        welcome_text = """Get_transform 是一个专为 GET笔记 用户设计的智能文件清理和整理工具。

主要功能：
• 智能识别并清理重复的笔记文件
• 自动将HTML文件重命名为有意义的标题
• 支持批量处理和时间戳管理
• 提供安全的试运行模式

本向导将帮助您完成初始配置，确保工具能够正常工作。"""
        
        self.ui.print_box(welcome_text)
        
        print("\n准备开始配置...")
        input("按回车键继续...")
    
    def explain_requirements(self):
        """解释使用要求"""
        self.ui.print_section("使用要求说明")
        
        requirements = """1. GET笔记导出文件
   • 您需要从 GET笔记 应用导出笔记数据
   • 导出文件通常包含时间戳命名的文件夹
   • 每个文件夹内应有 notes 子目录

2. 目录结构
   • History: 存放GET笔记导出的原始数据
   • New: 存放处理后的整理文件
   • Logs: 存放操作日志

3. 权限要求
   • 程序需要读取源文件的权限
   • 程序需要创建新文件和目录的权限"""
        
        print(requirements)
        
        ready = self.ui.get_valid_input(
            "\n是否已准备好开始配置? (y/n): ",
            ['y', 'yes', '是', 'n', 'no', '否'],
            error_msg="请输入 y(是) 或 n(否)"
        )
        
        if ready.lower() in ['n', 'no', '否']:
            self.ui.print_info("请准备好后重新运行程序")
            return False
        
        return True
    
    def configure_history_path(self) -> str:
        """配置history路径"""
        self.ui.print_section("步骤 1/3: 配置GET导出路径")
        
        print("History目录用于存放从GET笔记导出的原始数据。")
        print("这通常是一个包含多个时间戳文件夹的目录。")
        print()
        
        # 显示默认路径
        default_path = str(self.default_history_dir)
        print(f"默认路径: {default_path}")
        
        # 检查默认路径是否存在
        if self.default_history_dir.exists():
            self.ui.print_success("检测到默认路径存在")
            use_default = self.ui.get_valid_input(
                "是否使用默认路径? (y/n): ",
                ['y', 'yes', '是', 'n', 'no', '否']
            )
            
            if use_default.lower() in ['y', 'yes', '是']:
                return default_path
        
        # 让用户输入自定义路径
        while True:
            self.ui.print_info("请输入GET导出数据的完整路径")
            custom_path = input("路径: ").strip()
            
            if not custom_path:
                self.ui.print_error("路径不能为空")
                continue
            
            # 验证路径
            is_valid, error_msg = self._validate_path(custom_path)
            if is_valid:
                self.ui.print_success(f"路径验证成功: {custom_path}")
                return custom_path
            else:
                self.ui.print_error(f"路径验证失败: {error_msg}")
                
                # 提供修复建议
                suggestions = self._get_path_suggestions(custom_path, error_msg)
                if suggestions:
                    print("\n💡 修复建议:")
                    for suggestion in suggestions:
                        print(f"   • {suggestion}")
                print()
    
    def configure_output_paths(self) -> Tuple[str, str]:
        """配置输出路径"""
        self.ui.print_section("步骤 2/3: 配置输出路径")
        
        print("配置文件输出目录，用于存放处理后的文件和日志。")
        print()
        
        # New目录配置
        print("New目录: 存放处理后的整理文件")
        default_new = str(self.default_new_dir)
        print(f"默认路径: {default_new}")
        
        use_default_new = self.ui.get_valid_input(
            "是否使用默认New目录路径? (y/n): ",
            ['y', 'yes', '是', 'n', 'no', '否']
        )
        
        if use_default_new.lower() in ['y', 'yes', '是']:
            new_path = default_new
        else:
            while True:
                custom_new = input("请输入New目录路径: ").strip()
                if not custom_new:
                    self.ui.print_error("路径不能为空")
                    continue
                
                # 对于输出目录，我们允许它不存在（会自动创建）
                new_path = custom_new
                break
        
        # Logs目录配置
        print("\nLogs目录: 存放操作日志")
        default_logs = str(self.default_logs_dir)
        print(f"默认路径: {default_logs}")
        
        use_default_logs = self.ui.get_valid_input(
            "是否使用默认Logs目录路径? (y/n): ",
            ['y', 'yes', '是', 'n', 'no', '否']
        )
        
        if use_default_logs.lower() in ['y', 'yes', '是']:
            logs_path = default_logs
        else:
            while True:
                custom_logs = input("请输入Logs目录路径: ").strip()
                if not custom_logs:
                    self.ui.print_error("路径不能为空")
                    continue
                
                logs_path = custom_logs
                break
        
        return new_path, logs_path
    
    def configure_default_mode(self) -> str:
        """配置默认操作模式"""
        self.ui.print_section("步骤 3/3: 配置默认操作模式")
        
        print("选择您最常用的操作模式，这将作为程序启动时的默认选择。")
        print()
        
        modes = [
            ("1", "试运行模式", "查看将要执行的操作，不实际修改文件"),
            ("2", "正式运行模式", "自动选择处理模式并执行操作"),
            ("3", "仅复制模式", "跳过重复文件检测，仅复制和重命名文件")
        ]
        
        for mode_num, mode_name, mode_desc in modes:
            self.ui.print_menu_option(int(mode_num), mode_name, mode_desc)
        
        while True:
            choice = self.ui.get_valid_input(
                "\n请选择默认模式 (1-3): ",
                ['1', '2', '3'],
                error_msg="请输入 1、2 或 3"
            )
            
            mode_map = {
                '1': 'dry_run',
                '2': 'auto',
                '3': 'copy_only'
            }
            
            selected_mode = mode_map[choice]
            mode_names = {
                'dry_run': '试运行模式',
                'auto': '正式运行模式',
                'copy_only': '仅复制模式'
            }
            
            confirm = self.ui.get_valid_input(
                f"确认选择 {mode_names[selected_mode]} 作为默认模式? (y/n): ",
                ['y', 'yes', '是', 'n', 'no', '否']
            )
            
            if confirm.lower() in ['y', 'yes', '是']:
                return selected_mode
            else:
                print("请重新选择...")
    
    def show_configuration_summary(self, history_path: str, new_path: str, 
                                 logs_path: str, default_mode: str):
        """显示配置摘要"""
        self.ui.print_section("配置确认")
        
        mode_names = {
            'dry_run': '试运行模式',
            'auto': '正式运行模式',
            'copy_only': '仅复制模式'
        }
        
        summary = f"""配置摘要：

• GET导出路径: {history_path}
• 输出目录: {new_path}
• 日志目录: {logs_path}
• 默认模式: {mode_names.get(default_mode, default_mode)}

请确认以上配置是否正确。配置将保存到:
{self.config_manager.config_file}"""
        
        self.ui.print_box(summary)
        
        return self.ui.get_valid_input(
            "\n确认保存配置并开始使用? (y/n): ",
            ['y', 'yes', '是', 'n', 'no', '否']
        )
    
    def save_configuration(self, history_path: str, new_path: str, 
                          logs_path: str, default_mode: str):
        """保存配置"""
        # 设置配置值
        self.config_manager.set_history_dir(history_path)
        self.config_manager.set_new_dir(new_path)
        self.config_manager.set_logs_dir(logs_path)
        self.config_manager.set_default_mode(default_mode)
        
        # 保存配置文件
        success, error = self.config_manager.save_config()
        
        if success:
            self.ui.print_success(f"配置已保存到: {self.config_manager.config_file}")
            
            # 创建必要的目录
            self._create_directories(new_path, logs_path)
            
            return True
        else:
            self.ui.print_error(f"配置保存失败: {error}")
            return False
    
    def _create_directories(self, new_path: str, logs_path: str):
        """创建必要的目录"""
        directories = [
            (Path(new_path), "New目录"),
            (Path(logs_path), "Logs目录")
        ]
        
        print("\n🔧 创建输出目录...")
        for dir_path, dir_name in directories:
            try:
                if dir_path.exists():
                    self.ui.print_success(f"{dir_name}已存在")
                else:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    self.ui.print_success(f"{dir_name}创建成功")
            except Exception as e:
                self.ui.print_error(f"{dir_name}创建失败: {e}")
    
    def _validate_path(self, path_str: str) -> Tuple[bool, str]:
        """验证路径的有效性"""
        path = Path(path_str).expanduser()
        
        # 检查路径是否存在
        if not path.exists():
            return False, f"路径不存在: {path}"
        
        # 检查是否是目录
        if not path.is_dir():
            return False, f"路径不是目录: {path}"
        
        # 检查是否可读
        if not os.access(path, os.R_OK):
            return False, f"无法读取路径（权限不足）: {path}"
        
        return True, None
    
    def _get_path_suggestions(self, path_str: str, error_msg: str) -> list:
        """获取路径修复建议"""
        suggestions = []
        
        if "不存在" in error_msg:
            suggestions.append("检查路径拼写是否正确")
            suggestions.append("确认GET笔记导出已完成")
            suggestions.append("尝试使用绝对路径")
        
        elif "不是目录" in error_msg:
            suggestions.append("确认选择的是文件夹而不是文件")
            suggestions.append("检查路径是否指向正确的目录")
        
        elif "权限不足" in error_msg:
            suggestions.append("尝试以管理员权限运行")
            suggestions.append("检查文件夹的读取权限")
            suggestions.append("确认没有被其他程序占用")
        
        return suggestions
    
    def run(self) -> bool:
        """运行完整的向导流程"""
        try:
            # 1. 显示欢迎界面
            self.show_welcome()
            
            # 2. 解释使用要求
            if not self.explain_requirements():
                return False
            
            # 3. 配置history路径
            history_path = self.configure_history_path()
            
            # 4. 配置输出路径
            new_path, logs_path = self.configure_output_paths()
            
            # 5. 配置默认模式
            default_mode = self.configure_default_mode()
            
            # 6. 显示配置摘要
            confirm = self.show_configuration_summary(
                history_path, new_path, logs_path, default_mode
            )
            
            if confirm.lower() in ['y', 'yes', '是']:
                # 7. 保存配置
                if self.save_configuration(history_path, new_path, logs_path, default_mode):
                    self.ui.print_success("向导配置完成！")
                    print("\n现在可以开始使用 Get_transform 工具了。")
                    return True
                else:
                    self.ui.print_error("配置保存失败，请重试")
                    return False
            else:
                self.ui.print_warning("配置已取消")
                return False
                
        except KeyboardInterrupt:
            print("\n")
            self.ui.print_warning("向导被用户中断")
            return False
        except Exception as e:
            self.ui.print_error(f"向导运行过程中发生错误: {e}")
            return False