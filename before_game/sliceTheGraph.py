from PIL import Image, ImageFilter
import numpy as np

def channel_swap_1(image):
    """顏色通道交換方式1：綠色、藍色、紅色"""
    data = np.array(image)
    red, green, blue = data[:,:,0].copy(), data[:,:,1].copy(), data[:,:,2].copy()
    data[:,:,0], data[:,:,1], data[:,:,2] = green, blue, red
    swapped_image = Image.fromarray(data)
    return swapped_image

def channel_swap_2(image):
    """顏色通道交換方式2：藍色、紅色、綠色"""
    data = np.array(image)
    red, green, blue = data[:,:,0].copy(), data[:,:,1].copy(), data[:,:,2].copy()
    data[:,:,0], data[:,:,1], data[:,:,2] = blue, red, green
    swapped_image = Image.fromarray(data)
    return swapped_image

def channel_swap_3(image):
    """顏色通道交換方式3：紅色、藍色、綠色"""
    data = np.array(image)
    red, green, blue = data[:,:,0].copy(), data[:,:,1].copy(), data[:,:,2].copy()
    data[:,:,0], data[:,:,1], data[:,:,2] = red, blue, green
    swapped_image = Image.fromarray(data)
    return swapped_image

def negative_effect(image):
    """Applies a negative effect to the image while preserving the alpha channel if present."""
    data = np.array(image)

    if data.shape[-1] == 4:
        rgb = data[..., :3]
        alpha = data[..., 3]
        negative_rgb = 255 - rgb
        negative_image_data = np.dstack((negative_rgb, alpha))
    
    else:
        negative_image_data = 255 - data
    
    negative_image = Image.fromarray(negative_image_data)
    
    return negative_image

def pixelate(image, pixel_size=10):
    """像素化處理並維持原始尺寸"""
    # 記錄原始尺寸
    original_size = image.size
    
    # 縮小圖像
    small_image = image.resize(
        (image.width // pixel_size, image.height // pixel_size),
        Image.NEAREST
    )
    
    # 將縮小後的圖像放大回原始尺寸
    pixelated_image = small_image.resize(
        original_size,
        Image.NEAREST
    )
    
    return pixelated_image

def blur(image):
    """模糊處理"""
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
    return blurred_image

def pixelate2(image, pixel_size=100):
    """大程度像素化處理並維持原始尺寸"""
    # 記錄原始尺寸
    original_size = image.size
    
    # 縮小圖像
    small_image = image.resize(
        (image.width // pixel_size, image.height // pixel_size),
        Image.NEAREST
    )
    
    # 將縮小後的圖像放大回原始尺寸
    pixelated_image = small_image.resize(
        original_size,
        Image.NEAREST
    )
    
    return pixelated_image

def blur2(image):
    """大程度模糊處理"""
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=100))
    return blurred_image

def resize_image_to_fit(image, base=32):
    """將圖像縮放或裁剪以適應基數倍數的尺寸"""
    width, height = image.size
    new_width = (width // base) * base
    new_height = (height // base) * base
    
    if (new_width, new_height) == (width, height):
        return image
    
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image

def cut_swap_and_distribute(image):
    """將圖片裁切成 1024 等分，進行互換和旋轉處理，並分配到 4 張 PNG 圖檔中"""
    data = np.array(image)
    height, width, _ = data.shape
    
    block_height = height // 32
    block_width = width // 32
    blocks = []

    for i in range(32):
        for j in range(32):
            block = data[i*block_height:(i+1)*block_height, j*block_width:(j+1)*block_width]
            blocks.append(block)
    
    # 進行互換和旋轉處理
    swapped_blocks = [None] * 1024
    for i in range(1024):
        if swap == 1:
            complement = 1023 - i
        else:
            complement = i
            
        ones_count = bin(i).count('1')
        rotation_angle = 0
        rotated_block = np.rot90(blocks[complement], k=rotation_angle)
        swapped_blocks[i] = rotated_block
    
    # 創建4張新的PNG圖檔，背景為透明
    images = [Image.new("RGBA", (width, height), (0, 0, 0, 0)) for _ in range(4)]
    
    # 分配裁切出的小塊到4張圖檔中
    for i, block in enumerate(swapped_blocks):
        x = [94, 41, 150, 119, 36, 93, 171, 62, 24, 157, 6, 158, 186, 73, 71, 186, 1, 77, 138, 135, 198, 103, 121, 150, 73, 27, 167, 165, 80, 173, 8, 0, 64, 192, 159, 46, 116, 89, 171, 101, 161, 106, 125, 90, 198, 156, 158, 178, 72, 48, 141, 64, 20, 193, 31, 148, 47, 195, 182, 47, 86, 125, 97, 69, 51, 69, 137, 95, 183, 199, 133, 43, 40, 151, 165, 76, 120, 33, 40, 117, 118, 185, 188, 167, 92, 121, 163, 62, 84, 24, 71, 155, 89, 60, 110, 108, 73, 88, 29, 30, 16, 81, 55, 110, 20, 128, 21, 187, 72, 120, 14, 1, 184, 149, 4, 179, 172, 174, 127, 152, 136, 63, 17, 89, 45, 128, 178, 41, 137, 77, 127, 99, 103, 75, 38, 114, 60, 102, 54, 107, 69, 6, 52, 109, 42, 148, 157, 87, 107, 39, 131, 116, 136, 60, 192, 74, 23, 108, 1, 141, 154, 97, 186, 2, 86, 180, 124, 91, 196, 189, 99, 43, 96, 193, 189, 108, 81, 187, 110, 170, 8, 65, 89, 110, 140, 90, 116, 73, 97, 11, 9, 73, 24, 150, 102, 69, 190, 166, 21, 108, 13, 159, 87, 195, 34, 53, 74, 123, 147, 133, 170, 103, 70, 130, 109, 19, 131, 103, 185, 31, 88, 60, 78, 10, 111, 85, 84, 185, 119, 132, 106, 157, 83, 91, 162, 55, 161, 105, 55, 156, 169, 86, 107, 86, 137, 98, 116, 80, 77, 21, 76, 161, 185, 32, 87, 78, 64, 139, 1, 161, 94, 73, 36, 49, 132, 10, 73, 95, 68, 109, 93, 15, 5, 117, 51, 103, 26, 141, 84, 103, 74, 141, 138, 142, 111, 5, 42, 67, 151, 136, 84, 35, 92, 183, 116, 82, 156, 103, 68, 101, 37, 12, 104, 136, 142, 100, 62, 97, 35, 72, 157, 34, 162, 51, 156, 59, 115, 152, 37, 63, 72, 118, 10, 12, 59, 85, 146, 54, 100, 187, 57, 191, 48, 128, 88, 74, 155, 16, 76, 167, 12, 81, 94, 42, 50, 75, 118, 80, 48, 51, 55, 155, 130, 25, 124, 181, 180, 47, 24, 110, 98, 123, 82, 167, 99, 12, 88, 9, 160, 183, 85, 13, 143, 198, 165, 78, 0, 191, 163, 38, 155, 144, 108, 31, 90, 91, 121, 125, 24, 162, 15, 165, 118, 168, 129, 44, 78, 140, 51, 191, 107, 151, 124, 90, 168, 75, 1, 77, 95, 56, 5, 1, 96, 40, 185, 101, 120, 131, 150, 156, 83, 50, 103, 182, 86, 0, 185, 169, 147, 117, 174, 47, 87, 104, 198, 84, 66, 17, 12, 189, 168, 30, 132, 43, 60, 185, 86, 103, 144, 24, 76, 125, 108, 45, 73, 50, 25, 139, 37, 172, 127, 53, 20, 18, 99, 142, 17, 191, 140, 71, 66, 136, 128, 121, 114, 46, 134, 8, 77, 163, 196, 27, 73, 199, 9, 125, 108, 168, 139, 138, 91, 80, 57, 166, 97, 178, 12, 124, 71, 155, 142, 10, 15, 141, 45, 117, 149, 27, 89, 30, 86, 54, 85, 152, 86, 130, 186, 108, 12, 168, 92, 38, 78, 121, 86, 43, 186, 67, 168, 65, 31, 34, 43, 22, 43, 52, 85, 192, 68, 21, 187, 21, 121, 142, 180, 81, 194, 38, 80, 112, 115, 105, 162, 35, 32, 100, 45, 60, 179, 118, 143, 117, 56, 80, 183, 193, 190, 21, 172, 139, 186, 144, 77, 187, 24, 148, 92, 190, 165, 179, 135, 139, 189, 123, 46, 180, 49, 15, 104, 102, 152, 99, 1, 16, 60, 2, 152, 107, 145, 19, 64, 13, 197, 42, 185, 190, 179, 121, 106, 151, 60, 170, 93, 122, 145, 89, 10, 120, 166, 168, 119, 162, 116, 43, 87, 181, 156, 75, 156, 100, 35, 157, 187, 33, 115, 71, 181, 79, 199, 189, 36, 90, 65, 35, 95, 62, 86, 27, 31, 194, 181, 140, 67, 68, 121, 108, 120, 2, 80, 26, 128, 188, 66, 48, 128, 21, 116, 125, 5, 125, 163, 103, 116, 136, 151, 67, 103, 29, 110, 146, 56, 160, 133, 151, 24, 100, 78, 193, 121, 52, 170, 36, 44, 136, 166, 66, 43, 35, 25, 21, 198, 190, 12, 98, 142, 4, 64, 129, 41, 13, 46, 195, 176, 191, 55, 38, 79, 147, 132, 17, 116, 82, 147, 183, 71, 145, 0, 169, 112, 50, 172, 75, 116, 189, 188, 57, 82, 41, 150, 11, 28, 46, 173, 148, 20, 181, 3, 96, 182, 18, 188, 140, 35, 150, 167, 30, 118, 7, 171, 54, 156, 150, 189, 38, 124, 77, 108, 162, 71, 69, 123, 49, 128, 4, 154, 93, 163, 43, 165, 136, 159, 159, 159, 167, 122, 111, 149, 55, 159, 76, 157, 57, 126, 3, 79, 191, 44, 38, 36, 119, 49, 99, 115, 161, 58, 1, 105, 70, 193, 19, 156, 195, 39, 50, 48, 169, 98, 14, 121, 42, 60, 124, 199, 114, 62, 47, 92, 190, 68, 181, 143, 33, 118, 104, 132, 46, 57, 34, 95, 91, 123, 124, 112, 190, 18, 101, 117, 103, 34, 68, 153, 25, 171, 181, 178, 165, 31, 107, 79, 9, 123, 110, 53, 6, 188, 21, 197, 110, 75, 15, 188, 37, 183, 12, 33, 97, 94, 188, 160, 151, 153, 2, 109, 33, 163, 33, 167, 147, 36, 58, 31, 36, 66, 35, 122, 77, 105, 43, 180, 24, 7, 6, 159, 140, 2, 102, 72, 186, 96, 98, 16, 154, 32, 71, 33, 87, 66, 27, 168, 135, 44, 51, 184, 46, 148, 128, 11, 144, 11, 59, 31, 108, 44, 72, 95, 33, 144, 33, 178, 183, 191, 123, 104, 67, 136, 17, 36, 139, 81, 135, 191, 158, 148, 39, 96, 15, 49, 37, 92, 51, 150, 60, 55, 132, 40, 157, 124, 7, 142, 126, 137, 11, 126, 126, 31, 60, 183, 159, 143, 143, 43, 20, 59, 59, 19, 195, 134, 40, 184, 113, 36, 130, 40, 134, 116, 71, 198, 46, 86, 57, 179, 3, 12, 92, 166, 24, 169, 40, 92, 163, 122, 129, 28, 17, 37, 123, 79, 190, 26, 171, 46, 178, 132, 147, 19, 87, 190, 75, 88, 46, 152, 194, 103, 89, 32, 116, 181, 143, 49, 42, 92, 195, 176, 58, 37, 93, 40, 102, 26, 5, 59, 25, 94, 20, 124, 104, 199, 179, 82, 187, 108, 48, 40, 139, 104, 172, 34, 9, 40, 14, 74, 190, 73, 161, 113, 5, 6, 154, 9, 83, 90, 5, 27, 45, 23, 153, 182, 100, 194, 60, 90, 97, 31, 46, 94, 80, 72, 87, 94, 102, 22, 100, 151, 136, 87, 83, 138, 15, 193, 85, 163, 105, 139, 164, 43, 31, 143, 63, 28, 12, 83, 179, 148, 22, 189, 108, 53, 148, 99, 97, 121, 42, 62, 123, 138, 113, 96, 147, 148, 117, 27, 122, 126, 121, 99, 111, 182, 124, 157, 80, 125, 90, 25, 93, 83, 4, 69, 118, 80, 34, 65, 105, 127, 41, 150, 25, 135, 58, 130, 94, 0, 47, 36, 170, 199, 49, 83, 13, 149, 160, 90, 80, 13, 66, 142, 134, 172, 120, 9, 120, 31, 115, 6, 192, 65, 140, 124, 55, 61, 76, 106, 156, 5, 96, 76, 168, 172, 92, 186, 152, 86, 56, 159, 92, 122, 154, 186, 136, 124, 170, 73, 180, 68, 89, 35, 93, 162, 96, 128, 2, 185, 11, 28, 41, 119, 23, 68, 163, 42, 46, 193, 140, 74, 165, 165, 169, 80, 15, 27, 3, 32, 42, 193, 22, 87, 85, 176, 174, 20, 110, 106, 113, 145, 50, 102, 199, 164, 65, 144, 102, 186, 125, 4, 172, 14, 75, 130, 56, 12, 44, 137, 101, 57, 88, 103, 174, 8, 122, 100, 130, 78, 77, 58, 149, 84, 116, 190, 75, 1, 100, 185, 161, 149, 91, 0, 140, 192, 159, 61, 106, 36, 13, 117, 100, 84, 77, 143, 3, 117, 182, 174, 97, 76, 119, 79, 167, 162, 23, 55, 75, 174, 11, 67, 144, 198, 176, 48, 172, 190, 133, 57, 132, 134, 55, 79, 153, 120, 3, 0, 184, 129, 108, 11, 102, 88, 125, 79, 76, 196, 78, 129, 181, 160, 196, 161, 60, 71, 69, 40, 72, 58, 118, 61, 176, 121, 120, 78, 161, 59, 48, 43, 197, 70, 27, 138, 191, 83, 153, 192, 77, 158, 17, 125, 38, 131, 73, 182, 198, 171, 183, 117, 190, 35, 41, 183, 153, 176, 155, 68, 154, 172, 160, 95, 113, 76, 119, 65, 71, 77, 134, 23, 193, 56, 44, 79, 195, 1, 58, 74, 66, 30, 142, 3, 61, 176, 46, 173, 110, 114, 27, 30, 148, 11, 44, 48, 13, 193, 130, 18, 87, 149, 13, 61, 100, 101, 53, 82, 6, 185, 156, 74, 199, 162, 25, 71, 94, 161, 13, 156, 13, 12, 162, 129, 139, 52, 136, 144, 183, 167, 105, 25, 168, 141, 182, 114, 44, 153, 101, 80, 86, 15, 25, 182, 129, 134, 89, 185, 2, 126, 44, 51, 82, 72, 8, 73, 7, 6, 9, 21, 19, 29, 43, 41, 64, 191, 25, 74, 28, 170, 143, 108, 174, 77, 59, 18, 184, 45, 27, 172, 98, 67, 95, 111, 154, 57, 180, 137, 103, 63, 176, 68, 123, 140, 11, 5, 83, 66, 165, 110, 70, 88, 165, 88, 119, 132, 12, 20, 26, 79, 140, 90, 13, 44, 157, 3, 16, 74, 37, 116, 83, 79, 6, 50, 24, 8, 156, 106, 56, 50, 68, 55, 36, 166, 55, 157, 114, 5, 58, 106, 199, 104, 75, 67, 26, 26, 123, 10, 158, 54, 112, 151, 15, 125, 30, 149, 196, 172, 113, 146, 173, 136, 57, 98, 120, 86, 84, 0, 110, 158, 85, 170, 43, 158, 190, 90, 131, 47, 27, 118, 72, 74, 12, 127, 64, 119, 193, 56, 176, 93, 69, 84, 177, 85, 29, 107, 139, 106, 50, 72, 125, 88, 8, 127, 43, 20, 59, 77, 48, 157, 90, 195, 45, 24, 120, 183, 193, 142, 55, 56, 14, 16, 160, 147, 128, 91, 167, 178, 58, 94, 61, 65, 70, 168, 31, 190, 72, 33, 67, 94, 146, 148, 86, 11, 47, 101, 102, 59, 176, 38, 155, 34, 81, 141, 171, 108, 121, 68, 147, 103, 28, 113, 113, 73, 177, 114, 162, 195, 122, 122, 174, 35, 130, 18, 51, 162, 46, 195, 158, 22, 23, 191, 30, 93, 86, 93, 186, 86, 157, 187, 189, 15, 183, 115, 140, 48, 29, 133, 86, 132, 103, 183, 26, 25, 73, 3, 22, 84, 92, 94, 95, 104, 58, 146, 62, 138, 194, 115, 89, 82, 57, 16, 97, 84, 171, 160, 5, 118, 148, 62, 57, 112, 157, 189, 132, 36, 17, 54, 1, 110, 194, 162, 46, 168, 159, 96, 178, 129, 126, 54, 124, 106, 133, 83, 176, 14, 120, 162, 169, 168, 173, 160, 26, 74, 170, 169, 91, 46, 128, 149, 80, 151, 131, 56, 133, 87, 74, 142, 74, 184, 71, 189, 44, 130, 198, 100, 86, 130, 48, 1, 152, 26, 173, 76, 192, 146, 150, 51, 164, 166, 197, 109, 152, 43, 51, 96, 105, 158, 131, 39, 93, 156, 0, 183, 17, 93, 108, 36, 191, 28, 39, 140, 132, 101, 122, 171, 177, 98, 85, 97, 71, 37, 80, 114, 41, 172, 90, 144, 20, 187, 108, 169, 119, 114, 169, 167, 157, 121, 63, 48, 23, 180, 102, 193, 114, 130, 161, 44, 86, 109, 125, 138, 13, 39, 178, 63, 63, 112, 57, 120, 109, 63, 90, 199, 31, 185, 59, 192, 168, 181, 82, 21, 153, 136, 80, 81, 102, 144, 86, 163, 25, 99, 170, 23, 68, 81, 156, 118, 81, 36, 193, 137, 30, 84, 91, 106, 28, 189, 75, 122, 6, 36, 4, 12, 68, 16, 52, 199, 136, 85, 138, 173, 61, 79, 56, 102, 44, 92, 58, 11, 95, 142, 104, 29, 173, 188, 159, 145, 193, 116, 60, 39, 125, 59, 162, 42, 5, 137, 123, 105, 24]

        img_index = (i + x[i]) % 4  # 決定當前塊應該分配到哪一張圖檔
        
        if img_index in [0, 1, 2, 3]:
            x = (i % 32) * block_width
            y = (i // 32) % 32 * block_height
            images[img_index].paste(Image.fromarray(block), (x, y))
    
    # 保存4張圖檔
    for i, img in enumerate(images):
        if i == 0:
            img = pixelate(img)
            
        if i == 1:
            img = blur(img)
            
        if i == 2:
            img = blur2(image)
            
        if i == 3:
            img = pixelate2(image)
        
        img.save(f"output_folder/{pwd[i]}.png")
        
    # 保存4張圖檔
    for i, img in enumerate(images):
        if i == 0:
            img = channel_swap_1(img)
        if i == 1:
            img = channel_swap_2(img)
        if i == 2:
            img = channel_swap_3(img)
        if i == 3:
            img = negative_effect(img)
        
        img.save(f"output_folder/{pwd[i+4]}.png")

pwd = ["1", "2", "3", "4", "5", "6", "7", "8"]

# 是否要上下顛倒
swap = 1

# 假設我們有一個原始圖像路徑
input_image_path = "input_image.jpg"
original_image = Image.open(input_image_path)

# 調整圖像尺寸以適應裁切
adjusted_image = resize_image_to_fit(original_image)

# 裁切、處理並分配圖像
cut_swap_and_distribute(adjusted_image)