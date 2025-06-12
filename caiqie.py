import os
import cv2
import numpy as np

def crop_resize(image, target_size=(640, 640)):
    """中心裁剪后缩放（保持内容比例，但会丢失边缘部分）"""
    h, w = image.shape[:2]
    
    # 计算裁剪区域（取中央部分）
    crop_size = min(h, w)  # 选择短边
    start_h = (h - crop_size) // 2
    start_w = (w - crop_size) // 2
    cropped = image[start_h:start_h+crop_size, start_w:start_w+crop_size]
    
    # 缩放到目标尺寸
    return cv2.resize(cropped, target_size, interpolation=cv2.INTER_AREA)

def process_image(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Cannot read image {input_path}")
        return
    
    resized_img = crop_resize(img)
    cv2.imwrite(output_path, resized_img)
    print(f"Saved: {output_path}")

# 使用示例
process_image("input.jpg", "output_cropped.jpg")
def process_folder(input_dir, output_dir, mode="stretch"):
    """批量处理文件夹中的所有图片
    :param mode: "stretch"（拉伸）或 "crop"（裁剪）
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            img = cv2.imread(input_path)
            if img is None:
                continue
                
            if mode == "crop":
                resized = crop_resize(img)
            
                
                
            cv2.imwrite(output_path, resized)
    print(f"Processed all images in {input_dir}")

# 使用示例
#process_folder("input_images", "output_stretched", mode="stretch")
process_folder("./data/cs", "./data/css", mode="crop")