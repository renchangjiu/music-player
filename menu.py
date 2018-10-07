import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from PyQt5.QtCore import QObject, Qt, QThread, QUrl, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QFont, QPalette, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QPushButton, QLineEdit, QInputDialog, QMainWindow, \
    QTextEdit, \
    QAction, QFileDialog, QLCDNumber, QSlider, QAbstractItemView, QComboBox, QSplitter, QDockWidget, QStackedWidget, \
    QListWidget, QLabel, QHBoxLayout, QMessageBox, QSpinBox, QMenu


class Menu(QMenu):
    leave = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def leaveEvent(self, QEvent):
        super().leaveEvent(QEvent)
        self.leave.emit()

# def main():
#     app = QApplication(sys.argv)
#     my_window = MyWindow()
#     my_window.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == "__main__":
#     main()
