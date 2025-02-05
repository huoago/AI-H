from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建一个 256x256 的图像
    size = (256, 256)
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    circle_bbox = (20, 20, 236, 236)
    draw.ellipse(circle_bbox, fill='#4A90E2')
    
    # 添加文字
    try:
        font = ImageFont.truetype("simhei.ttf", 120)
    except:
        font = ImageFont.load_default()
        
    text = "AI"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, font=font, fill='white')
    
    # 保存为ICO文件
    icon_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
    os.makedirs(icon_dir, exist_ok=True)
    icon_path = os.path.join(icon_dir, 'icon.ico')
    
    image.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    return icon_path

if __name__ == '__main__':
    create_icon() 