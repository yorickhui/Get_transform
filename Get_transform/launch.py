#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get_transform 启动脚本
自动检查Python版本、依赖安装，并启动主程序

作者: AI Assistant
创建时间: 2025-01-27
"""

import sys
import subprocess
import os
from pathlib import Path
from config_manager import ConfigManager


class InitializationManager:
    """目录初始化和路径配置管理"""
    
    def __init__(self, script_dir, config_manager: ConfigManager):
        self.script_dir = Path(script_dir)
        self.config_manager = config_manager
        self.default_history_dir = self.script_dir / "history"
        self.new_dir = self.script_dir / "new"
        self.logs_dir = self.script_dir / "logs"
    
    def create_directories(self):
        """创建必要的目录"""
        directories = [
            (self.default_history_dir, "history"),
            (self.new_dir, "new"),
            (self.logs_dir, "logs"),
        ]
        
        print("\n🔧 初始化目录结构")
        print("=" * 50)
        
        all_success = True
        for dir_path, dir_name in directories:
            try:
                if dir_path.exists():
                    print(f"✅ 目录已存在: {dir_name}/")
                else:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"✅ 目录创建成功: {dir_name}/")
            except Exception as e:
                print(f"❌ 目录创建失败 ({dir_name}/): {e}")
                all_success = False
        
        if not all_success:
            print("\n⚠️  部分目录创建失败，但程序将继续运行")
        
        return all_success
    
    def validate_history_path(self, path_str):
        """验证history路径的有效性"""
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
    
    def get_history_path(self, use_saved_config: bool = True):
        """获取并配置history路径"""
        # 如果配置中已有history路径且允许使用
        if use_saved_config:
            saved_path = self.config_manager.get_history_dir()
            if saved_path:
                # 验证保存的路径是否仍然有效
                is_valid, error_msg = self.validate_history_path(saved_path)
                if is_valid:
                    print(f"✅ 使用已保存的history路径: {saved_path}")
                    return saved_path
                else:
                    print(f"⚠️  保存的路径无效: {error_msg}")
                    print("需要重新配置...")
        
        print("\n📁 配置GET导出路径")
        print("=" * 50)
        
        default_path = str(self.default_history_dir)
        print(f"默认路径: {default_path}")
        
        while True:
            try:
                choice = input("\n是否使用默认路径? (y/n): ").strip().lower()
            except EOFError:
                choice = 'y'  # 默认使用
            
            if choice in ['y', 'yes', '是']:
                # 检查默认路径是否存在
                if self.default_history_dir.exists() and self.default_history_dir.is_dir():
                    print(f"✅ 使用默认路径: {default_path}")
                    return str(self.default_history_dir)
                else:
                    print(f"⚠️  默认路径不存在或不是目录")
                    continue
            
            elif choice in ['n', 'no', '否']:
                custom_path = input("\n请输入自定义的history路径: ").strip()
                
                if not custom_path:
                    print("❌ 路径不能为空")
                    continue
                
                is_valid, error_msg = self.validate_history_path(custom_path)
                if is_valid:
                    print(f"✅ 路径验证成功: {custom_path}")
                    return custom_path
                else:
                    print(f"❌ 路径验证失败: {error_msg}")
                    print("请检查路径是否正确、存在且有读取权限")
                    continue
            else:
                print("请输入 y(是) 或 n(否)")
    
    def initialize(self, force_reconfigure: bool = False):
        """执行初始化流程"""
        # 创建必要的目录
        self.create_directories()
        
        # 获取history路径（如果强制重新配置，则不使用保存的配置）
        history_path = self.get_history_path(use_saved_config=not force_reconfigure)
        
        # 保存配置
        self.config_manager.set_history_dir(history_path)
        self.config_manager.set_new_dir(str(self.new_dir))
        self.config_manager.set_logs_dir(str(self.logs_dir))
        
        success, error = self.config_manager.save_config()
        if success:
            print(f"\n✅ 配置已保存到: {self.config_manager.config_file}")
        else:
            print(f"\n⚠️  配置保存失败: {error}")
        
        return history_path


class DependencyChecker:
    """依赖检查和安装工具"""
    
    def __init__(self):
        self.min_python_version = (3, 6)
        self.requirements_file = Path(__file__).parent / "requirements.txt"
        self.main_script = Path(__file__).parent / "duplicate_file_cleaner.py"
        
    def check_python_version(self):
        """检查Python版本"""
        current_version = sys.version_info[:2]
        
        print(f"当前Python版本: {sys.version}")
        print(f"最低要求版本: {'.'.join(map(str, self.min_python_version))}")
        
        if current_version < self.min_python_version:
            print(f"\n❌ 错误: Python版本过低！")
            print(f"当前版本: {'.'.join(map(str, current_version))}")
            print(f"要求版本: {'.'.join(map(str, self.min_python_version))} 或更高")
            print("\n🔧 解决方案:")
            print("1. 请升级Python到最新版本")
            print("2. 推荐从 https://www.python.org 下载Python 3.8+")
            print("3. 安装时请确保勾选'Add Python to PATH'选项")
            return False
            
        print("✅ Python版本检查通过")
        return True
    
    def check_pip_availability(self):
        """检查pip是否可用"""
        try:
            # 尝试运行pip --version
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ pip 可用")
                return True
            else:
                print("❌ pip 不可用")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            print(f"❌ pip 检查失败: {e}")
            return False
    
    def read_requirements(self):
        """读取requirements.txt文件"""
        if not self.requirements_file.exists():
            print("❌ requirements.txt 文件不存在")
            return []
        
        try:
            with open(self.requirements_file, 'r', encoding='utf-8') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"📋 发现依赖包: {', '.join(requirements)}")
            return requirements
        except Exception as e:
            print(f"❌ 读取requirements.txt失败: {e}")
            return []
    
    def check_installed_packages(self, requirements):
        """检查已安装的包"""
        missing_packages = []
        
        for package in requirements:
            try:
                # 尝试导入包来检查是否已安装
                if package.lower() == 'beautifulsoup4':
                    import bs4
                else:
                    # 对于其他包，使用importlib
                    import importlib
                    importlib.import_module(package.replace('-', '_'))
                print(f"✅ {package} 已安装")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} 未安装")
        
        return missing_packages
    
    def install_package(self, package):
        """安装单个包"""
        print(f"\n🔧 正在安装 {package}...")
        
        try:
            # 使用python -m pip install来确保使用正确的pip
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                print(f"✅ {package} 安装成功")
                return True
            else:
                print(f"❌ {package} 安装失败")
                print(f"错误信息: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ {package} 安装超时")
            return False
        except Exception as e:
            print(f"❌ {package} 安装过程中出错: {e}")
            return False
    
    def install_dependencies(self, missing_packages):
        """安装缺失的依赖"""
        if not missing_packages:
            print("✅ 所有依赖都已安装")
            return True
        
        print(f"\n📦 需要安装的依赖包: {', '.join(missing_packages)}")
        
        while True:
            choice = input("\n是否自动安装缺失的依赖？(y/n/s跳过): ").lower().strip()
            
            if choice in ['y', 'yes', '是']:
                success_count = 0
                for package in missing_packages:
                    if self.install_package(package):
                        success_count += 1
                
                if success_count == len(missing_packages):
                    print("✅ 所有依赖安装成功")
                    return True
                else:
                    print(f"\n⚠️  部分依赖安装失败 ({success_count}/{len(missing_packages)})")
                    print("\n🔧 手动安装解决方案:")
                    print("1. 尝试使用管理员权限运行")
                    print("2. 检查网络连接")
                    print("3. 手动执行以下命令:")
                    for package in missing_packages:
                        print(f"   python -m pip install {package}")
                    
                    retry = input("\n是否重试安装？(y/n): ").lower().strip()
                    if retry in ['y', 'yes', '是']:
                        continue
                    else:
                        return False
                        
            elif choice in ['n', 'no', '否']:
                print("\n❌ 依赖安装被取消")
                print("🔧 手动安装解决方案:")
                for package in missing_packages:
                    print(f"   python -m pip install {package}")
                return False
                
            elif choice in ['s', 'skip', '跳过']:
                print("\n⚠️  跳过依赖安装")
                print("注意: 程序可能因缺少依赖而无法正常运行")
                return True
                
            else:
                print("请输入 y(是)/n(否)/s(跳过)")
    
    def launch_main_script(self, history_path=None, new_dir=None, logs_dir=None):
        """启动主程序"""
        if not self.main_script.exists():
            print(f"❌ 主脚本不存在: {self.main_script}")
            return False
        
        print(f"\n🚀 启动主程序: {self.main_script.name}")
        print("=" * 50)
        
        try:
            # 准备环境变量，传递配置路径
            env = os.environ.copy()
            if history_path:
                env['GET_HISTORY_PATH'] = history_path
            if new_dir:
                env['GET_NEW_PATH'] = new_dir
            if logs_dir:
                env['GET_LOGS_PATH'] = logs_dir
            
            # 使用当前Python解释器运行主脚本
            os.execve(sys.executable, [sys.executable, str(self.main_script)], env)
        except Exception as e:
            print(f"❌ 启动主程序失败: {e}")
            print(f"请手动运行: python {self.main_script}")
            return False
    
    def run(self):
        """运行完整的检查流程"""
        print("🌀 Get_transform 启动检查")
        print("=" * 50)
        
        # 1. 检查Python版本
        if not self.check_python_version():
            input("\n按回车键退出...")
            sys.exit(1)
        
        # 2. 检查pip可用性
        if not self.check_pip_availability():
            print("\n❌ pip 不可用，无法自动安装依赖")
            print("\n🔧 解决方案:")
            print("1. 确保pip已正确安装")
            print("2. 尝试重新安装Python并确保包含pip")
            print("3. 手动下载pip: https://pip.pypa.io/en/stable/installation/")
            input("\n按回车键退出...")
            sys.exit(1)
        
        # 3. 读取依赖列表
        requirements = self.read_requirements()
        if not requirements:
            print("\n⚠️  未发现依赖要求，直接启动主程序")
            self.launch_main_script()
            return
        
        # 4. 检查已安装的包
        missing_packages = self.check_installed_packages(requirements)
        
        # 5. 安装缺失的依赖
        if not self.install_dependencies(missing_packages):
            print("\n⚠️  依赖安装不完整，程序可能无法正常运行")
            proceed = input("是否仍要继续启动程序？(y/n): ").lower().strip()
            if proceed not in ['y', 'yes', '是']:
                input("按回车键退出...")
                sys.exit(1)
        
        # 6. 加载和初始化配置
        script_dir = Path(self.main_script).parent
        config_manager = ConfigManager(script_dir)
        
        # 尝试加载配置
        config_loaded, error_msg = config_manager.load_config()
        
        if config_loaded:
            print("\n✅ 配置文件加载成功")
            config_manager.display_config()
            
            # 验证配置中的路径
            paths_valid, validation_error = config_manager.validate_paths()
            if not paths_valid:
                print(f"\n⚠️  配置路径验证失败: {validation_error}")
                print("需要重新配置...")
                need_init = True
            else:
                # 询问是否使用现有配置
                try:
                    use_existing = input("\n是否使用现有配置? (y/n): ").strip().lower()
                except EOFError:
                    use_existing = 'y'
                
                need_init = use_existing not in ['y', 'yes', '是']
        else:
            print(f"\n⚠️  配置文件加载失败: {error_msg}")
            
            # 如果是文件损坏，尝试恢复
            if "格式错误" in error_msg or "结构无效" in error_msg:
                print("⚠️  检测到配置文件损坏，尝试恢复...")
                recovered, recovery_msg = config_manager.recover_from_corruption()
                if recovered:
                    print(f"✅ {recovery_msg}")
                else:
                    print(f"❌ {recovery_msg}")
            else:
                # 配置文件不存在，创建默认配置
                print("创建新的配置...")
                config_manager.create_default_config()
            
            need_init = True
        
        # 执行初始化流程
        if need_init:
            initializer = InitializationManager(script_dir, config_manager)
            try:
                history_path = initializer.initialize(force_reconfigure=not config_loaded)
            except KeyboardInterrupt:
                print("\n\n👋 用户取消初始化")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ 初始化失败: {e}")
                input("按回车键退出...")
                sys.exit(1)
        else:
            # 使用配置中的路径
            history_path = config_manager.get_history_dir()
            print(f"\n✅ 使用配置中的history路径: {history_path}")
        
        # 7. 启动主程序（传递配置）
        self.launch_main_script(
            history_path=history_path,
            new_dir=config_manager.get_new_dir(),
            logs_dir=config_manager.get_logs_dir()
        )


def main():
    """主入口函数"""
    try:
        checker = DependencyChecker()
        checker.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 启动过程中发生未预期的错误: {e}")
        input("按回车键退出...")
        sys.exit(1)


if __name__ == "__main__":
    main()