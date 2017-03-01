from matplotlib.figure import Figure

_author__ = "Saulius Lukse"
__copyright__ = "Copyright 2016, kurokesu.com"
__version__ = "0.1"
__license__ = "GPL"

from PyQt4 import QtCore, QtGui, uic
import sys
import cv2
import numpy as np
import threading
import time
import Queue
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from TempHistory import TempHistory

running = False
capture_thread = None
form_class = uic.loadUiType("simple.ui")[0]
q = Queue.Queue()


def grab(cam, queue, width, height, fps):
    global running
    capture = cv2.VideoCapture(cam)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, fps)

    while (running):
        frame = {}
        capture.grab()
        retval, img = capture.retrieve(0)
        frame["img"] = img

        if queue.qsize() < 10:
            queue.put(frame)
        else:
            print queue.qsize()

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, *args, **kwargs):
        fig = Figure(figsize=(5, 3), dpi=100)
        self.axes = fig.add_subplot(111)
        self.figure = fig

        super(MplCanvas, self).__init__(fig)
        self.setParent(kwargs['parent'])
        FigureCanvasQTAgg.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

class TempCanvas(MplCanvas):
    def __init__(self, *args, **kwargs):
        fsize = 10
        super(TempCanvas, self).__init__(*args, **kwargs)
        self.axes.set_title(kwargs['title'], fontsize=fsize)

        self.axes.set_ylabel("Temp(celsius)", fontsize=fsize)
        self.axes.grid(True, linestyle='-', color='0.75')
        self.axes.get_xaxis().set_ticks([])
        self.axes.tick_params(axis='both', which='major', labelsize=fsize - 2)
        self.axes.tick_params(axis='both', which='minor', labelsize=fsize - 2)
        self.th = TempHistory((self.figure, self.axes))



class OwnImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.startButton.clicked.connect(self.start_clicked)
        self.main_widget = QtGui.QWidget(self)

        self.window_width = self.ImgWidget.frameSize().width()
        self.window_height = self.ImgWidget.frameSize().height()
        self.ImgWidget = OwnImageWidget(self.ImgWidget)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
        self.verticalLayout.addWidget(TempCanvas(title="random high", parent=self.main_widget))
        self.verticalLayout.addWidget(TempCanvas(title="random average", parent=self.main_widget))

    def start_clicked(self):
        global running
        running = True
        capture_thread.start()
        self.startButton.setEnabled(False)
        self.startButton.setText('Starting...')

    def update_frame(self):
        if not q.empty():
            self.startButton.setText('Camera is live')
            frame = q.get()
            img = frame["img"]

            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
            self.ImgWidget.setImage(image)

    def closeEvent(self, event):
        global running
        running = False


capture_thread = threading.Thread(target=grab, args=(0, q, 1920, 1080, 30))

app = QtGui.QApplication(sys.argv)
w = MyWindowClass(None)
w.setWindowTitle('Kurokesu PyQT OpenCV USB camera test panel')
w.show()
app.exec_()

