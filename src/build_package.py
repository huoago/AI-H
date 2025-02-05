import os
import shutil
from pathlib import Path
import subprocess
import zipfile
import json

class PackageBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.dist_dir = self.root_dir / 'dist'
        self.release_dir = self.root_dir / 'release'
        self.version = '0.1.0'
        
    def clean_dirs(self):
        """清理旧的构建目录"""
        for dir_path in [self.dist_dir, self.release_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                
    def create_dirs(self):
        """创建必要的目录结构"""
        dirs = [
            self.release_dir,
            self.release_dir / 'installer',
            self.release_dir / 'portable',
            self.release_dir / 'docs',
            self.release_dir / 'models',
            self.release_dir / 'templates'
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def build_exe(self):
        """构建可执行文件"""
        print("正在构建可执行文件...")
        subprocess.run([
            'pyinstaller',
            '--name=AI文章生成助手',
            '--windowed',
            '--icon=resources/icon.ico',
            '--add-data=ai_article_generator/config;config',
            '--add-data=ai_article_generator/templates;templates',
            '--hidden-import=torch',
            '--hidden-import=transformers',
            '--noconfirm',
            '--clean',
            '--onefile',
            'ai_article_generator/main.py'
        ], check=True)
        
    def create_installer(self):
        """创建安装程序"""
        print("正在创建安装程序...")
        subprocess.run([
            'iscc',
            'installer.iss'
        ], check=True)
        
    def copy_files(self):
        """复制文件到发布目录"""
        print("正在复制文件...")
        
        # 复制可执行文件
        shutil.copy2(
            self.dist_dir / 'AI文章生成助手.exe',
            self.release_dir / 'portable'
        )
        
        # 复制安装程序
        shutil.copy2(
            self.dist_dir / 'installer' / f'AI文章生成助手_安装程序_v{self.version}.exe',
            self.release_dir / 'installer'
        )
        
        # 复制文档
        self.create_docs()
        
        # 复制模型和模板
        self._copy_resources()
        
    def create_docs(self):
        """创建文档"""
        docs = {
            'README.md': """
# AI文章生成助手

## 简介
AI文章生成助手是一个基于人工智能的文章生成工具，支持多种文件格式的处理。

## 安装说明
1. 运行安装程序 `AI文章生成助手_安装程序_v0.1.0.exe`
2. 按照提示完成安装
3. 从开始菜单启动程序

## 使用方法
1. 选择输入文件
2. 选择生成模板
3. 点击生成按钮
4. 保存生成的文章

## 系统要求
- Windows 10/11 64位
- 4GB以上内存
- 2GB可用磁盘空间
""",
            '使用说明.md': """
# 使用说明

## 基本操作
1. 文件处理
2. 模板选择
3. 参数设置
4. 生成控制

## 常见问题
1. 如何选择合适的模板
2. 如何调整生成参数
3. 如何处理特殊格式

## 注意事项
- 建议使用清晰的原始文件
- 定期备份重要数据
- 遵守相关法律法规
"""
        }
        
        for filename, content in docs.items():
            file_path = self.release_dir / 'docs' / filename
            file_path.write_text(content.strip(), encoding='utf-8')
            
    def _copy_resources(self):
        """复制资源文件"""
        # 复制模板
        templates_src = self.root_dir / 'ai_article_generator/templates'
        if templates_src.exists():
            shutil.copytree(
                templates_src,
                self.release_dir / 'templates',
                dirs_exist_ok=True
            )
            
        # 复制模型（如果存在）
        models_src = self.root_dir / 'models'
        if models_src.exists():
            shutil.copytree(
                models_src,
                self.release_dir / 'models',
                dirs_exist_ok=True
            )
            
    def create_portable(self):
        """创建便携版"""
        print("正在创建便携版...")
        portable_dir = self.release_dir / 'portable'
        
        # 创建配置文件
        config = {
            'version': self.version,
            'portable': True,
            'first_run': True
        }
        
        config_path = portable_dir / 'config.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
            
        # 创建便携版压缩包
        zip_path = self.release_dir / f'AI文章生成助手_便携版_v{self.version}.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(portable_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(portable_dir)
                    zf.write(file_path, arc_name)
                    
    def build(self):
        """执行完整的构建过程"""
        try:
            print("开始构建发布包...")
            self.clean_dirs()
            self.create_dirs()
            self.build_exe()
            self.create_installer()
            self.copy_files()
            self.create_portable()
            print("发布包构建完成！")
            
        except Exception as e:
            print(f"构建失败: {str(e)}")
            raise

if __name__ == '__main__':
    builder = PackageBuilder()
    builder.build() 