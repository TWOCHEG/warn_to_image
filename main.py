async def add_warn_to_img(img: Image.Image, text_list: list[str], icon: Image.Image) -> Image.Image:
        img = img.convert("RGB").resize((1024, 1024))
        
        blurred = img.filter(ImageFilter.GaussianBlur(radius=30))
        
        overlay_img = icon.convert('RGBA')
        size = blurred.size
        overlay_img = overlay_img.resize((int(size[0] / 2), int(size[1] / 2)))
        white_bg = Image.new('RGBA', overlay_img.size, (255, 255, 255, 255))
        diff = ImageChops.difference(overlay_img, white_bg)
        bbox = diff.getbbox()
        if bbox:
            overlay_img = overlay_img.crop(bbox)
        bg_width, bg_height = blurred.size
        img_width, img_height = overlay_img.size
        offset = ((bg_width - img_width) // 2, ((bg_height - img_height) // 2) - 150)
        
        shadow = Image.new('RGBA', overlay_img.size, color=(0, 0, 0, 255))
        alpha = overlay_img.split()[-1]
        shadow.putalpha(alpha)
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
        shadow_offset = (offset[0] + 10, offset[1] + 10)
        blurred.paste(shadow, shadow_offset, mask=shadow)
        blurred.paste(overlay_img, offset, mask=overlay_img)
        
        text_mask = Image.new("L", blurred.size, 0)
        draw = ImageDraw.Draw(text_mask)
        margin_ratio = 0.05
        max_text_width = blurred.width * (1 - 2 * margin_ratio)
        font_path = "comicbd.ttf"
        initial_font_size = blurred.width // 10
        min_font_size = 10
        line_spacing = 20
        
        def load_font(size):
            try:
                return ImageFont.truetype(font_path, max(size, min_font_size))
            except IOError:
                try:
                    return ImageFont.truetype("arial.ttf", max(size, min_font_size))
                except IOError:
                    return ImageFont.load_default()
        
        def get_text_size(font_obj, text):
            try:
                bbox = draw.textbbox((0, 0), text, font=font_obj)
                return bbox[2] - bbox[0], bbox[3] - bbox[1]
            except AttributeError:
                return font_obj.getsize(text)
        
        fonts = []
        text_sizes = []
        for text in text_list:
            font_size = initial_font_size
            current_font = load_font(font_size)
            text_width, text_height = get_text_size(current_font, text)
            
            if text_width > max_text_width:
                while text_width > max_text_width and font_size > min_font_size:
                    font_size -= 1
                    current_font = load_font(font_size)
                    text_width, text_height = get_text_size(current_font, text)
            else:
                while text_width < max_text_width:
                    font_size += 1
                    current_font = load_font(font_size)
                    new_width, new_height = get_text_size(current_font, text)
                    if new_width > max_text_width:
                        font_size -= 1
                        current_font = load_font(font_size)
                        text_width, text_height = get_text_size(current_font, text)
                        break
                    text_width, text_height = new_width, new_height
            
            fonts.append(current_font)
            text_sizes.append((text_width, text_height))
        
        total_text_height = sum(height for _, height in text_sizes) + (len(text_list) - 1) * line_spacing
        start_y = ((blurred.height - total_text_height) // 2) + 150
        current_y = start_y
        
        text_layer = Image.new("RGBA", blurred.size, (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_layer)
        
        for i, (text, font) in enumerate(zip(text_list, fonts)):
            text_width, text_height = text_sizes[i]
            x = (blurred.width - text_width) // 2
            
            shadow_color = (0, 0, 0, 255)
            shadow_offset = (x + 10, current_y + 10)
            text_draw.text(shadow_offset, text, font=font, fill=shadow_color)
            
            draw.text((x, current_y), text, fill=255, font=font)
            
            current_y += text_height + line_spacing
        
        text_shadow = text_layer.filter(ImageFilter.GaussianBlur(radius=10))
        blurred.paste(text_shadow, (0, 0), mask=text_shadow)
        
        inverted = ImageChops.invert(blurred)
        result = Image.composite(inverted, blurred, text_mask)
        return result
