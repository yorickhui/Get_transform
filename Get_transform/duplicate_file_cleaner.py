#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文件对比和清理工具
用于对比history文件夹下的不同时间版本，删除最新版本中与旧版本重复的文件
并将最新版本的HTML文件复制到new目录并重命名

作者: AI Assistant
创建时间: 2025-01-27
更新时间: 2025-01-27
"""

import os
import re
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Set
from bs4 import BeautifulSoup

class DuplicateFileCleaner:
    def __init__(self, history_dir: str, new_dir: str = None):
        """
        初始化文件清理器
        
        Args:
            history_dir: history目录的路径
            new_dir: 复制文件的目标目录，默认为history目录同级的new目录
        """
        self.history_dir = Path(history_dir)
        self.new_dir = Path(new_dir) if new_dir else self.history_dir.parent / "new"
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志记录"""
        log_file = self.history_dir.parent / f"file_cleaner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"日志文件创建: {log_file}")
    
    def extract_timestamp_from_folder(self, folder_name: str) -> str:
        """
        从文件夹名称中提取时间戳
        
        Args:
            folder_name: 文件夹名称，如 'voicenotes_202510171604_getnotes_archive_...'
            
        Returns:
            时间戳字符串，如 '202510171604'，如果未找到则返回空字符串
        """
        # 匹配模式：voicenotes_后跟12位数字（YYYYMMDDHHMM）
        pattern = r'voicenotes_(\d{12})_'
        match = re.search(pattern, folder_name)
        return match.group(1) if match else ""
    
    def get_sorted_folders(self) -> List[Tuple[str, str]]:
        """
        获取按时间戳排序的文件夹列表
        
        Returns:
            [(时间戳, 文件夹路径), ...] 按时间戳升序排列
        """
        folders = []
        
        if not self.history_dir.exists():
            self.logger.error(f"History目录不存在: {self.history_dir}")
            return folders
        
        for item in self.history_dir.iterdir():
            if item.is_dir():
                timestamp = self.extract_timestamp_from_folder(item.name)
                if timestamp:
                    folders.append((timestamp, str(item)))
                    self.logger.info(f"发现文件夹: {item.name} (时间戳: {timestamp})")
                else:
                    self.logger.warning(f"无法解析时间戳的文件夹: {item.name}")
        
        # 按时间戳排序（升序，最新的在最后）
        folders.sort(key=lambda x: x[0])
        return folders
    
    def get_files_in_notes(self, folder_path: str) -> Set[str]:
        """
        获取指定文件夹notes目录下的所有文件名
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            文件名集合
        """
        notes_dir = Path(folder_path) / "notes"
        files = set()
        
        if not notes_dir.exists():
            self.logger.warning(f"Notes目录不存在: {notes_dir}")
            return files
        
        for file_path in notes_dir.iterdir():
            if file_path.is_file():
                files.add(file_path.name)
        
        self.logger.info(f"在 {notes_dir} 中找到 {len(files)} 个文件")
        return files
    
    def parse_index_html(self, folder_path: str) -> Dict[str, str]:
        """
        解析index.html文件，提取文件名与笔记标题的映射关系
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            {文件名: 笔记标题} 的字典
        """
        index_file = Path(folder_path) / "index.html"
        file_title_map = {}
        
        if not index_file.exists():
            self.logger.warning(f"index.html文件不存在: {index_file}")
            return file_title_map
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找所有指向notes目录的链接
            links = soup.find_all('a', href=re.compile(r'notes/.*\.html'))
            
            for link in links:
                href = link.get('href')
                title = link.get_text(strip=True)
                
                if href and title:
                    # 提取文件名（去掉notes/前缀）
                    filename = href.replace('notes/', '')
                    file_title_map[filename] = title
            
            self.logger.info(f"从index.html解析出 {len(file_title_map)} 个文件标题映射")
            
        except Exception as e:
            self.logger.error(f"解析index.html失败: {e}")
        
        return file_title_map
    
    def sanitize_filename(self, title: str) -> str:
        """
        清理文件名，移除不合法的字符
        
        Args:
            title: 原始标题
            
        Returns:
            清理后的文件名
        """
        # 移除或替换不合法的文件名字符
        illegal_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(illegal_chars, '_', title)
        
        # 移除多余的空格和点
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        sanitized = sanitized.replace('..', '.')
        
        # 限制文件名长度
        if len(sanitized) > 200:
            sanitized = sanitized[:200]
        
        return sanitized
    
    def copy_and_rename_files(self, folder_path: str, dry_run: bool = True) -> Dict[str, any]:
        """
        复制notes目录中的HTML文件到new目录并根据标题重命名
        
        Args:
            folder_path: 源文件夹路径
            dry_run: 是否为试运行模式
            
        Returns:
            操作结果字典
        """
        self.logger.info("开始复制和重命名文件...")
        
        # 解析index.html获取文件名与标题的映射
        file_title_map = self.parse_index_html(folder_path)
        
        if not file_title_map:
            return {"success": False, "message": "未找到文件标题映射"}
        
        notes_dir = Path(folder_path) / "notes"
        if not notes_dir.exists():
            return {"success": False, "message": "notes目录不存在"}
        
        # 确保目标目录存在
        if not dry_run:
            self.new_dir.mkdir(parents=True, exist_ok=True)
        
        copied_count = 0
        skipped_count = 0
        error_count = 0
        
        for filename, title in file_title_map.items():
            source_file = notes_dir / filename
            
            if not source_file.exists():
                self.logger.warning(f"源文件不存在: {source_file}")
                skipped_count += 1
                continue
            
            # 生成新文件名
            sanitized_title = self.sanitize_filename(title)
            new_filename = f"{sanitized_title}.html"
            target_file = self.new_dir / new_filename
            
            # 处理重名文件
            counter = 1
            original_target = target_file
            while target_file.exists() and not dry_run:
                name_part = original_target.stem
                target_file = self.new_dir / f"{name_part}_{counter}.html"
                counter += 1
            
            if dry_run:
                self.logger.info(f"[试运行] 将复制: {source_file} -> {target_file}")
            else:
                try:
                    shutil.copy2(source_file, target_file)
                    self.logger.info(f"已复制: {filename} -> {new_filename}")
                    copied_count += 1
                except Exception as e:
                    self.logger.error(f"复制文件失败 {source_file} -> {target_file}: {e}")
                    error_count += 1
        
        result = {
            "success": True,
            "message": "文件复制和重命名完成",
            "total_files": len(file_title_map),
            "copied_count": copied_count,
            "skipped_count": skipped_count,
            "error_count": error_count,
            "target_dir": str(self.new_dir),
            "dry_run": dry_run
        }
        
        self.logger.info(f"文件复制结果 - 总数: {len(file_title_map)}, 复制: {copied_count}, 跳过: {skipped_count}, 错误: {error_count}")
        
        return result
    
    def copy_unique_files_from_multiple_folders(self, folder1: str, folder2: str, dry_run: bool = True) -> Dict[str, any]:
        """
        从两个文件夹中复制独有文件到new目录并重命名
        
        Args:
            folder1: 第一个文件夹路径
            folder2: 第二个文件夹路径
            dry_run: 是否为试运行模式
            
        Returns:
            操作结果字典
        """
        self.logger.info("开始从多个文件夹复制独有文件...")
        
        # 找出两个文件夹中的独有文件
        unique_in_folder1, unique_in_folder2 = self.find_unique_files(folder1, folder2)
        
        # 解析两个文件夹的index.html获取文件名与标题的映射
        file_title_map1 = self.parse_index_html(folder1)
        file_title_map2 = self.parse_index_html(folder2)
        
        if not file_title_map1 and not file_title_map2:
            return {"success": False, "message": "未找到任何文件标题映射"}
        
        # 确保目标目录存在
        if not dry_run:
            self.new_dir.mkdir(parents=True, exist_ok=True)
        
        copied_count = 0
        skipped_count = 0
        error_count = 0
        
        # 复制第一个文件夹中的独有文件
        if file_title_map1:
            self.logger.info(f"复制 {Path(folder1).name} 中的独有文件...")
            notes_dir1 = Path(folder1) / "notes"
            
            for filename in unique_in_folder1:
                if filename in file_title_map1:
                    title = file_title_map1[filename]
                    source_file = notes_dir1 / filename
                    
                    if not source_file.exists():
                        self.logger.warning(f"源文件不存在: {source_file}")
                        skipped_count += 1
                        continue
                    
                    # 生成新文件名
                    safe_title = self.sanitize_filename(title)
                    new_filename = f"{safe_title}.html"
                    target_file = self.new_dir / new_filename
                    
                    # 处理文件名冲突
                    counter = 1
                    while target_file.exists() and not dry_run:
                        new_filename = f"{safe_title}_{counter}.html"
                        target_file = self.new_dir / new_filename
                        counter += 1
                    
                    if dry_run:
                        self.logger.info(f"[试运行] 将复制: {source_file} -> {target_file}")
                    else:
                        try:
                            shutil.copy2(source_file, target_file)
                            self.logger.info(f"已复制: {source_file} -> {target_file}")
                            copied_count += 1
                        except Exception as e:
                            self.logger.error(f"复制文件失败 {source_file}: {e}")
                            error_count += 1
                else:
                    self.logger.warning(f"文件 {filename} 在标题映射中未找到")
                    skipped_count += 1
        
        # 复制第二个文件夹中的独有文件
        if file_title_map2:
            self.logger.info(f"复制 {Path(folder2).name} 中的独有文件...")
            notes_dir2 = Path(folder2) / "notes"
            
            for filename in unique_in_folder2:
                if filename in file_title_map2:
                    title = file_title_map2[filename]
                    source_file = notes_dir2 / filename
                    
                    if not source_file.exists():
                        self.logger.warning(f"源文件不存在: {source_file}")
                        skipped_count += 1
                        continue
                    
                    # 生成新文件名
                    safe_title = self.sanitize_filename(title)
                    new_filename = f"{safe_title}.html"
                    target_file = self.new_dir / new_filename
                    
                    # 处理文件名冲突
                    counter = 1
                    while target_file.exists() and not dry_run:
                        new_filename = f"{safe_title}_{counter}.html"
                        target_file = self.new_dir / new_filename
                        counter += 1
                    
                    if dry_run:
                        self.logger.info(f"[试运行] 将复制: {source_file} -> {target_file}")
                    else:
                        try:
                            shutil.copy2(source_file, target_file)
                            self.logger.info(f"已复制: {source_file} -> {target_file}")
                            copied_count += 1
                        except Exception as e:
                            self.logger.error(f"复制文件失败 {source_file}: {e}")
                            error_count += 1
                else:
                    self.logger.warning(f"文件 {filename} 在标题映射中未找到")
                    skipped_count += 1
        
        total_unique_files = len(unique_in_folder1) + len(unique_in_folder2)
        
        self.logger.info(f"独有文件复制完成: 复制 {copied_count} 个，跳过 {skipped_count} 个，错误 {error_count} 个")
        
        return {
            "success": True,
            "message": f"独有文件复制操作完成",
            "copied_count": copied_count,
            "skipped_count": skipped_count,
            "error_count": error_count,
            "target_dir": str(self.new_dir),
            "total_files": total_unique_files,
            "unique_in_folder1": len(unique_in_folder1),
            "unique_in_folder2": len(unique_in_folder2)
        }
    
    def find_duplicate_files(self, newer_folder: str, older_folders: List[str]) -> Set[str]:
        """
        找出新文件夹中与旧文件夹重复的文件
        
        Args:
            newer_folder: 最新文件夹路径
            older_folders: 旧文件夹路径列表
            
        Returns:
            重复文件名集合
        """
        newer_files = self.get_files_in_notes(newer_folder)
        duplicate_files = set()
        
        for older_folder in older_folders:
            older_files = self.get_files_in_notes(older_folder)
            duplicates = newer_files.intersection(older_files)
            duplicate_files.update(duplicates)
            
            if duplicates:
                self.logger.info(f"与 {Path(older_folder).name} 重复的文件数量: {len(duplicates)}")
        
        return duplicate_files
    
    def find_unique_files(self, folder1: str, folder2: str) -> Tuple[Set[str], Set[str]]:
        """
        找出两个文件夹中的独有文件
        
        Args:
            folder1: 第一个文件夹路径
            folder2: 第二个文件夹路径
            
        Returns:
            (folder1独有文件集合, folder2独有文件集合)
        """
        files1 = self.get_files_in_notes(folder1)
        files2 = self.get_files_in_notes(folder2)
        
        # 找出各自独有的文件
        unique_in_folder1 = files1 - files2
        unique_in_folder2 = files2 - files1
        
        self.logger.info(f"{Path(folder1).name} 中独有文件数量: {len(unique_in_folder1)}")
        self.logger.info(f"{Path(folder2).name} 中独有文件数量: {len(unique_in_folder2)}")
        
        return unique_in_folder1, unique_in_folder2
    
    def delete_duplicate_files(self, folder_path: str, duplicate_files: Set[str], dry_run: bool = True) -> int:
        """
        删除重复文件
        
        Args:
            folder_path: 文件夹路径
            duplicate_files: 要删除的文件名集合
            dry_run: 是否为试运行模式（不实际删除）
            
        Returns:
            删除的文件数量
        """
        notes_dir = Path(folder_path) / "notes"
        deleted_count = 0
        
        for filename in duplicate_files:
            file_path = notes_dir / filename
            if file_path.exists():
                if dry_run:
                    self.logger.info(f"[试运行] 将删除: {file_path}")
                else:
                    try:
                        file_path.unlink()
                        self.logger.info(f"已删除: {file_path}")
                        deleted_count += 1
                    except Exception as e:
                        self.logger.error(f"删除文件失败 {file_path}: {e}")
            else:
                self.logger.warning(f"文件不存在: {file_path}")
        
        return deleted_count
    
    def create_backup(self, folder_path: str) -> str:
        """
        创建文件夹备份
        
        Args:
            folder_path: 要备份的文件夹路径
            
        Returns:
            备份文件夹路径
        """
        folder_path = Path(folder_path)
        backup_name = f"{folder_path.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = folder_path.parent / backup_name
        
        try:
            shutil.copytree(folder_path, backup_path)
            self.logger.info(f"备份创建成功: {backup_path}")
            return str(backup_path)
        except Exception as e:
            self.logger.error(f"创建备份失败: {e}")
            raise
    
    def run_cleanup(self, dry_run: bool = True, copy_files: bool = True) -> Dict[str, any]:
        """
        执行清理操作
        
        Args:
            dry_run: 是否为试运行模式
            copy_files: 是否复制和重命名文件到new目录
            
        Returns:
            操作结果字典
        """
        self.logger.info("=" * 50)
        self.logger.info("开始执行文件清理操作")
        self.logger.info("=" * 50)
        
        # 获取排序后的文件夹列表
        folders = self.get_sorted_folders()
        
        if len(folders) == 0:
            self.logger.error("未找到任何有效文件夹")
            return {"success": False, "message": "未找到任何有效文件夹"}
        
        # 根据文件夹数量决定处理逻辑
        backup_path = None  # 初始化backup_path变量
        
        if len(folders) == 1:
            # 只有一个文件夹，复制所有文件
            self.logger.info("检测到只有一个文件夹，将复制所有文件")
            timestamp, folder_path = folders[0]
            self.logger.info(f"处理文件夹: {Path(folder_path).name} (时间戳: {timestamp})")
            
            # 直接复制所有文件，无需删除重复文件
            duplicate_files = set()  # 空集合，表示没有重复文件需要删除
            newest_folder = folder_path
            
        else:
            # 多个文件夹，直接对比最新的2个文件夹，找出独有文件
            self.logger.info(f"检测到{len(folders)}个文件夹，将对比最新的2个文件夹")
            
            # 取最新的2个文件夹
            if len(folders) >= 2:
                newest_timestamp, newest_folder = folders[-1]
                second_newest_timestamp, second_newest_folder = folders[-2]
                
                self.logger.info(f"最新文件夹: {Path(newest_folder).name} (时间戳: {newest_timestamp})")
                self.logger.info(f"对比文件夹: {Path(second_newest_folder).name} (时间戳: {second_newest_timestamp})")
                
                # 存储两个文件夹路径，用于后续的独有文件复制
                folder1 = newest_folder
                folder2 = second_newest_folder
                
            else:
                # 这种情况理论上不会发生，因为上面已经检查了len(folders) == 1
                newest_timestamp, newest_folder = folders[-1]
                self.logger.info(f"最新文件夹: {Path(newest_folder).name} (时间戳: {newest_timestamp})")
                folder1 = newest_folder
                folder2 = None
            
            # 多文件夹模式不需要删除重复文件，只需要复制独有文件
            duplicate_files = set()  # 空集合，表示不删除任何文件
        
        # 在新的逻辑下，不删除任何重复文件，只复制独有文件
        deleted_count = 0
        if len(folders) == 1:
            self.logger.info("单文件夹模式，跳过重复文件删除步骤")
        else:
            self.logger.info("多文件夹模式，跳过重复文件删除步骤（只复制独有文件）")
        
        # 复制和重命名文件到new目录
        copy_result = None
        if copy_files:
            self.logger.info("=" * 30)
            if len(folders) == 1:
                # 单文件夹模式：复制所有文件
                copy_result = self.copy_and_rename_files(newest_folder, dry_run)
            else:
                # 多文件夹模式：复制独有文件
                if folder2 is not None:
                    copy_result = self.copy_unique_files_from_multiple_folders(folder1, folder2, dry_run)
                else:
                    # 如果只有一个文件夹，回退到单文件夹模式
                    copy_result = self.copy_and_rename_files(folder1, dry_run)
            self.logger.info("=" * 30)
        
        result = {
            "success": True,
            "message": "清理操作完成",
            "newest_folder": newest_folder,
            "duplicate_count": len(duplicate_files),
            "deleted_count": deleted_count,
            "backup_path": backup_path,
            "copy_result": copy_result,
            "dry_run": dry_run
        }
        
        self.logger.info("=" * 50)
        self.logger.info("清理操作完成")
        self.logger.info(f"重复文件数量: {len(duplicate_files)}")
        self.logger.info(f"删除文件数量: {deleted_count}")
        if copy_result:
            self.logger.info(f"复制文件数量: {copy_result.get('copied_count', 0)}")
            self.logger.info(f"目标目录: {copy_result.get('target_dir', '')}")
        if backup_path:
            self.logger.info(f"备份路径: {backup_path}")
        self.logger.info("=" * 50)
        
        return result


def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    
    # 配置相对路径
    history_dir = script_dir / "history"
    new_dir = script_dir / "new"
    
    # 检查history目录是否存在
    if not history_dir.exists():
        print(f"错误: 未找到history目录: {history_dir}")
        print(f"请确保在包含history文件夹的目录中运行此脚本")
        return
    
    # 创建清理器实例
    cleaner = DuplicateFileCleaner(str(history_dir), str(new_dir))
    
    print("智能文件清理和复制工具")
    print("=" * 60)
    print("此工具将根据文件夹数量自动选择处理模式:")
    print("• 单文件夹模式: 复制所有文件到new目录并重命名")
    print("• 多文件夹模式: 对比最新2个文件夹，删除重复文件并复制独有文件")
    print("• 所有HTML文件都会根据标题重命名为有意义的文件名")
    print("建议先运行试运行模式查看将要执行的操作")
    print("=" * 60)
    
    while True:
        print("\n请选择操作:")
        print("1. 试运行 (查看将要执行的操作，不实际执行)")
        print("2. 正式运行 (根据文件夹数量自动选择处理模式)")
        print("3. 仅复制重命名 (跳过重复文件删除，仅复制重命名)")
        print("4. 退出")
        
        choice = input("请输入选择 (1-4): ").strip()
        
        if choice == "1":
            print("\n执行试运行...")
            result = cleaner.run_cleanup(dry_run=True, copy_files=True)
            print(f"\n试运行结果: {result['message']}")
            print(f"发现重复文件: {result['duplicate_count']} 个")
            if result.get('copy_result'):
                copy_result = result['copy_result']
                print(f"将复制文件: {copy_result.get('total_files', 0)} 个")
                print(f"目标目录: {copy_result.get('target_dir', '')}")
            
        elif choice == "2":
            try:
                confirm = input("是否执行? (y/n): ").strip().lower()
            except EOFError:
                confirm = 'y'  # 默认执行
            execute_operation = confirm in ['y', 'yes', '是']
            
            if execute_operation:
                print("\n执行正式操作...")
                result = cleaner.run_cleanup(dry_run=False, copy_files=True)
                print(f"\n操作结果: {result['message']}")
                print(f"删除文件数量: {result['deleted_count']} 个")
                if result.get('copy_result'):
                    copy_result = result['copy_result']
                    print(f"复制文件数量: {copy_result.get('copied_count', 0)} 个")
                    print(f"目标目录: {copy_result.get('target_dir', '')}")
            else:
                print("操作已取消")
                
        elif choice == "3":
            print("\n执行仅复制重命名操作...")
            try:
                confirm = input("确认执行复制操作? (y/n): ").strip().lower()
            except EOFError:
                confirm = 'y'  # 自动确认
            if confirm in ['y', 'yes', '是']:
                # 获取文件夹列表并选择最新的
                folders = cleaner.get_sorted_folders()
                if folders:
                    if len(folders) == 1:
                        print("检测到单文件夹模式，将复制所有文件")
                        newest_folder = folders[0][1]
                    else:
                        print(f"检测到多文件夹模式，将复制最新文件夹中的文件")
                        newest_folder = folders[-1][1]
                    
                    print(f"处理文件夹: {Path(newest_folder).name}")
                    result = cleaner.copy_and_rename_files(newest_folder, dry_run=False)
                    print(f"\n操作结果: {result['message']}")
                    print(f"复制文件数量: {result.get('copied_count', 0)} 个")
                    print(f"目标目录: {result.get('target_dir', '')}")
                else:
                    print("未找到有效的文件夹")
            else:
                print("操作已取消")
                
        elif choice == "4":
            print("退出程序")
            break
            
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()