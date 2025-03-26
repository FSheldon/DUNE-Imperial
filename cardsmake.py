from PIL import Image, ImageDraw, ImageFont

def add_rounded_border(image_path, border_thickness=30, column_width=35, corner_radius=30):
    # 打开图片
    base_image = Image.open(image_path).convert("RGBA")
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
image_path = "assets/rawpic/修行.jpg"
image_with_border = add_rounded_border(image_path)
image_with_border.show()
image_with_border.save("assets/cards/修行.png")
