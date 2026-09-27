import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLabel, QHBoxLayout, QVBoxLayout, QFileDialog

from PyQt5.QtGui import QPixmap, QMovie

from PIL import Image, ImageFilter, ImageSequence

app = QApplication([])  #Я подключаю pyqt5
window = QWidget()# Создание окна
window.setWindowTitle("Easy Editor")# Название окна
window.resize(900, 600)# Размер окна

btn_dir = QPushButton("Папка")# создание кнопки
lw_files = QListWidget()# Создание листа

lb_image = QLabel("Картинка")# Создание основного лэйбла (картинки)
lb_image.setAlignment(Qt.AlignCenter)# перемещение в центр

#создание кнопок
btn_left = QPushButton("Лево")
btn_right = QPushButton("Право")
btn_flip = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/б")
btn_save = QPushButton("Сохранить")


# Левая колонка
layout_left = QVBoxLayout()
layout_left.addWidget(btn_dir)
layout_left.addWidget(lw_files)

layout_actions = QHBoxLayout()
layout_actions.addWidget(btn_left)
layout_actions.addWidget(btn_right)
layout_actions.addWidget(btn_flip)
layout_actions.addWidget(btn_sharp)
layout_actions.addWidget(btn_bw)
layout_actions.addWidget(btn_save)

layout_right = QVBoxLayout()
layout_right.addWidget(lb_image, stretch=5)
layout_right.addLayout(layout_actions)

main_layout = QHBoxLayout()
main_layout.addLayout(layout_left, stretch=1)
main_layout.addLayout(layout_right, stretch=4)

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
                break
    return result


def showFilenamesList():
    chooseWorkdir()
    if workdir:
        all_files = os.listdir(workdir)
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.JPG', '.JPEG', '.PNG', '.BMP', '.GIF']
        image_files = filter(all_files, extensions)
        lw_files.clear()
        lw_files.addItems(image_files)

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = "Modified/"
        self.movie = None
    
    def load_image(self, filename):
        self.filename = filename
        path = os.path.join(workdir, filename)
        if not filename.lower().endswith('.gif'):
            self.image = Image.open(path)
        else:
            self.image = None

    def show_image(self, path):
        lb_image.hide()
        if self.movie:
            self.movie.stop()
            self.movie = None
            lb_image.setMovie(None)

        w = lb_image.width()
        h = lb_image.height()

        if path.lower().endswith('.gif'):
            self.movie = QMovie(path)
            
            self.movie.setScaledSize(lb_image.size().scaled(w, h, Qt.KeepAspectRatio))
            lb_image.setMovie(self.movie)
            lb_image.show()
            self.movie.start()
        else:
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lb_image.setPixmap(pixmap)
            lb_image.show()

    def saveImage(self):
        if self.image:
            path = os.path.join(workdir, self.save_dir)
            if not os.path.exists(path):
                os.mkdir(path)
            full_path = os.path.join(path, self.filename)
            self.image.save(full_path)
            return full_path
        return None
    
    def do_bw(self):
        if self.image:
            self.image = self.image.convert('L')
            temp_path = self.saveImage()
            self.show_image(temp_path)

    def do_left(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            temp_path = self.saveImage()
            self.show_image(temp_path) 


    def do_right(self):
        if self.image:
            self.image = self.image.rotate(-90, expand=True)
            temp_path = self.saveImage()
            self.show_image(temp_path) 

    def do_sharpen(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            temp_path = self.saveImage()
            self.show_image(temp_path) 

    def do_flip(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            temp_path = self.saveImage()
            self.show_image(temp_path) 


workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.load_image(filename)
        full_path = os.path.join(workdir, filename)
        workimage.show_image(full_path)

btn_dir.clicked.connect(showFilenamesList)
lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_save.clicked.connect(workimage.saveImage)

window.setLayout(main_layout)
window.show()
app.exec_()
