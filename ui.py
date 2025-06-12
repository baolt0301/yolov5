import sys
import cv2
import torch
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QVBoxLayout, QWidget, QFileDialog, QComboBox)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
import numpy as np

# 在类初始化时添加模型选择
def chushihua_model(self):


def change_model(self, index):
    models = ["yolov5s", "yolov5m", "yolov5l"]
    self.model = torch.hub.load('ultralytics/yolov5', models[index])
# 加载YOLOv5模型
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

class DetectionThread(QThread):
    finished = pyqtSignal(np.ndarray, float)  # 发送处理后的图像和耗时

    
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

    def run(self):
        start_time = time.time()
        results = model(self.frame)
        processed_frame = results.render()[0]
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        end_time = time.time()
        self.finished.emit(processed_frame, end_time - start_time)

class VideoProcessor(QThread):
    frame_processed = pyqtSignal(np.ndarray, float)

    def __init__(self, source):
        super().__init__()
        self.source = source
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.source)
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            start_time = time.time()
            results = model(frame)
            processed_frame = results.render()[0]
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            end_time = time.time()
            
            self.frame_processed.emit(processed_frame, end_time - start_time)
            
        cap.release()

    def stop(self):
        self.running = False

class YOLOv5App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv5 检测系统")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化变量
        self.current_mode = "image"
        self.video_processor = None
        self.camera_processor = None
        self.camera_index = 0
        
        # 创建UI
        self.init_ui()
        
    def init_ui(self):
        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 模式选择
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["图片检测", "视频检测", "摄像头检测"])
        self.mode_combo.currentIndexChanged.connect(self.change_mode)
        layout.addWidget(self.mode_combo)

        # 摄像头设备选择
        self.camera_combo = QComboBox()
        self.refresh_camera_list()
        layout.addWidget(self.camera_combo)

        # 图像显示
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)
        layout.addWidget(self.image_label)

        # 时间显示
        self.time_label = QLabel("处理时间: 0.00s")
        layout.addWidget(self.time_label)

        # 控制按钮
        self.control_btn = QPushButton("打开文件")
        self.control_btn.clicked.connect(self.handle_control)
        layout.addWidget(self.control_btn)

        # 停止按钮
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)

    def refresh_camera_list(self):
        self.camera_combo.clear()
        for i in range(4):  # 检查前4个摄像头设备
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.camera_combo.addItem(f"摄像头 {i}")
                cap.release()

    def change_mode(self, index):
        modes = ["image", "video", "camera"]
        self.current_mode = modes[index]
        self.control_btn.setText({
            0: "打开图片",
            1: "打开视频",
            2: "启动摄像头"
        }[index])

    def handle_control(self):
        if self.current_mode == "image":
            self.open_image()
        elif self.current_mode == "video":
            self.open_video()
        elif self.current_mode == "camera":
            self.start_camera()

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "图片文件 (*.png *.jpg *.jpeg)")
        if path:
            frame = cv2.imread(path)
            self.process_frame(frame)

    def open_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开视频", "", "视频文件 (*.mp4 *.avi *.mov)")
        if path:
            self.stop_processing()
            self.video_processor = VideoProcessor(path)
            self.video_processor.frame_processed.connect(self.update_frame)
            self.video_processor.start()
            self.toggle_controls(True)

    def start_camera(self):
        self.camera_index = self.camera_combo.currentIndex()
        self.stop_processing()
        self.camera_processor = VideoProcessor(self.camera_index)
        self.camera_processor.frame_processed.connect(self.update_frame)
        self.camera_processor.start()
        self.toggle_controls(True)

    def process_frame(self, frame):
        thread = DetectionThread(frame)
        thread.finished.connect(self.update_frame)
        thread.start()

    def update_frame(self, frame, process_time):
        # 显示处理时间
        self.time_label.setText(f"处理时间: {process_time:.2f}s")
        
        # 转换并显示图像
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img).scaled(
            self.image_label.size(), Qt.KeepAspectRatio))

    def toggle_controls(self, processing):
        self.stop_btn.setEnabled(processing)
        self.control_btn.setEnabled(not processing)
        self.mode_combo.setEnabled(not processing)

    def stop_processing(self):
        if self.video_processor:
            self.video_processor.stop()
        if self.camera_processor:
            self.camera_processor.stop()
        self.toggle_controls(False)

    def closeEvent(self, event):
        self.stop_processing()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YOLOv5App()
    window.show()
    sys.exit(app.exec_())