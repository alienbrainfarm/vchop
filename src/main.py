import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QListWidgetItem, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov']

class VideoBrowser(QMainWindow):
    def __init__(self, start_dir=None):
        super().__init__()
        self.setWindowTitle('vchop - Video Browser')
        self.setGeometry(100, 100, 800, 600)
        self.list_widget = QListWidget()
        self.setCentralWidget(self.list_widget)
        self.create_menu()
        if start_dir:
            self.open_directory(start_dir)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        open_action = QAction('Open Directory', self)
        open_action.triggered.connect(self.select_directory)
        file_menu.addAction(open_action)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            self.open_directory(dir_path)

    def open_directory(self, dir_path):
        self.list_widget.clear()
        for filename in os.listdir(dir_path):
            if any(filename.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
                item = QListWidgetItem(filename)
                item.setIcon(QIcon.fromTheme('video-x-generic'))
                item.setSizeHint(QSize(100, 100))
                self.list_widget.addItem(item)

if __name__ == '__main__':
    start_dir = sys.argv[1] if len(sys.argv) > 1 else None
    app = QApplication(sys.argv)
    window = VideoBrowser(start_dir)
    window.show()
    sys.exit(app.exec_())
