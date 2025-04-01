from PIL import Image, ImageDraw, ImageFont

def add_name(image_path, name):
    # 打开图片
    base_image = Image.open(image_path)
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
    draw.text((40, 30), name, font=font, fill="black")
    
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
    
def add_factions(base_image, factions, margin=10):
    """
    在卡牌左侧粘贴势力图标。
    
    :param base_image: PIL.Image, 卡牌基础图片
    :param factions: list[str], 需要粘贴的势力名称列表（最多 4 个）
    :param margin: int, 势力图标之间的间隔
    :return: PIL.Image, 添加势力图标后的图片
    """
    max_factions = min(len(factions), 4)  # 最多 4 个势力
    width, height = base_image.size
    icon_path = "assets/textures/factions/"  # 势力图标所在目录
    icon_size = Image.open(icon_path + factions[0] + ".png").size  # 读取第一个势力图标的大小
    icon_w, icon_h = icon_size
    
    # 计算起始 y 坐标，使图标在左侧居中排列
    total_height = max_factions * icon_h + (max_factions - 1) * margin
    start_y = 84
    paste_x = margin  # 图标左侧固定间距
    
    for i in range(max_factions):
        faction = factions[i]
        try:
            icon = Image.open(icon_path + faction + ".png").convert("RGBA")
            base_image.paste(icon, (paste_x , start_y + i * (icon_h + 2)), icon)
        except FileNotFoundError:
            print(f"[警告] 势力图标 {faction}.png 未找到，跳过。")
    
    return base_image

def add_outputs(base_image, effects):
    """
    在卡牌底侧粘贴效果图标。
    
    :param base_image: PIL.Image, 卡牌基础图片
    :param effects: list[str], 需要粘贴的效果名称列表（最多 4 个）
    :return: PIL.Image, 添加效果图标后的图片 以及粘贴的底图片的 height
    """
    
    # 加载底图片
    base_overlay = Image.open("assets/textures/bottom.png")
    base_width, base_height = base_overlay.size
    
    # 调整底图片宽度匹配卡牌
    card_width, card_height = base_image.size
    base_image.paste(base_overlay, (35, card_height-base_height-25), base_overlay)
    
    if not effects:
        return base_image, base_height
    
    # 处理效果图标
    effect_images_pers = []
    effect_images_knife = []
    has_persuasion = False  # 是否有“说服”效果
    has_knife = False  # 是否有“刀”效果

    for effect in effects[:4]:
        if effect.startswith("说服"):
            effect_img = Image.open(f"assets/textures/persuasion/{effect[2:]}.png").resize((80, 80))
            effect_images_pers.append(effect_img) 
            has_persuasion = True  # 标记“说服”已出现
            #如果 effect 以 "说服" 开头，说明它是 “说服”类型 的效果，比如 "说服3"。
            #effect[2:] 取出 "说服" 后面的数字（如 "3"），用于加载相应的图片。
        elif effect.startswith("刀"):
            effect_img = Image.open("assets/textures/knife.png").resize((60,60)) 
            has_knife = True
            for i in range(0, int(effect[1:])):
                effect_images_knife.append(effect_img)  # 添加多把刀
        else:
            continue
    
    base_spacing = 20 if has_persuasion and has_knife else 0  # 只有两种效果同时出现时才加间距
    effect_images = effect_images_pers + effect_images_knife
    
    # 计算图标位置（底部居中排列）
    total_width = sum(img.width for img in effect_images_pers) + base_spacing + int(sum(img.width for img in effect_images_knife) * 0.75)
    start_x = (card_width - total_width) // 2
    y_pos = card_height - 25 - (base_height + effect_images[0].height) // 2 #-25是减去底部边框
    
    x_offset = start_x
    for img in effect_images_pers:
        base_image.paste(img, (x_offset, y_pos), img)
        x_offset += img.width + 20
    
    for img in effect_images_knife:
        base_image.paste(img, (x_offset, y_pos + 15), img)
        x_offset += img.width - 20
    
    return base_image, base_height + 25 #output栏加边框高度 

def add_effects(base_image, outputs_height, effects):
    """
    在卡牌底侧粘贴效果图标。
    
    :param base_image: PIL.Image, 卡牌基础图片
    :param outputs_height: int, 输出栏的高度
    :param effects: list[str], 需要粘贴的效果名称列表（最多 4 个）
    :return: PIL.Image, 添加效果图标后的图片
    """
    base_overlay = Image.open("assets/textures/effect_bottom.png")
    overlay_width, overlay_height = base_overlay.size
    
    card_width, card_height = base_image.size
    base_image.paste(base_overlay, (35, card_height - overlay_height - outputs_height ), base_overlay)

    return base_image, overlay_height + outputs_height

def add_region(base_image , regions, effects_height, margin = 10):
    
    len_region = len(regions)
    card_width, card_height = base_image.size
    icon_path = "assets/textures/card_region_icon/"  # 势力图标所在目录
    icon_size = Image.open(icon_path + regions[0] + ".png").size  # 读取第一个势力图标的大小
    icon_w, icon_h = icon_size
    
    # 计算起始 y 坐标，使图标在左侧居中排列
    total_height = len_region  * icon_h + (len_region  - 1) * margin
    start_y = card_height - total_height - effects_height
    paste_x = 35 # 图标左侧固定间距
    
    for i in range(len_region):
        region = regions[i]
        try:
            icon = Image.open(icon_path + region + ".png").convert("RGBA")
            base_image.paste(icon, (paste_x, start_y + i * (icon_h + 5)), icon)
        except FileNotFoundError:
            print(f"[警告] 区域图标 {region}.png 未找到，跳过。")
    
    return base_image

def add_rounded_border(base_image, border_thickness=30, column_width=35, corner_radius=30):
    """
    加边框 切圆
    """
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
image_with_border = add_factions(image_with_border, ["弗雷曼人","宇宙公会","贝尼·杰瑟里特姐妹会"])
effects_list = ["说服5","刀4"]
image_with_border, overlay_height = add_outputs(image_with_border, effects_list)
image_with_border, overlay_height = add_effects(image_with_border, overlay_height, effects_list)
image_with_border = add_region(image_with_border, ["立法会" ,"香料贸易"], overlay_height)
image_with_border = add_rounded_border(image_with_border)

image_with_border.show()
image_with_border.save("assets/cards/修行.png")
