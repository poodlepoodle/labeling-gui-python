from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import cv2
import glob
import os
import numpy as np

class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.upload_list = {}

        self.base_path = os.path.join(os.getcwd(), 'inputs')
        self.img_list = glob.glob(os.path.join(self.base_path, '*.jpg'))
        self.img_list.sort()
        self.pos = 0
        self.total = len(self.img_list)
        print(f"* Total Images : {self.total}")

        self.setWindowTitle("Image Labeling Tool v0.0.1 (poodlepoodle)")

        self.width = 620
        self.height = 620
        self.resize(self.width, self.height)
        
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.img_list[self.pos]).scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label.setPixmap(self.pixmap)
        self.label.adjustSize()
        
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open New Image')
        openAction.triggered.connect(self.loadImage)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)

    def loadImage(self):
        # print(f'* Img load : {self.img_list[self.pos]}')
        self.pixmap = QPixmap(self.img_list[self.pos]).scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label.setPixmap(self.pixmap)
        self.label.adjustSize()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Left:
            if not self.pos == 0:
                self.pos -= 1
                self.loadImage()
                                                
        elif e.key() == Qt.Key_Right:
            self.pos += 1
            self.loadImage()

        elif e.key() == Qt.Key_Up:
            print(f"* {self.img_list[self.pos]} -> up")
            self.upload_list[self.img_list[self.pos]] = 'up'
            self.pos += 1
            self.loadImage()

        elif e.key() == Qt.Key_Down:
            print(f"* {self.img_list[self.pos]} -> down")
            self.upload_list[self.img_list[self.pos]] = 'down'
            self.pos += 1
            self.loadImage()

        elif e.key() == Qt.Key_X:
            print(f"* {self.img_list[self.pos]} -> excluse from list")
            self.upload_list[self.img_list[self.pos]] = 'exclude'
            self.pos += 1
            self.loadImage()

        elif e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.uploadImage()

            self.upload_list = {}
            self.img_list = glob.glob(os.path.join(self.base_path, '*.jpg'))
            self.img_list.sort()
            self.pos = 0
            self.total = len(self.img_list)
            print(f"* Total Images : {self.total}")

            self.loadImage()

    def uploadImage(self):
        print("#---------- upload list ----------#")
        for key, item in sorted(self.upload_list.items(), key=lambda x:x[1]):
            os.system("mv " + key + " " + os.path.join(os.getcwd(), 'outputs', item))
            # print("mv " + key + " " + os.path.join(os.getcwd(), 'output', item))
            print(f"successfully moved {key} -> {item}")
        print("#---------------------------------#")

if __name__ == '__main__':
    import sys
    
    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())