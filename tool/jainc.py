import cv2
import numpy as np

def visualize_annotations(image_path, annotation_path):
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    with open(annotation_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center, y_center, box_width, box_height = map(float, parts[1:])

            # 转换为像素坐标
            x1 = int((x_center - box_width / 2) * width)
            y1 = int((y_center - box_height / 2) * height)
            x2 = int((x_center + box_width / 2) * width)
            y2 = int((y_center + box_height / 2) * height)

            # 绘制矩形框
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, str(class_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('Annotated Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 使用示例
image_file = './data/mydata/train/images/1_jpg.rf.330c46c5a4bf31429a2a743b339bfa78_3.jpg'
annotation_file = './data/mydata/train/labels/1_jpg.rf.330c46c5a4bf31429a2a743b339bfa78_3.txt'
visualize_annotations(image_file, annotation_file)