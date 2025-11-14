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
    
    def initialize_directories(self):
        """初始化目录结构"""
        try:
            from directory_manager import DirectoryManager
            
            print("\n" + "=" * 50)
            dir_manager = DirectoryManager(Path(__file__).parent)
            success = dir_manager.initialize_on_first_run()
            
            if not success:
                print("\n⚠️  目录初始化未完成")
                print("如需帮助，请参考程序文档")
                proceed = input("\n是否仍要继续启动程序？(y/n): ").lower().strip()
                if proceed not in ['y', 'yes', '是']:
                    input("按回车键退出...")
                    sys.exit(1)
            
            print("=" * 50)
        except Exception as e:
            print(f"\n⚠️  目录初始化出错: {e}")
            print("将尝试继续启动程序...")
    
    def launch_main_script(self):
        """启动主程序"""
        if not self.main_script.exists():
            print(f"❌ 主脚本不存在: {self.main_script}")
            return False
        
        print(f"\n🚀 启动主程序: {self.main_script.name}")
        print("=" * 50)
        
        try:
            # 使用当前Python解释器运行主脚本
            os.execv(sys.executable, [sys.executable, str(self.main_script)])
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
            print("\n⚠️  未发现依赖要求，继续初始化...")
        else:
            # 4. 检查已安装的包
            missing_packages = self.check_installed_packages(requirements)
            
            # 5. 安装缺失的依赖
            if not self.install_dependencies(missing_packages):
                print("\n⚠️  依赖安装不完整，程序可能无法正常运行")
                proceed = input("是否仍要继续启动程序？(y/n): ").lower().strip()
                if proceed not in ['y', 'yes', '是']:
                    input("按回车键退出...")
                    sys.exit(1)
        
        # 6. 初始化目录结构（在启动主程序前）
        self.initialize_directories()
        
        # 7. 启动主程序
        self.launch_main_script()


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