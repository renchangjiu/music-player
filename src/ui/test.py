import sys, configparser
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QProcess, QEvent, QSize, QPointF
from PyQt5.QtGui import QPixmap, QBrush, QFont, QColor, QIcon, QImage, QFontMetrics, QCursor, QLinearGradient, \
    QGradient, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QAbstractItemView, QListWidgetItem, QTableWidgetItem, \
    QAction, QMenu, QLabel, QCheckBox, QFileDialog

from PyQt5 import QtCore, QtGui, QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    # my_window = ChooseMusicDirPage()
    # my_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
