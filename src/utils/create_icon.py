from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_app_icon():
    """创建应用图标"""
    # 创建一个 256x256 的图像
    size = (256, 256)
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    circle_bbox = (20, 20, 236, 236)
    draw.ellipse(circle_bbox, fill='#4A90E2')  # 使用蓝色背景
    
    # 添加文字
    try:
        # 尝试加载中文字体
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",  # Windows
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",  # Linux
            "/System/Library/Fonts/PingFang.ttc"  # macOS
        ]
        
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 120)
                break
                
        if font is None:
            font = ImageFont.load_default()
            
    except Exception:
        font = ImageFont.load_default()
    
    # 绘制文字
    text = "AI"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # 添加文字阴影
    shadow_offset = 3
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill='#2C5EA0')
    
    # 添加主文字
    draw.text((x, y), text, font=font, fill='white')
    
    # 保存为ICO文件
    resources_dir = Path(__file__).parent.parent.parent / 'resources'
    resources_dir.mkdir(exist_ok=True)
    
    icon_path = resources_dir / 'icon.ico'
    
    # 创建多个尺寸的图标
    sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
    image.save(str(icon_path), format='ICO', sizes=sizes)
    
    return icon_path

if __name__ == '__main__':
    icon_path = create_app_icon()
    print(f"图标已创建: {icon_path}") 