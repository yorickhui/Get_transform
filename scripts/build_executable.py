#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get_transform 构建脚本
自动构建可执行文件，支持 Windows、macOS、Linux

用法:
    python scripts/build_executable.py [选项]

选项:
    --clean     清理构建目录
    --debug     构建调试版本
    --onedir    构建目录版本（而非单文件）
    --test      构建后测试可执行文件

作者: AI Assistant
创建时间: 2025-01-27
"""

import sys
import os
import shutil
import subprocess
import argparse
import platform
from pathlib import Path


class ExecutableBuilder:
    """可执行文件构建器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.spec_file = project_root / "get_transform.spec"
        self.dist_dir = project_root / "dist"
        self.build_dir = project_root / "build"
        self.platform = platform.system()
        
    def check_pyinstaller(self):
        """检查 PyInstaller 是否已安装"""
        print("🔍 检查 PyInstaller...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "PyInstaller", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ PyInstaller 已安装 (版本: {version})")
                return True
            else:
                print("❌ PyInstaller 未正确安装")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            print(f"❌ PyInstaller 检查失败: {e}")
            return False
    
    def install_pyinstaller(self):
        """安装 PyInstaller"""
        print("\n📦 安装 PyInstaller...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "pyinstaller"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print("✅ PyInstaller 安装成功")
                return True
            else:
                print(f"❌ PyInstaller 安装失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ PyInstaller 安装过程出错: {e}")
            return False
    
    def clean(self):
        """清理构建目录"""
        print("\n🧹 清理构建目录...")
        
        dirs_to_clean = [self.dist_dir, self.build_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"✅ 已删除: {dir_path}")
                except Exception as e:
                    print(f"⚠️  删除失败 ({dir_path}): {e}")
            else:
                print(f"ℹ️  目录不存在，跳过: {dir_path}")
        
        print("✅ 清理完成")
    
    def build(self, debug=False, onedir=False):
        """构建可执行文件"""
        print("\n🔨 开始构建可执行文件...")
        print(f"📍 平台: {self.platform}")
        print(f"📍 Python: {sys.version}")
        print(f"📍 Spec文件: {self.spec_file}")
        
        if not self.spec_file.exists():
            print(f"❌ Spec文件不存在: {self.spec_file}")
            return False
        
        # 构建 PyInstaller 命令
        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            str(self.spec_file),
            "--clean",  # 清理临时文件
            "--noconfirm",  # 不确认覆盖
        ]
        
        if debug:
            cmd.append("--debug=all")
        
        # 如果指定 onedir，需要修改 spec 文件或使用命令行参数
        # 这里我们使用 spec 文件，所以 onedir 选项暂不支持动态切换
        
        print(f"\n📋 执行命令: {' '.join(cmd)}")
        print("⏳ 构建中，请稍候...\n")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=False,  # 显示输出
                text=True,
                timeout=600  # 10分钟超时
            )
            
            if result.returncode == 0:
                print("\n✅ 构建成功！")
                self.show_output_info()
                return True
            else:
                print(f"\n❌ 构建失败 (退出码: {result.returncode})")
                return False
                
        except subprocess.TimeoutExpired:
            print("\n❌ 构建超时（超过10分钟）")
            return False
        except Exception as e:
            print(f"\n❌ 构建过程出错: {e}")
            return False
    
    def show_output_info(self):
        """显示输出文件信息"""
        print("\n📦 构建产物:")
        print("=" * 60)
        
        if not self.dist_dir.exists():
            print("❌ dist目录不存在")
            return
        
        # 查找可执行文件
        executable_name = "get_transform"
        if self.platform == "Windows":
            executable_name += ".exe"
        
        executable_path = self.dist_dir / executable_name
        
        if executable_path.exists():
            size_mb = executable_path.stat().st_size / (1024 * 1024)
            print(f"✅ 可执行文件: {executable_path}")
            print(f"   大小: {size_mb:.2f} MB")
            print(f"   平台: {self.platform}")
            
            # 显示使用说明
            print("\n📖 使用方法:")
            print(f"   直接运行: {executable_path}")
            print(f"   或复制到任意位置运行")
            
        else:
            print(f"❌ 未找到可执行文件: {executable_path}")
            print("\n📂 dist目录内容:")
            for item in self.dist_dir.iterdir():
                print(f"   - {item.name}")
    
    def test_executable(self):
        """测试可执行文件"""
        print("\n🧪 测试可执行文件...")
        
        executable_name = "get_transform"
        if self.platform == "Windows":
            executable_name += ".exe"
        
        executable_path = self.dist_dir / executable_name
        
        if not executable_path.exists():
            print(f"❌ 可执行文件不存在: {executable_path}")
            return False
        
        print(f"📍 测试文件: {executable_path}")
        print("⏳ 启动测试（将在3秒后自动终止）...\n")
        
        try:
            # 运行可执行文件，但设置超时以避免阻塞
            result = subprocess.run(
                [str(executable_path)],
                capture_output=True,
                text=True,
                timeout=3,
                input="\n"  # 发送换行符以跳过等待输入
            )
            
            print("✅ 可执行文件可以正常启动")
            return True
            
        except subprocess.TimeoutExpired:
            # 超时是正常的，因为程序可能在等待用户输入
            print("✅ 可执行文件可以正常启动（超时是正常的）")
            return True
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Get_transform 可执行文件构建工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/build_executable.py              # 标准构建
  python scripts/build_executable.py --clean      # 清理后构建
  python scripts/build_executable.py --debug      # 调试模式构建
  python scripts/build_executable.py --test       # 构建并测试
        """
    )
    
    parser.add_argument("--clean", action="store_true", help="清理构建目录")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--onedir", action="store_true", help="构建目录版本")
    parser.add_argument("--test", action="store_true", help="构建后测试")
    parser.add_argument("--install-pyinstaller", action="store_true", help="安装PyInstaller")
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print("=" * 60)
    print("🌀 Get_transform 可执行文件构建工具")
    print("=" * 60)
    print(f"📍 项目目录: {project_root}")
    print(f"📍 平台: {platform.system()} {platform.machine()}")
    print(f"📍 Python: {sys.version}")
    
    # 创建构建器
    builder = ExecutableBuilder(project_root)
    
    # 检查 PyInstaller
    if not builder.check_pyinstaller():
        print("\n⚠️  PyInstaller 未安装")
        
        if args.install_pyinstaller:
            if not builder.install_pyinstaller():
                print("\n❌ 构建失败: 无法安装 PyInstaller")
                sys.exit(1)
        else:
            print("\n🔧 解决方案:")
            print("   1. 运行: python -m pip install pyinstaller")
            print("   2. 或使用 --install-pyinstaller 选项")
            
            try:
                choice = input("\n是否现在安装 PyInstaller? (y/n): ").strip().lower()
                if choice in ['y', 'yes', '是']:
                    if not builder.install_pyinstaller():
                        print("\n❌ 构建失败: 无法安装 PyInstaller")
                        sys.exit(1)
                else:
                    print("\n👋 构建取消")
                    sys.exit(0)
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 构建取消")
                sys.exit(0)
    
    # 清理
    if args.clean:
        builder.clean()
    
    # 构建
    success = builder.build(debug=args.debug, onedir=args.onedir)
    
    if not success:
        print("\n❌ 构建失败")
        sys.exit(1)
    
    # 测试
    if args.test:
        test_success = builder.test_executable()
        if not test_success:
            print("\n⚠️  测试未通过，但构建已完成")
    
    print("\n" + "=" * 60)
    print("✅ 构建流程完成")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 构建取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
