#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录管理和路径检测模块
负责首次运行时的目录结构初始化和GET导出路径的智能检测

作者: AI Assistant
创建时间: 2025-01-27
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from typing import Optional, Tuple, List


class DirectoryManager:
    """目录管理器，负责目录初始化和路径检测"""
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        初始化目录管理器
        
        Args:
            base_dir: 基础目录，默认为脚本所在目录
        """
        if base_dir is None:
            self.base_dir = Path(__file__).parent.absolute()
        else:
            self.base_dir = Path(base_dir).absolute()
        
        self.history_dir = self.base_dir / "history"
        self.new_dir = self.base_dir / "new"
        self.logs_dir = self.base_dir / "logs"
        self.config_file = self.base_dir / "config.json"
        
    def ensure_directories(self) -> List[str]:
        """
        确保必要的目录存在，如果不存在则创建
        
        Returns:
            创建的目录列表
        """
        created_dirs = []
        required_dirs = [
            (self.history_dir, "history"),
            (self.new_dir, "new"),
            (self.logs_dir, "logs")
        ]
        
        for dir_path, dir_name in required_dirs:
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(dir_name)
                    print(f"✅ 创建目录: {dir_name}/")
                except Exception as e:
                    print(f"❌ 创建目录失败 {dir_name}/: {e}")
                    print(f"   请检查目录权限: {dir_path}")
                    raise
        
        if created_dirs:
            print(f"\n📁 已自动创建 {len(created_dirs)} 个目录: {', '.join(created_dirs)}")
        
        return created_dirs
    
    def is_valid_export_folder(self, folder_path: Path) -> bool:
        """
        验证是否为有效的GET导出文件夹
        
        Args:
            folder_path: 要验证的文件夹路径
            
        Returns:
            是否为有效的导出文件夹
        """
        if not folder_path.exists() or not folder_path.is_dir():
            return False
        
        index_file = folder_path / "index.html"
        notes_dir = folder_path / "notes"
        
        return index_file.exists() and notes_dir.exists() and notes_dir.is_dir()
    
    def find_export_folders(self, search_path: Path) -> List[Path]:
        """
        在指定路径下搜索有效的GET导出文件夹
        
        Args:
            search_path: 搜索路径
            
        Returns:
            找到的有效导出文件夹列表
        """
        valid_folders = []
        
        if not search_path.exists() or not search_path.is_dir():
            return valid_folders
        
        # 直接检查当前目录
        if self.is_valid_export_folder(search_path):
            valid_folders.append(search_path)
        
        # 搜索子目录（最多两层）
        for item in search_path.iterdir():
            if item.is_dir() and self.is_valid_export_folder(item):
                valid_folders.append(item)
            elif item.is_dir():
                # 搜索第二层
                for subitem in item.iterdir():
                    if subitem.is_dir() and self.is_valid_export_folder(subitem):
                        valid_folders.append(subitem)
        
        return valid_folders
    
    def extract_zip_if_needed(self, zip_path: Path, extract_to: Path) -> Optional[Path]:
        """
        如果提供的是ZIP文件，则解压并返回解压后的目录
        
        Args:
            zip_path: ZIP文件路径
            extract_to: 解压目标目录
            
        Returns:
            解压后的目录路径，如果失败则返回None
        """
        if not zip_path.exists() or not zipfile.is_zipfile(zip_path):
            return None
        
        try:
            print(f"📦 检测到压缩包，正在解压: {zip_path.name}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"✅ 解压完成: {extract_to}")
            return extract_to
        except Exception as e:
            print(f"❌ 解压失败: {e}")
            return None
    
    def count_export_folders_in_history(self) -> int:
        """
        统计history目录中的导出文件夹数量
        
        Returns:
            导出文件夹数量
        """
        if not self.history_dir.exists():
            return 0
        
        count = 0
        for item in self.history_dir.iterdir():
            if item.is_dir() and self.is_valid_export_folder(item):
                count += 1
        
        return count
    
    def copy_folder_to_history(self, source_folder: Path) -> bool:
        """
        将导出文件夹复制到history目录
        
        Args:
            source_folder: 源文件夹路径
            
        Returns:
            是否复制成功
        """
        if not self.is_valid_export_folder(source_folder):
            print(f"❌ 不是有效的导出文件夹: {source_folder}")
            return False
        
        try:
            target_folder = self.history_dir / source_folder.name
            
            # 检查目标是否已存在
            if target_folder.exists():
                print(f"⚠️  目标文件夹已存在: {target_folder.name}")
                overwrite = input("是否覆盖? (y/n): ").strip().lower()
                if overwrite not in ['y', 'yes', '是']:
                    print("❌ 取消复制操作")
                    return False
                shutil.rmtree(target_folder)
            
            print(f"📋 正在复制文件夹到history目录...")
            shutil.copytree(source_folder, target_folder)
            print(f"✅ 复制成功: {source_folder.name} -> history/{target_folder.name}")
            return True
            
        except Exception as e:
            print(f"❌ 复制失败: {e}")
            return False
    
    def load_config(self) -> dict:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  加载配置文件失败: {e}")
            return {}
    
    def save_config(self, config: dict) -> bool:
        """
        保存配置文件
        
        Args:
            config: 配置字典
            
        Returns:
            是否保存成功
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
            return False
    
    def update_history_path(self, history_path: str) -> bool:
        """
        更新配置中的history路径
        
        Args:
            history_path: history目录路径
            
        Returns:
            是否更新成功
        """
        config = self.load_config()
        config['history_path'] = str(history_path)
        return self.save_config(config)
    
    def guide_user_select_path(self) -> Optional[Path]:
        """
        引导用户选择GET导出所在目录
        
        Returns:
            选定的有效导出文件夹路径，如果取消则返回None
        """
        print("\n" + "=" * 60)
        print("🔍 首次运行检测到 history 目录为空")
        print("=" * 60)
        print("\n请选择GET笔记导出文件的位置:")
        print(f"1. 使用默认路径 (当前目录下的 history/)")
        print(f"2. 输入自定义路径")
        print(f"3. 查看使用说明")
        print(f"4. 退出程序")
        
        while True:
            choice = input("\n请输入选择 (1-4): ").strip()
            
            if choice == "1":
                print(f"\n📂 使用默认路径: {self.history_dir}")
                print("⚠️  请将GET笔记导出文件夹放入该目录后再运行程序")
                return None
                
            elif choice == "2":
                return self._handle_custom_path_input()
                
            elif choice == "3":
                self._show_usage_guide()
                continue
                
            elif choice == "4":
                print("👋 退出程序")
                sys.exit(0)
                
            else:
                print("❌ 无效选择，请输入 1-4")
    
    def _handle_custom_path_input(self) -> Optional[Path]:
        """
        处理用户自定义路径输入
        
        Returns:
            选定的有效导出文件夹路径，如果取消则返回None
        """
        while True:
            print("\n" + "-" * 60)
            path_input = input("请输入GET导出文件夹路径 (或输入 'q' 返回): ").strip()
            
            if path_input.lower() == 'q':
                return None
            
            if not path_input:
                print("❌ 路径不能为空")
                continue
            
            # 去除引号
            path_input = path_input.strip('"').strip("'")
            input_path = Path(path_input)
            
            # 检查路径是否存在
            if not input_path.exists():
                print(f"❌ 路径不存在: {input_path}")
                retry = input("是否重新输入? (y/n): ").strip().lower()
                if retry not in ['y', 'yes', '是']:
                    return None
                continue
            
            # 检查是否为ZIP文件
            if input_path.is_file() and zipfile.is_zipfile(input_path):
                return self._handle_zip_file(input_path)
            
            # 检查是否为有效的导出文件夹
            if self.is_valid_export_folder(input_path):
                print(f"✅ 检测到有效的导出文件夹: {input_path.name}")
                return self._handle_valid_folder(input_path)
            
            # 搜索子目录中的导出文件夹
            print(f"📂 正在搜索导出文件夹...")
            found_folders = self.find_export_folders(input_path)
            
            if not found_folders:
                print(f"❌ 未找到有效的GET导出文件夹")
                print("   有效的导出文件夹应包含:")
                print("   - index.html 文件")
                print("   - notes/ 目录")
                retry = input("\n是否重新输入? (y/n): ").strip().lower()
                if retry not in ['y', 'yes', '是']:
                    return None
                continue
            
            if len(found_folders) == 1:
                print(f"✅ 找到1个导出文件夹: {found_folders[0].name}")
                return self._handle_valid_folder(found_folders[0])
            
            # 多个文件夹，让用户选择
            print(f"\n✅ 找到 {len(found_folders)} 个导出文件夹:")
            for i, folder in enumerate(found_folders, 1):
                print(f"  {i}. {folder.name}")
            
            while True:
                select = input(f"\n请选择要使用的文件夹 (1-{len(found_folders)}) 或输入 'q' 返回: ").strip()
                if select.lower() == 'q':
                    return None
                try:
                    index = int(select) - 1
                    if 0 <= index < len(found_folders):
                        return self._handle_valid_folder(found_folders[index])
                    else:
                        print(f"❌ 请输入 1-{len(found_folders)}")
                except ValueError:
                    print("❌ 请输入有效的数字")
    
    def _handle_zip_file(self, zip_path: Path) -> Optional[Path]:
        """
        处理ZIP压缩包
        
        Args:
            zip_path: ZIP文件路径
            
        Returns:
            解压后的有效导出文件夹路径，如果失败则返回None
        """
        print(f"\n📦 检测到压缩包: {zip_path.name}")
        extract = input("是否解压到临时目录并搜索导出文件夹? (y/n): ").strip().lower()
        
        if extract not in ['y', 'yes', '是']:
            return None
        
        # 创建临时解压目录
        temp_dir = self.base_dir / "temp_extract"
        temp_dir.mkdir(exist_ok=True)
        
        extracted_path = self.extract_zip_if_needed(zip_path, temp_dir)
        if not extracted_path:
            return None
        
        # 搜索解压后的文件夹
        found_folders = self.find_export_folders(extracted_path)
        
        if not found_folders:
            print(f"❌ 压缩包中未找到有效的GET导出文件夹")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return None
        
        if len(found_folders) == 1:
            folder = found_folders[0]
        else:
            print(f"\n✅ 找到 {len(found_folders)} 个导出文件夹:")
            for i, f in enumerate(found_folders, 1):
                print(f"  {i}. {f.name}")
            
            while True:
                select = input(f"\n请选择要使用的文件夹 (1-{len(found_folders)}): ").strip()
                try:
                    index = int(select) - 1
                    if 0 <= index < len(found_folders):
                        folder = found_folders[index]
                        break
                    else:
                        print(f"❌ 请输入 1-{len(found_folders)}")
                except ValueError:
                    print("❌ 请输入有效的数字")
        
        # 复制到history并清理临时目录
        result_folder = self._handle_valid_folder(folder)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return result_folder
    
    def _handle_valid_folder(self, folder_path: Path) -> Optional[Path]:
        """
        处理有效的导出文件夹
        
        Args:
            folder_path: 导出文件夹路径
            
        Returns:
            最终的文件夹路径，如果取消则返回None
        """
        # 如果文件夹已经在history目录中
        if folder_path.parent == self.history_dir:
            print(f"✅ 文件夹已在history目录中")
            return folder_path
        
        # 询问是否复制到history
        print(f"\n📋 是否将文件夹复制到 history 目录?")
        print(f"   源路径: {folder_path}")
        print(f"   目标路径: {self.history_dir / folder_path.name}")
        
        copy_choice = input("复制到history? (y/n): ").strip().lower()
        
        if copy_choice in ['y', 'yes', '是']:
            if self.copy_folder_to_history(folder_path):
                return self.history_dir / folder_path.name
            else:
                return None
        else:
            print("⚠️  未复制到history目录，请手动将文件夹放入history目录")
            return None
    
    def _show_usage_guide(self):
        """显示使用说明"""
        print("\n" + "=" * 60)
        print("📖 GET笔记导出文件使用说明")
        print("=" * 60)
        print("""
1. 导出GET笔记:
   - 在GET笔记App中选择导出功能
   - 导出的文件通常是一个ZIP压缩包或文件夹

2. 有效的导出文件夹结构:
   voicenotes_202510171604_getnotes_archive_xxx/
   ├── index.html          (必需：笔记索引文件)
   └── notes/              (必需：笔记HTML文件目录)
       ├── xxxxx.html
       ├── xxxxx.html
       └── ...

3. 使用本工具:
   - 方式1: 将导出文件夹直接放入 history/ 目录
   - 方式2: 解压ZIP包后，将包含index.html和notes/的文件夹放入history/
   - 方式3: 使用本向导选择导出文件所在位置，工具会自动处理

4. 注意事项:
   - 首次使用时，history/中至少要有一个导出文件夹
   - 导出文件夹名称应包含时间戳 (格式: voicenotes_YYYYMMDDHHMM_...)
   - 不要删除history中的历史版本，以便对比增量
        """)
        print("=" * 60)
    
    def initialize_on_first_run(self) -> bool:
        """
        首次运行初始化流程
        
        Returns:
            是否初始化成功（可以继续运行程序）
        """
        print("\n🔧 正在初始化目录结构...")
        
        # 1. 确保必要目录存在
        created_dirs = self.ensure_directories()
        
        # 2. 检查history目录是否有导出文件夹
        export_count = self.count_export_folders_in_history()
        
        if export_count > 0:
            print(f"✅ history 目录中已有 {export_count} 个导出文件夹")
            return True
        
        # 3. history为空，引导用户
        print("\n⚠️  history 目录为空")
        result_folder = self.guide_user_select_path()
        
        if result_folder:
            print(f"\n✅ 初始化完成，准备就绪")
            return True
        else:
            print("\n⚠️  未选择有效的导出文件夹")
            print("请将GET笔记导出文件夹放入以下目录后再运行程序:")
            print(f"  {self.history_dir}")
            return False


def main():
    """测试函数"""
    manager = DirectoryManager()
    
    print("目录管理器测试")
    print("=" * 60)
    
    # 测试目录初始化
    success = manager.initialize_on_first_run()
    
    if success:
        print("\n✅ 初始化成功，可以继续运行主程序")
    else:
        print("\n❌ 初始化未完成")


if __name__ == "__main__":
    main()
