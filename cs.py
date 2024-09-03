import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QWidget, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5 import QtCore,QtGui
import qtawesome
import sys
import torch
import cv2
import os


# 继承QWidget，设计窗口
class fire(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # 构造图标文件的
        s_path = os.path.join(os.path.dirname(__file__), "system.png'")
        s_dir = os.path.dirname(s_path)#绝对路径
        system_path = os.path.join(s_dir, 'icon', 'system.png')
        self.image = QPixmap(system_path)
        hubconf_path = os.path.join(os.path.dirname(__file__), "hubconf.py")
        best_path = os.path.join(os.path.dirname(__file__), "best.pt")
        hubconf_dir = os.path.dirname(hubconf_path)  # 获取 hubconf.py 文件所在的目录
        self.model = torch.hub.load(hubconf_dir, 'custom', path=best_path, source='local')
        # print(hubconf_path)

    def initUI(self):
        # 设置窗口属性
        self.setFixedSize(960,700)
        i_path = os.path.join(os.path.dirname(__file__), "fire.png'")
        i_dir = os.path.dirname(i_path)#绝对路径
        icon_path = os.path.join(i_dir, 'icon', 'fire.png')
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle('森林火灾烟雾报警')

        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        self.middle_widget = QWidget()
        self.middle_widget.setObjectName('middle_widget')
        self.middle_layout = QGridLayout()
        self.middle_widget.setLayout(self.middle_layout)

        self.left_widget = QWidget()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        self.right_widget = QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        self.main_layout.addWidget(self.left_widget,0,0,8,6,Qt.AlignRight) # 左侧部件
        self.main_layout.addWidget(self.right_widget,0,6,8,6) # 右侧部件     
        
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        
        # 添加一个按钮
        self.btn_1 = QPushButton(qtawesome.icon('ei.picture',color='black'),"选择图片")
        self.btn_1.setObjectName('left_button')
        self.btn_1.clicked.connect(self.select_image)
        self.btn_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 添加一个按钮
        self.btn_2 = QPushButton(qtawesome.icon('ei.folder-open',color='yellow'),"存放路径")
        self.btn_2.setObjectName('right_button')
        self.btn_2.clicked.connect(self.select_save)
        self.btn_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 添加一个按钮
        self.btn_3 = QPushButton(qtawesome.icon('ei.camera',color='blue'),'打开摄像')
        self.btn_3.setObjectName('right_button')
        self.btn_3.clicked.connect(self.run_python_pi)
        self.btn_3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btn_4 = QPushButton(qtawesome.icon('fa.play',color='black'),'开始推理')
        self.btn_4.setObjectName('left_button')
        self.btn_4.clicked.connect(self.run_python_image)
        self.btn_4.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.left_layout.addWidget(self.btn_1,5,6,1,2)
        self.right_layout.addWidget(self.btn_2,5,7,1,2)
        self.left_layout.addWidget(self.btn_4,6,6,1,2)
        self.right_layout.addWidget(self.btn_3,6,7,1,2)

        self.image_path = ''
        self.save_dir = ''

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)#背景图片

    def run_python_image(self):
        if not self.image_path and self.save_dir:
            QMessageBox.warning(self, '错误', '请选择图片和存放目录')
            return
        img = cv2.imread(self.image_path)
        # 使用模型进行推理
        results = self.model(img)  # 根据旧版本进行推理
        # 保存结果
        results.save(self.save_dir)
        # cv2.imwrite(self.image_path, results)
        QMessageBox.information(self, '检测完成', f'结果已保存到: {self.save_dir}')
        # results.open(self.image_path)


    def select_image(self):
       # 打开文件对话框让用户选择图片
       self.image_path, _ = QFileDialog.getOpenFileName(self,'选择图片',QDir.homePath(), 'Images (*.png *.jpg *.jpeg)')
       if self.image_path:
            QMessageBox.information(self, '图片选择', f'选择的图片路径: {self.image_path}')


    def select_save(self):
        self.save_dir = QFileDialog.getExistingDirectory(self,'存放路径',QDir.homePath())
        if self.save_dir:
            QMessageBox.information(self, '图片选择', f'选择的存放路径: {self.save_dir}')
        
    def run_python_pi(self):

        script_path = os.path.join(os.path.dirname(__file__), "fire.py")
        subprocess.Popen(["python", script_path])  # 调用外部Python脚本
        print("打开成功")

    def show_message(self):
        QMessageBox.information(self, '提示', '打开成功')


# 创建应用程序并运行
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = fire()
    ex.show()
    sys.exit(app.exec_())
