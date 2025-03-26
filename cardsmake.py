# from PIL import Image, ImageDraw, ImageFont

# def draw_gradient_diamond(draw, position, size, cost):
#     """绘制带渐变的蓝青色菱形，并在其中显示 cost """
#     x, y = position
#     half_size = size // 2
    
#     # 创建渐变填充
#     for i in range(size):
#         color = (0, int(150 + (105 * i / size)), int(255 - (155 * i / size)))  # 生成蓝青色渐变
#         draw.line([(x - half_size + i, y - i), (x + half_size - i, y - i)], fill=color)
    
#     # 绘制边框
#     diamond = [(x, y - half_size), (x + half_size, y), (x, y + half_size), (x - half_size, y)]
#     draw.polygon(diamond, outline="white", width=2)
    
#     # 显示 cost
#     font = ImageFont.truetype("assets/fonts/arial.ttf", 24)
#     text_size = draw.textbbox((0, 0), str(cost), font=font)
#     text_x = x - (text_size[2] - text_size[0]) // 2
#     text_y = y - (text_size[3] - text_size[1]) // 2
#     draw.text((text_x, text_y), str(cost), fill="white", font=font)

# def generate_card_image(card_data):
#     base_image = Image.open(card_data["image"]).resize((300, 450))
    
#     # 创建黑色边框的底图
#     final_image = Image.new("RGB", (320, 470), "black")
#     final_image.paste(base_image, (10, 10))
#     draw = ImageDraw.Draw(final_image)
    
#     font = ImageFont.truetype("assets/fonts/arial.ttf", 24)
#     small_font = ImageFont.truetype("assets/fonts/arial.ttf", 18)
    
#     # 绘制顶部区域
#     draw.rectangle([(10, 10), (160, 50)], fill="white")
#     draw.text((15, 15), card_data["name"], fill="black", font=font)
#     draw.rectangle([(160, 10), (310, 50)], fill=(128, 0, 128))  # 紫色背景
#     draw.text((165, 15), card_data["faction"], fill="white", font=font)
    
#     # 绘制底部区域
#     draw.text((15, 400), f"Regions: {', '.join(card_data['regions'])}", fill="white", font=small_font)
#     draw.text((15, 420), f"Effect: {card_data['effect']}", fill="white", font=small_font)
#     draw.text((15, 440), f"Output: {card_data['output']}", fill="white", font=small_font)
    
#     # 绘制 cost 菱形
#     draw_gradient_diamond(draw, (280, 40), 40, card_data["cost"])
    
#     # 保存图片
#     final_image.save(f"assets/cards/{card_data['name']}.png")

# # 读取 JSON 数据并生成卡片
# import json
# with open("cards.json", "r", encoding="utf-8") as f:
#     cards = json.load(f)

# for card in cards:
#     generate_card_image(card)

from PIL import Image, ImageDraw, ImageFont

def add_rounded_border(image_path, border_thickness=20, corner_radius=30):
    # 打开图片
    base_image = Image.open(image_path)
    width, height = base_image.size

    # 创建一个新的图像，稍微大一点来容纳边框
    #bordered_image = Image.new("RGB", (width + 2 * border_thickness, height + 2 * border_thickness), "white")
    #bordered_image.paste(base_image, (border_thickness, border_thickness))

    # 创建绘图对象
    draw = ImageDraw.Draw(base_image)

    # 绘制外圆角边框
    draw.rounded_rectangle(
        [0, 0, width, height],
        radius=corner_radius,
        outline="black",
        width=border_thickness
    )

    # 绘制内圆角边框
    draw.rounded_rectangle(
        [border_thickness, border_thickness, width - border_thickness, height - border_thickness],
        radius=corner_radius,
        outline="white",
        width=border_thickness
    )

    return base_image

# 使用示例
image_path = "assets/rawpic/修行.jpg"
image_with_border = add_rounded_border(image_path)
image_with_border.show()
image_with_border.save("assets/cards/修行.jpg")
