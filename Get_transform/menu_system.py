#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强菜单系统模块
提供统一的菜单界面和交互逻辑

作者: AI Assistant
创建时间: 2025-01-27
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from config_manager import ConfigManager
from wizard import UIFormatter


class EnhancedMainMenu:
    """增强的主菜单系统"""
    
    def __init__(self, config_manager: ConfigManager, cleaner_instance):
        self.config_manager = config_manager
        self.cleaner = cleaner_instance
        self.ui = UIFormatter()
        
        # 菜单选项定义
        self.menu_options = {
            "1": {
                "name": "试运行模式",
                "description": "查看将要执行的操作，不实际修改文件",
                "action": self._run_dry_run,
                "confirm": False
            },
            "2": {
                "name": "正式运行模式", 
                "description": "自动选择处理模式并执行操作",
                "action": self._run_full_execution,
                "confirm": True
            },
            "3": {
                "name": "仅复制模式",
                "description": "跳过重复文件检测，仅复制和重命名文件",
                "action": self._run_copy_only,
                "confirm": True
            },
            "4": {
                "name": "查看配置",
                "description": "显示当前配置信息",
                "action": self._show_configuration,
                "confirm": False
            },
            "5": {
                "name": "重新配置",
                "description": "修改路径设置和默认模式",
                "action": self._reconfigure,
                "confirm": False
            },
            "6": {
                "name": "退出程序",
                "description": "安全退出程序",
                "action": self._exit_program,
                "confirm": False
            }
        }
    
    def display_main_menu(self):
        """显示主菜单"""
        self.ui.print_header("Get_transform 智能文件清理工具", 70)
        
        # 显示当前配置概览
        self._show_config_summary()
        
        # 显示菜单选项
        self.ui.print_section("主菜单")
        
        for key, option in self.menu_options.items():
            self.ui.print_menu_option(
                int(key), 
                option["name"], 
                option["description"]
            )
        
        print("\n" + "─" * 50)
    
    def _show_config_summary(self):
        """显示配置摘要"""
        try:
            config = self.config_manager.config
            
            # 获取路径信息
            history_dir = config.get('history_dir', '未配置')
            new_dir = config.get('new_dir', '未配置')
            logs_dir = config.get('logs_dir', '未配置')
            default_mode = config.get('default_mode', '未配置')
            
            # 模式名称映射
            mode_names = {
                'dry_run': '试运行',
                'auto': '自动运行',
                'copy_only': '仅复制'
            }
            default_mode_name = mode_names.get(default_mode, default_mode)
            
            # 检查history目录状态
            history_status = "❌ 不存在"
            if history_dir != '未配置':
                history_path = Path(history_dir)
                if history_path.exists():
                    folders = self._get_folder_count(history_path)
                    history_status = f"✅ 存在 ({folders}个文件夹)"
            
            summary = f"""当前配置：
• GET导出路径: {history_dir} {history_status}
• 输出目录: {new_dir}
• 日志目录: {logs_dir}
• 默认模式: {default_mode_name}"""
            
            self.ui.print_box(summary, 70)
            
        except Exception as e:
            self.ui.print_warning(f"无法显示配置摘要: {e}")
    
    def _get_folder_count(self, history_path: Path) -> int:
        """获取history目录中的文件夹数量"""
        try:
            count = 0
            for item in history_path.iterdir():
                if item.is_dir():
                    # 检查是否包含时间戳
                    if item.name.startswith('voicenotes_'):
                        count += 1
            return count
        except:
            return 0
    
    def get_user_choice(self) -> str:
        """获取用户选择"""
        while True:
            try:
                choice = input("\n请输入选择 (1-6): ").strip()
                
                if not choice:
                    self.ui.print_error("请输入一个选项")
                    continue
                
                if choice not in self.menu_options:
                    valid_options = list(self.menu_options.keys())
                    self.ui.print_error(f"无效选择，请输入: {', '.join(valid_options)}")
                    continue
                
                return choice
                
            except EOFError:
                # EOF时默认选择退出
                return "6"
            except KeyboardInterrupt:
                print("\n")
                self.ui.print_warning("操作被取消")
                return "6"
    
    def execute_choice(self, choice: str) -> bool:
        """执行用户选择"""
        try:
            option = self.menu_options[choice]
            
            # 如果需要确认
            if option["confirm"]:
                if not self._confirm_action(option["name"]):
                    self.ui.print_info("操作已取消")
                    return True
            
            # 执行操作
            return option["action"]()
            
        except Exception as e:
            self.ui.print_error(f"执行操作时发生错误: {e}")
            return True
    
    def _confirm_action(self, action_name: str) -> bool:
        """确认操作"""
        confirm = self.ui.get_valid_input(
            f"确认执行 {action_name}? (y/n): ",
            ['y', 'yes', '是', 'n', 'no', '否']
        )
        return confirm.lower() in ['y', 'yes', '是']
    
    def _run_dry_run(self) -> bool:
        """运行试运行模式"""
        self.ui.print_section("试运行模式")
        
        try:
            # 检查history目录
            if not self._check_history_directory():
                return True
            
            print("正在分析文件...")
            result = self.cleaner.run_cleanup(dry_run=True, copy_files=True)
            
            self._display_dry_run_result(result)
            return True
            
        except Exception as e:
            self.ui.print_error(f"试运行失败: {e}")
            return True
    
    def _run_full_execution(self) -> bool:
        """运行正式执行模式"""
        self.ui.print_section("正式运行模式")
        
        try:
            # 检查history目录
            if not self._check_history_directory():
                return True
            
            print("正在执行文件清理和复制...")
            result = self.cleaner.run_cleanup(dry_run=False, copy_files=True)
            
            self._display_execution_result(result)
            return True
            
        except Exception as e:
            self.ui.print_error(f"执行失败: {e}")
            return True
    
    def _run_copy_only(self) -> bool:
        """运行仅复制模式"""
        self.ui.print_section("仅复制模式")
        
        try:
            # 检查history目录
            if not self._check_history_directory():
                return True
            
            # 获取文件夹列表
            folders = self.cleaner.get_sorted_folders()
            if not folders:
                self.ui.print_warning("未找到有效的文件夹")
                return True
            
            # 选择最新文件夹
            if len(folders) == 1:
                print("检测到单文件夹模式，将复制所有文件")
                newest_folder = folders[0][1]
            else:
                print(f"检测到多文件夹模式，将复制最新文件夹中的文件")
                newest_folder = folders[-1][1]
            
            print(f"处理文件夹: {Path(newest_folder).name}")
            
            result = self.cleaner.copy_and_rename_files(newest_folder, dry_run=False)
            self._display_copy_result(result)
            return True
            
        except Exception as e:
            self.ui.print_error(f"复制操作失败: {e}")
            return True
    
    def _show_configuration(self) -> bool:
        """显示详细配置信息"""
        self.ui.print_section("当前配置详情")
        
        try:
            self.config_manager.display_config()
            
            # 显示目录状态
            print("\n📁 目录状态检查:")
            self._check_directory_status()
            
        except Exception as e:
            self.ui.print_error(f"显示配置失败: {e}")
        
        return True
    
    def _reconfigure(self) -> bool:
        """重新配置"""
        self.ui.print_section("重新配置")
        
        # 询问用户要重新配置哪些部分
        print("请选择要重新配置的项目：")
        print("1. GET导出路径")
        print("2. 输出路径 (New/Logs目录)")
        print("3. 默认操作模式")
        print("4. 全部重新配置")
        print("5. 返回主菜单")
        
        choice = self.ui.get_valid_input(
            "请选择 (1-5): ",
            ['1', '2', '3', '4', '5']
        )
        
        if choice == '5':
            return True
        
        try:
            if choice == '1':
                self._reconfigure_history_path()
            elif choice == '2':
                self._reconfigure_output_paths()
            elif choice == '3':
                self._reconfigure_default_mode()
            elif choice == '4':
                # 导入向导进行完整重新配置
                from wizard import InteractiveWizard
                wizard = InteractiveWizard(
                    self.config_manager.script_dir,
                    self.config_manager
                )
                return wizard.run()
            
            # 保存配置
            success, error = self.config_manager.save_config()
            if success:
                self.ui.print_success("配置已更新")
            else:
                self.ui.print_error(f"配置保存失败: {error}")
                
        except Exception as e:
            self.ui.print_error(f"重新配置失败: {e}")
        
        return True
    
    def _exit_program(self) -> bool:
        """退出程序"""
        # 询问是否保存配置（如果有未保存的更改）
        self.ui.print_info("感谢使用 Get_transform！")
        return False  # 返回False表示退出主循环
    
    def _check_history_directory(self) -> bool:
        """检查history目录"""
        history_dir = self.config_manager.get_history_dir()
        if not history_dir:
            self.ui.print_error("未配置GET导出路径")
            return False
        
        history_path = Path(history_dir)
        if not history_path.exists():
            self.ui.print_error(f"GET导出路径不存在: {history_dir}")
            self.ui.print_info("请检查路径或重新配置")
            return False
        
        return True
    
    def _check_directory_status(self):
        """检查目录状态"""
        config = self.config_manager.config
        
        for dir_type in ['history_dir', 'new_dir', 'logs_dir']:
            dir_path = config.get(dir_type)
            if dir_path:
                path = Path(dir_path)
                if path.exists():
                    if path.is_dir():
                        self.ui.print_success(f"{dir_type}: ✅ 存在且可访问")
                        
                        # 显示额外信息
                        if dir_type == 'history_dir':
                            folder_count = self._get_folder_count(path)
                            print(f"   包含 {folder_count} 个时间戳文件夹")
                    else:
                        self.ui.print_error(f"{dir_type}: ❌ 不是目录")
                else:
                    if dir_type in ['new_dir', 'logs_dir']:
                        self.ui.print_warning(f"{dir_type}: ⚠️  不存在（将自动创建）")
                    else:
                        self.ui.print_error(f"{dir_type}: ❌ 不存在")
            else:
                self.ui.print_error(f"{dir_type}: ❌ 未配置")
    
    def _reconfigure_history_path(self):
        """重新配置history路径"""
        from wizard import InteractiveWizard
        wizard = InteractiveWizard(
            self.config_manager.script_dir,
            self.config_manager
        )
        new_path = wizard.configure_history_path()
        self.config_manager.set_history_dir(new_path)
    
    def _reconfigure_output_paths(self):
        """重新配置输出路径"""
        from wizard import InteractiveWizard
        wizard = InteractiveWizard(
            self.config_manager.script_dir,
            self.config_manager
        )
        new_path, logs_path = wizard.configure_output_paths()
        self.config_manager.set_new_dir(new_path)
        self.config_manager.set_logs_dir(logs_path)
    
    def _reconfigure_default_mode(self):
        """重新配置默认模式"""
        from wizard import InteractiveWizard
        wizard = InteractiveWizard(
            self.config_manager.script_dir,
            self.config_manager
        )
        default_mode = wizard.configure_default_mode()
        self.config_manager.set_default_mode(default_mode)
    
    def _display_dry_run_result(self, result: Dict[str, Any]):
        """显示试运行结果"""
        self.ui.print_section("试运行结果")
        
        print(f"📊 分析结果: {result['message']}")
        print(f"🔄 发现重复文件: {result['duplicate_count']} 个")
        
        if result.get('copy_result'):
            copy_result = result['copy_result']
            print(f"📄 将复制文件: {copy_result.get('total_files', 0)} 个")
            print(f"📁 目标目录: {copy_result.get('target_dir', '')}")
        
        print("\n💡 这是试运行结果，没有实际修改任何文件")
    
    def _display_execution_result(self, result: Dict[str, Any]):
        """显示执行结果"""
        self.ui.print_section("执行结果")
        
        print(f"✅ 操作完成: {result['message']}")
        print(f"🗑️  删除重复文件: {result['deleted_count']} 个")
        
        if result.get('copy_result'):
            copy_result = result['copy_result']
            print(f"📄 复制文件数量: {copy_result.get('copied_count', 0)} 个")
            print(f"📁 目标目录: {copy_result.get('target_dir', '')}")
        
        # 显示日志文件位置
        if hasattr(self.cleaner, 'logger') and self.cleaner.logger.handlers:
            for handler in self.cleaner.logger.handlers:
                if hasattr(handler, 'baseFilename'):
                    log_file = handler.baseFilename
                    print(f"📝 详细日志: {log_file}")
                    break
    
    def _display_copy_result(self, result: Dict[str, Any]):
        """显示复制结果"""
        self.ui.print_section("复制结果")
        
        print(f"✅ 复制完成: {result['message']}")
        print(f"📄 复制文件数量: {result.get('copied_count', 0)} 个")
        print(f"📁 目标目录: {result.get('target_dir', '')}")
        
        # 显示日志文件位置
        if hasattr(self.cleaner, 'logger') and self.cleaner.logger.handlers:
            for handler in self.cleaner.logger.handlers:
                if hasattr(handler, 'baseFilename'):
                    log_file = handler.baseFilename
                    print(f"📝 详细日志: {log_file}")
                    break
    
    def run(self):
        """运行主菜单循环"""
        while True:
            try:
                self.display_main_menu()
                choice = self.get_user_choice()
                
                if not self.execute_choice(choice):
                    break  # 退出程序
                    
            except KeyboardInterrupt:
                print("\n")
                self.ui.print_warning("程序被中断")
                break
            except Exception as e:
                self.ui.print_error(f"主菜单发生错误: {e}")
                
                retry = self.ui.get_valid_input(
                    "是否继续使用程序? (y/n): ",
                    ['y', 'yes', '是', 'n', 'no', '否']
                )
                
                if retry.lower() not in ['y', 'yes', '是']:
                    break