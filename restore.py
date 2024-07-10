from PIL import Image
import numpy as np
import time

def reverse_cut_swap_and_distribute(images):
    if len(images) != 4:
        raise ValueError("Exactly four images are required.")
    
    # Create a new RGBA image to store the accumulated data
    restored_image = Image.new('RGBA', images[0].size)
    restored_image_data = np.array(restored_image)
    
    # Accumulate image data while handling transparency
    for image in images:
        data = np.array(image)
        
        if data.shape[-1] == 4:  # Check if image has RGBA channels
            # Blend images using alpha (transparency) channel
            alpha = data[:, :, 3] / 255.0  # Normalize alpha channel
            for c in range(3):  # RGB channels
                restored_image_data[:, :, c] = (1 - alpha) * restored_image_data[:, :, c] + alpha * data[:, :, c]
            restored_image_data[:, :, 3] = np.maximum(restored_image_data[:, :, 3], data[:, :, 3])
        else:
            # If image doesn't have alpha channel, simply add RGB values
            restored_image_data[:, :, :3] += data[:, :, :3]
    
    # Ensure pixel values are within valid range [0, 255]
    restored_image_data = np.clip(restored_image_data, 0, 255).astype(np.uint8)
    
    # Convert NumPy array back to PIL Image
    restored_image2 = Image.fromarray(restored_image_data)
    
    height, width, _ = restored_image_data.shape
    
    block_height = height // 32
    block_width = width // 32
    blocks = []

    for i in range(32):
        for j in range(32):
            block = restored_image_data[i*block_height:(i+1)*block_height, j*block_width:(j+1)*block_width]
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
        
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    for i, block in enumerate(swapped_blocks):
        x = (i % 32) * block_width
        y = (i // 32) % 32 * block_height
        restored_image2.paste(Image.fromarray(block), (x, y))
        
    return restored_image2

def reverse_channel_swap_1(image):
    """顏色通道交換方式1的還原：紅色、綠色、藍色"""
    data = np.array(image)
    green, blue, red = data[:,:,0].copy(), data[:,:,1].copy(), data[:,:,2].copy()
    data[:,:,0], data[:,:,1], data[:,:,2] = red, green, blue
    restored_image = Image.fromarray(data)
    return restored_image

def reverse_channel_swap_2(image):
    """顏色通道交換方式2的還原：綠色、藍色、紅色"""
    data = np.array(image)
    blue, red, green = data[:,:,0].copy(), data[:,:,1].copy(), data[:,:,2].copy()
    data[:,:,0], data[:,:,1], data[:,:,2] = red, green, blue
    restored_image = Image.fromarray(data)
    return restored_image

def reverse_channel_swap_3(image):
    """顏色通道交換方式3的還原：紅色、綠色、藍色"""
    data = np.array(image)
    red, blue, green = data[:,:,0].copy(), data[:,:,1].copy(), data[:,:,2].copy()
    data[:,:,0], data[:,:,1], data[:,:,2] = red, green, blue
    restored_image = Image.fromarray(data)
    return restored_image

def reverse_negative_effect(image):
    """Applies the reverse negative effect to the image while preserving the alpha channel if present."""
    data = np.array(image)

    if data.shape[-1] == 4:
        rgb = data[..., :3]
        alpha = data[..., 3]
        negative_rgb = 255 - rgb
        negative_image_data = np.dstack((negative_rgb, alpha))
    
    else:
        negative_image_data = 255 - data
    
    restored_image = Image.fromarray(negative_image_data)
    
    return restored_image



# 是否要上下顛倒
swap = 1


    
frames = []
gif_images = []

# 加載四張圖片
image_paths = []

pwd = ""

pwd = input(f"Input passwords for the 4 correct photos:")

for i in range(4):
    image_paths.append(f"_{pwd[i]}.png")



images = [Image.open(path) for path in image_paths]

gif_images.append(images[0])
images[0] = reverse_channel_swap_1(images[0])
gif_images.append(images[0])

gif_images.append(images[1])
images[1] = reverse_channel_swap_2(images[1])
gif_images.append(images[1])

gif_images.append(images[2])
images[2] = reverse_channel_swap_3(images[2])
gif_images.append(images[2])

gif_images.append(images[3])
images[3] = reverse_negative_effect(images[3])
gif_images.append(images[3])


# 還原原始圖像
restored_image = reverse_cut_swap_and_distribute(images)
gif_images.append(restored_image)


# 确保每个图像是 RGBA 模式
for i, img in enumerate(gif_images):
    if img.mode != 'RGBA':
        gif_images[i] = img.convert('RGBA')

# 创建一个空白的画布，用于叠加图像，假设画布大小为所有图像中最大的宽高
canvas_width = max(img.width for img in gif_images)
canvas_height = max(img.height for img in gif_images)
canvas = Image.new('RGBA', (canvas_width, canvas_height))

# 叠加每一帧并保存
for i, img in enumerate(gif_images[:9]):  # 只处理前9帧
    canvas.paste(img, (0, 0), img)  # 在画布上叠加当前帧
    canvas.save(f'frame_{i+1}.png')
    canvas.show()
    time.sleep(0.05)
    
    