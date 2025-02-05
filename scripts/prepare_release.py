import os
import re
from datetime import datetime

def update_version(version):
    """更新版本号"""
    # 更新 setup.py
    with open('setup.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(
        r'version=["\']\d+\.\d+\.\d+["\']',
        f'version="{version}"',
        content
    )
    
    with open('setup.py', 'w', encoding='utf-8') as f:
        f.write(content)

def create_changelog(version):
    """创建更新日志"""
    date = datetime.now().strftime('%Y-%m-%d')
    changelog = f"""# {version} ({date})

## 新特性
- 

## 改进
- 

## 修复
- 

"""
    
    changelog_path = 'CHANGELOG.md'
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
        changelog += old_content
    
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog)

def main():
    version = input('请输入新版本号 (例如: 1.0.0): ').strip()
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print('版本号格式错误！')
        return
    
    # 更新版本号
    update_version(version)
    
    # 创建更新日志
    create_changelog(version)
    
    print(f'\n版本 {version} 准备就绪！')
    print('请执行以下命令：')
    print(f'git add .')
    print(f'git commit -m "Release version {version}"')
    print(f'git tag v{version}')
    print(f'git push origin main v{version}')

if __name__ == '__main__':
    main() 