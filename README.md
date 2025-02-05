# AI文章生成助手

![Build Status](https://github.com/yourusername/ai-article-generator/workflows/Build%20and%20Release/badge.svg)
![Tests](https://github.com/yourusername/ai-article-generator/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/yourusername/ai-article-generator/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/ai-article-generator)

## 简介
AI文章生成助手是一个基于Python开发的智能文章生成工具，可以将输入文本转换为不同风格的文章。

## 功能特点
- 支持多种文件格式输入（TXT、PDF、图片等）
- 内置多种文章模板（新闻、博客、论文）
- 智能文本处理和生成
- 简洁直观的用户界面
- OCR图片文字识别

## 系统要求
- Windows 7/8/10/11
- Python 3.8 或更高版本
- 2GB 以上内存
- 500MB 磁盘空间

## 安装说明
1. 安装 Python 环境
2. 安装依赖包：
```bash
pip install -r requirements.txt
```

## 快速开始
1. 直接运行程序：
```bash
python src/run.py
```

2. 或构建可执行文件：
```bash
build_release.bat
```

## 使用方法
1. 启动程序
2. 选择或拖拽文件到程序窗口
3. 选择目标文章模板
4. 点击"生成"按钮
5. 等待生成完成

## 注意事项
- 首次运行会下载必要的模型文件
- 图片文字识别需要安装 Tesseract-OCR
- 建议输入文本长度不超过2000字

## 问题反馈
如遇问题，请提交 Issue 或发送邮件至：support@example.com

## 开源协议
MIT License 