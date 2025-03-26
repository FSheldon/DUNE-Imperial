from PIL import Image, ImageDraw, ImageFont

def generate_card_image(card_data):
    base_image = Image.open(card_data["image"]).resize((300, 450))
    draw = ImageDraw.Draw(base_image)
    
    # 载入字体（需要提供路径）
    font = ImageFont.truetype("assets/fonts/arial.ttf", 24)

    # 绘制名称
    draw.text((10, 10), card_data["name"], fill="black", font=font)
    draw.text((10, 50), f"势力: {card_data['faction']}", fill="white", font=font)
    draw.text((10, 90), f"效果: {card_data['effect']}", fill="white", font=font)
    
    # 保存图片
    base_image.save(f"assets/cards/{card_data['name']}.png")

# 读取 JSON 数据并生成卡片
import json
with open("cards.json", "r", encoding="utf-8") as f:
    cards = json.load(f)

for card in cards:
    generate_card_image(card)
