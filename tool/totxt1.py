import xml.etree.ElementTree as ET
import os
from os import getcwd
import glob

# 1. 定义文件夹路径
image_set = r'labels'  # 存放XML文件的文件夹
imageset2 = r'1'       # 保存TXT文件的文件夹

# 2. 修正类别顺序：与TXT中的类别ID完全匹配（green=0, red=1, yellow=2）
classes = ['green', 'red', 'yellow']  # 注意：顺序不可错，对应YOLO的类别ID 0,1,2

# 3. 数据集根目录
data_dir = r'./data/train'

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(data_dir, imageset1, imageset2, image_id):
    in_file = open(data_dir + '/%s/%s.xml' % (imageset1, image_id), encoding='UTF-8')
    out_file = open(data_dir + '/%s/%s.txt' % (imageset2, image_id), 'w', encoding='UTF-8')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text.lower()  # 统一转为小写，确保匹配
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)  # 根据列表顺序生成类别ID（green=0, red=1, yellow=2）
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str('%.6f' % a) for a in bb]) + '\n')

# 获取所有XML文件
image_ids = [os.path.basename(x)[:-4] for x in glob.glob(data_dir + '/%s/*.xml' % image_set)]
print('\n%s数量:' % image_set, len(image_ids))

# 转换每个文件
for i, image_id in enumerate(image_ids, 1):
    convert_annotation(data_dir, image_set, imageset2, image_id)
    print("%s 数据:%s/%s文件完成！" % (image_set, i, len(image_ids)))

print("Done!!!")