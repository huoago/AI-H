import os
import shutil
from pathlib import Path
import PyInstaller.__main__
import subprocess
import zipfile

class ReleaseBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.release_dir = self.root_dir / 'release'
        self.version = '0.1.0'
        
    def clean_dirs(self):
        """清理旧的构建目录"""
        dirs_to_clean = ['build', 'dist', 'release']
        for dir_name in dirs_to_clean:
            dir_path = self.root_dir / dir_name
            if dir_path.exists():
                shutil.rmtree(dir_path)
                
    def create_dirs(self):
        """创建必要的目录"""
        dirs_to_create = [
            self.release_dir,
            self.release_dir / 'installer',
            self.release_dir / 'portable',
            self.release_dir / 'docs',
            self.release_dir / 'portable/config',
            self.release_dir / 'portable/templates',
            self.release_dir / 'portable/models',
        ]
        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def build_exe(self):
        """构建exe文件"""
        print("正在构建exe文件...")
        PyInstaller.__main__.run([
            'ai_article_generator/main.py',
            '--name=AI文章生成助手',
            '--windowed',
            '--icon=resources/icon.ico',
            '--add-data=ai_article_generator/config;config',
            '--add-data=ai_article_generator/templates;templates',
            '--hidden-import=torch',
            '--hidden-import=transformers',
            '--hidden-import=pytesseract',
            '--hidden-import=pdfplumber',
            '--hidden-import=PIL',
            '--hidden-import=docx',
            '--hidden-import=openpyxl',
            '--hidden-import=markdown',
            '--hidden-import=pptx',
            '--hidden-import=bs4',
            '--noconfirm',
            '--clean',
            '--onefile',
        ])
        
    def build_installer(self):
        """构建安装程序"""
        print("正在构建安装程序...")
        inno_script = self.root_dir / 'installer.iss'
        subprocess.run([
            'C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe',
            str(inno_script)
        ], check=True)
        
    def copy_files(self):
        """复制文件到发布目录"""
        print("正在复制文件...")
        
        # 复制可执行文件
        shutil.copy2(
            self.root_dir / 'dist/AI文章生成助手.exe',
            self.release_dir / 'portable/AI文章生成助手.exe'
        )
        
        # 复制安装程序
        shutil.copy2(
            self.root_dir / 'installer/AI文章生成助手_安装程序_v0.1.0.exe',
            self.release_dir / 'installer'
        )
        
        # 复制文档
        shutil.copy2(self.root_dir / 'LICENSE', self.release_dir)
        shutil.copy2(self.root_dir / 'README.md', self.release_dir)
        
        # 复制配置文件和模板
        self._copy_dir('ai_article_generator/config', 'portable/config')
        self._copy_dir('ai_article_generator/templates', 'portable/templates')
        
    def _copy_dir(self, src, dst):
        """复制目录"""
        src_path = self.root_dir / src
        dst_path = self.release_dir / dst
        if src_path.exists():
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            
    def create_docs(self):
        """创建文档"""
        print("正在生成文档...")
        docs = {
            '使用说明.md': """
# AI文章生成助手使用说明

## 1. 安装说明
1. 运行安装程序
2. 按提示完成安装
3. 首次运行时会自动下载必要的模型

## 2. 使用方法
1. 启动程序
2. 选择要处理的文件
3. 选择输出模板
4. 点击生成按钮

## 3. 注意事项
- 确保网络连接正常
- 首次使用需要下载模型
- 建议使用清晰的原始文件
            """,
            
            '常见问题.md': """
# 常见问题解答

## 1. 程序无法启动
- 检查是否已安装所有依赖
- 确认Tesseract-OCR已正确安装
- 查看日志文件了解详细错误信息

## 2. 模型下载失败
- 检查网络连接
- 尝试使用代理
- 手动下载模型文件

## 3. 文字识别不准确
- 确保原始文件清晰
- 调整图片亮度和对比度
- 使用更高质量的扫描件
            """
        }
        
        for filename, content in docs.items():
            md_path = self.release_dir / 'docs' / filename
            pdf_path = md_path.with_suffix('.pdf')
            
            # 保存Markdown文件
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # TODO: 转换为PDF（需要安装额外工具）
            
    def create_portable_zip(self):
        """创建便携版压缩包"""
        print("正在创建便携版压缩包...")
        zip_path = self.release_dir / f'AI文章生成助手_便携版_v{self.version}.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(self.release_dir / 'portable'):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(self.release_dir / 'portable')
                    zf.write(file_path, arc_name)
                    
    def build(self):
        """构建完整发布包"""
        try:
            print("开始构建发布包...")
            self.clean_dirs()
            self.create_dirs()
            self.build_exe()
            self.build_installer()
            self.copy_files()
            self.create_docs()
            self.create_portable_zip()
            print("发布包构建完成！")
        except Exception as e:
            print(f"构建失败: {str(e)}")

if __name__ == '__main__':
    builder = ReleaseBuilder()
    builder.build() 