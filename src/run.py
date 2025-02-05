import sys
import os
from pathlib import Path
import logging

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ai_article_generator.utils.init_env import init_project_env
from ai_article_generator.utils.config_manager import ConfigManager
from ai_article_generator.core.article_generator import ArticleGenerator

def setup_logging():
    """设置日志"""
    log_dir = project_root / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def run_app():
    """运行应用程序"""
    try:
        # 设置日志
        setup_logging()
        logging.info("正在启动AI文章生成助手...")
        
        # 初始化环境
        if not init_project_env():
            logging.error("环境初始化失败")
            return False
            
        # 加载配置
        config = ConfigManager()
        logging.info("配置加载成功")
        
        # 创建文章生成器
        generator = ArticleGenerator()
        
        # 简单的命令行界面
        while True:
            print("\n=== AI文章生成助手 ===")
            print("1. 生成文章")
            print("2. 管理模板")
            print("3. 设置")
            print("4. 退出")
            
            choice = input("\n请选择功能 (1-4): ")
            
            if choice == '1':
                # 生成文章
                input_file = input("请输入源文件路径: ")
                template = input("请选择模板 (新闻/博客/论文): ")
                
                try:
                    result = generator.generate(input_file, template)
                    print("\n生成结果:")
                    print(result)
                    
                    # 保存结果
                    output_file = f"output/生成文章_{template}_{Path(input_file).stem}.txt"
                    os.makedirs("output", exist_ok=True)
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result)
                    print(f"\n结果已保存到: {output_file}")
                    
                except Exception as e:
                    logging.error(f"生成失败: {str(e)}")
                    print(f"生成失败: {str(e)}")
                    
            elif choice == '2':
                # 管理模板
                print("\n当前可用模板:")
                templates = config.get('templates', [])
                for i, template in enumerate(templates, 1):
                    print(f"{i}. {template['name']}")
                    
            elif choice == '3':
                # 设置
                print("\n当前设置:")
                settings = config.get_all()
                for key, value in settings.items():
                    print(f"{key}: {value}")
                    
            elif choice == '4':
                print("感谢使用！")
                break
                
            else:
                print("无效的选择，请重试")
                
        return True
        
    except Exception as e:
        logging.error(f"程序运行错误: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        if run_app():
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n程序已终止")
        sys.exit(0)
    except Exception as e:
        logging.error(f"未处理的错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 