from setuptools import setup, find_packages
import os

def get_version():
    """获取版本号"""
    version = os.environ.get('GITHUB_REF', '0.0.0')
    if version.startswith('refs/tags/v'):
        version = version[11:]  # 移除 'refs/tags/v' 前缀
    return version

def get_long_description():
    """获取长描述"""
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(
    name="ai-article-generator",
    version=get_version(),
    author="Your Name",
    author_email="your.email@example.com",
    description="AI文章生成助手",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-article-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        line.strip()
        for line in open('requirements.txt', encoding='utf-8')
        if line.strip() and not line.startswith('#')
    ],
    package_data={
        'ai_article_generator': [
            'config/*.json',
            'templates/*.json',
        ],
    },
    entry_points={
        'console_scripts': [
            'ai-article-generator=ai_article_generator.main:main',
        ],
    },
) 