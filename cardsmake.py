from PIL import Image, ImageDraw, ImageFont

def add_name(image_path, name):
    # 打开图片
    base_image = Image.open(image_path).convert("RGBA")
    width, height = base_image.size

    texture = Image.open("assets/textures/card_name_texture.jpg").resize((width, 80))    
    font = ImageFont.truetype("assets/fonts/arial.ttf", 36)

    # 创建一个带透明度的黑色边框（稍大一点）
    border_thickness = 4  # 边框厚度
    bordered_texture = Image.new("RGBA", (width + border_thickness * 2, 80 + border_thickness * 2), "black")
    bordered_texture.paste(texture, (border_thickness, border_thickness))

    # 贴到 base_image
    base_image.paste(bordered_texture, (-border_thickness, -border_thickness), bordered_texture)

    draw = ImageDraw.Draw(base_image)
    draw.text((50, 30), name, font=font, fill="black")
    
    return base_image

def add_cost(base_image,cost):
    # 打开图片
    if not (1 <= cost <= 9):
        raise ValueError("Cost 必须是 1-9 之间的整数")

    # 载入 cost 贴图
    cost_image_path = f"assets/textures/persuasion/{cost}.png"
    cost_image = Image.open(cost_image_path).convert("RGBA")

    # 获取图像尺寸
    base_width, base_height = base_image.size
    cost_width, cost_height = cost_image.size

    # 计算右上角的粘贴位置
    margin = 10  # 右上角边距
    paste_x = base_width - cost_width - margin 
    paste_y = margin + 3

    # 贴上 cost 贴图（支持透明度）
    base_image.paste(cost_image, (paste_x, paste_y), cost_image)

    return base_image
    


def add_rounded_border(base_image, border_thickness=30, column_width=35, corner_radius=30):
    # 打开图片
    base_image = base_image.convert("RGBA")
    width, height = base_image.size
    
    # 创建绘图对象
    draw = ImageDraw.Draw(base_image)

    # 绘制外圆角边框
    draw.rounded_rectangle(
        [0, 0, width, height],
        radius=corner_radius,
        outline="black",
        width=border_thickness
    )

    # 在最左和最右绘制黑色 column
    draw.rectangle((0, 0, column_width, height), fill="black")  # 左边
    draw.rectangle((width - column_width, 0, width, height), fill="black")  # 右边

    # 创建遮罩，使图片本身成为圆角
    mask = Image.new("L", (width, height), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([0, 0, width, height], radius=corner_radius, fill=255)
    base_image.putalpha(mask)

    return base_image

# 使用示例
# image_path = "assets/rawpic/修行.jpg"
# base_image = Image.open(image_path).convert("RGBA")
# width, height = base_image.size
# print(
#     f"width: {width}, height: {height}"
# )
image_with_border = add_name("assets/rawpic/修行0.jpg", "修行")
image_with_border = add_cost(image_with_border, 2)
image_with_border = add_rounded_border(image_with_border)
image_with_border.show()
image_with_border.save("assets/cards/修行.png")
