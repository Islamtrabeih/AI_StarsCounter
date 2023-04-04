from PyQt5 import QtCore, QtGui, QtWidgets
from skimage.feature import blob_log
from skimage.io import imread
import matplotlib.pyplot as plt



class Ui_Star_counter(object):
    def setupUi(self, Star_counter):
        Star_counter.setWindowModality(QtCore.Qt.ApplicationModal)
        Star_counter.setEnabled(True)
        Star_counter.resize(750, 540)
        Star_counter.setWindowIcon(QtGui.QIcon("Image.png"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Star_counter.sizePolicy().hasHeightForWidth())
        Star_counter.setSizePolicy(sizePolicy)
        Star_counter.setMinimumSize(QtCore.QSize(750, 540))
        Star_counter.setMaximumSize(QtCore.QSize(750, 540))
        self.gridLayoutWidget = QtWidgets.QWidget(Star_counter)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 731, 521))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = MyGraphicsView()
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing, False)
        self.graphicsView.viewport().setCursor(QtCore.Qt.CrossCursor)
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 3)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setText("Please select an Image File")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.gridLayout.addWidget(self.toolButton, 0, 2, 1, 1)
        self.round_button = QtWidgets.QPushButton("Retry", self.gridLayoutWidget)
        self.round_button.setGeometry(3, int(self.gridLayoutWidget.sizeHint().height()/2 + 100), 50, 50)
        self.round_button.setStyleSheet("QPushButton {border-radius : 25; background-color: #FFB84C; border: 2px solid #ECF9FF} QPushButton:pressed { background-color: #EACFD1; border: 2px solid #FF597B} QPushButton:hover {border : 2px solid #EACFD1}")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox.setSingleStep(0.01)
        self.gridLayout.addWidget(self.doubleSpinBox, 2, 2, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)

        # lightpalette = QtGui.QPalette()
        # lightpalette.setColor(QtGui.QPalette.Window, QtGui.QColor(250, 251, 252))
        # lightpalette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
        # lightpalette.setColor(QtGui.QPalette.Base, QtGui.QColor(242, 214, 216))
        # lightpalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(250, 251, 252))
        # lightpalette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        # lightpalette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.black)
        # lightpalette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
        # lightpalette.setColor(QtGui.QPalette.Button, QtGui.QColor(250, 251, 252))
        # lightpalette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.black)
        # lightpalette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        # lightpalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(255, 99, 99))
        # lightpalette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        # app.setPalette(lightpalette)

        self.path = None

        def open_file():
            global pic
            self.file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", "Image Files (*.Jpg)")
            if self.file_name[0] != '':
                self.path = self.file_name[0]
                self.lineEdit.setText(self.file_name[0])
                scene = QtWidgets.QGraphicsScene()
                pic = QtGui.QPixmap(self.file_name[0])
                scene.addPixmap(pic)
                self.graphicsView.setScene(scene)

        def retry():
            self.lineEdit.setText("Please select an Image File")
            self.lineEdit_2.setText("")
            scene = QtWidgets.QGraphicsScene()
            scene.addPixmap(QtGui.QPixmap(None))
            self.graphicsView.setScene(scene)

        def process():
            if self.path == None:
                self.lineEdit_2.setText("Please select an Image File")
            elif self.doubleSpinBox.value() == 0.00:
                self.lineEdit_2.setText("Please update the threshold")
            else:
                image = imread(self.path, as_gray=True)
                thrsd = self.doubleSpinBox.value()
                log_b = blob_log(image, max_sigma=30, num_sigma=10, threshold=thrsd)
                nstar = len(log_b)
                self.lineEdit_2.setText(f'{nstar} Star')
                fig, ax = plt.subplots(1, figsize=(17, 10))
                ax.set_aspect('equal')
                ax.imshow(image)
                for xx, yy, rr in log_b:
                    c = plt.Circle((yy, xx), rr,  fill = False)
                    ax.add_patch(c)
                plt.savefig('result.jpg')
                scene = QtWidgets.QGraphicsScene()
                pic = QtGui.QPixmap("result.jpg")
                scene.addPixmap(pic)
                self.graphicsView.setScene(scene)

        self.toolButton.clicked.connect(open_file)
        self.round_button.clicked.connect(retry)
        self.pushButton.clicked.connect(process)
        self.retranslateUi(Star_counter)
        QtCore.QMetaObject.connectSlotsByName(Star_counter)

    def retranslateUi(self, Star_counter):
        _translate = QtCore.QCoreApplication.translate
        Star_counter.setWindowTitle(_translate("Star_counter", "Stars_counter"))
        self.label.setText(_translate("Star_counter", "Image :"))
        self.toolButton.setText(_translate("Star_counter", "+"))
        self.pushButton.setText(_translate("Star_counter", "Process"))



class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self):
        super(MyGraphicsView, self).__init__()
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self._isPanning = False
        self._mousePressed = False
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)

    def mousePressEvent(self,  event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mousePressed = True
            self._startPos = event.pos()
            pos[0] = self._startPos.x()
            pos[1] = self._startPos.y()
            if self._isPanning:
                event.accept()
            else:
                super(MyGraphicsView, self).mousePressEvent(event)
        elif event.button() == QtCore.Qt.MiddleButton:
            self._mousePressed = True
            self._isPanning = True

    def mouseMoveEvent(self, event):
        if self._mousePressed and self._isPanning:
            event.accept()
        else:
            if pic == None:
                pass
            else:
                self._endPos = event.pos()
                pos[2] = self._endPos.x()
                pos[3] = self._endPos.y()
                self.crop()
            super(MyGraphicsView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(MyGraphicsView, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
        pass

    def wheelEvent(self,  event):
        # zoom factor
        factor = 1.1
        # Set Anchors
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        # Save the scene pos
        oldPos = self.mapToScene(event.pos())
        # Zoom
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)
        # Get the new position
        newPos = self.mapToScene(event.pos())
        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

    def crop(self):
        polygon = QtCore.QRectF(pos[0], pos[1], pos[2] - pos[0], pos[3] - pos[1])
        path = QtGui.QPainterPath()
        path.addRect(polygon)
        source = pic
        r = path.boundingRect().toRect().intersected(source.rect())
        pixmap = QtGui.QPixmap(source.size())
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setClipPath(path)
        painter.drawPixmap(QtCore.QPoint(), source, source.rect())
        painter.end()
        result = pixmap.copy(r)
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(result)
        self.setScene(scene)



pos = [0, 0, 0, 0]
pic = None

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Star_counter = QtWidgets.QWidget()
    ui = Ui_Star_counter()
    ui.setupUi(Star_counter)
    Star_counter.show()
    sys.exit(app.exec_())
