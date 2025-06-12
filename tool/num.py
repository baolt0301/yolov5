import os

def get_every_class_num(txt_folder_path):
    # 需修改，根据自己的类别，注意一一对应
    class_categories = ['0', '1', '2']
    class_num = 3  # 样本类别数
    class_num_list = [0] * class_num

    # 获取文件夹下所有txt文件
    txt_files = [file for file in os.listdir(txt_folder_path) if file.endswith('.txt')]

    for txt_file in txt_files:
        file_path = os.path.join(txt_folder_path, txt_file)
        with open(file_path, 'r') as file:
            file_data = file.readlines()  # 读取所有行
            for every_row in file_data:
                class_str = every_row.split(' ')[0].strip()  # 去除换行符
                if class_str in class_categories:
                    class_ind = class_categories.index(class_str)
                    class_num_list[class_ind] += 1

    # 输出每一类的数量以及总数
    result = dict(zip(class_categories, class_num_list))
    for name, num in result.items():
        print(name, ":", num)
    print("-----------------------------------")
    print('total:', sum(class_num_list))

if __name__ == '__main__':
    # 需修改，txt文件夹所在路径
    txt_folder_path = r'.\data\mydata\valid\labels'
    get_every_class_num(txt_folder_path)

