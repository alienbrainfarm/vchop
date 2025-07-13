import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QListWidgetItem, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
import cv2
from PIL import Image
import json
from pathlib import Path
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import shutil

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov']
THUMBNAIL_SIZE = (200, 200)
THUMBNAIL_DIR = '.vchop/thumbnails'
RECENT_DIRS_PATH = Path.home() / '.vchop' / 'recent_dirs.json'
MAX_RECENT = 5

class VideoBrowser(QMainWindow):
    def __init__(self, start_dir=None):
        super().__init__()
        self.setWindowTitle('vchop - Video Browser')
        self.setGeometry(100, 100, 800, 600)
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setSpacing(10)
        self.list_widget.setStyleSheet('background-color: black;')  # Set black background
        self.setCentralWidget(self.list_widget)
        self.recent_dirs = self.load_recent_dirs()
        self.create_menu()
        if start_dir:
            self.open_directory(start_dir)
            self.update_recent_dirs(start_dir)
        elif self.recent_dirs:
            self.open_directory(self.recent_dirs[0])
        # else: wait for user to select

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        open_action = QAction('Open Directory', self)
        open_action.triggered.connect(self.select_directory)
        file_menu.addAction(open_action)
        # Add recent dirs submenu
        recent_menu = file_menu.addMenu('Recent Directories')
        for dir_path in self.recent_dirs:
            action = QAction(dir_path, self)
            action.triggered.connect(lambda checked, d=dir_path: self.open_directory(d))
            recent_menu.addAction(action)
        # Add Actions dropdown
        actions_menu = menubar.addMenu('Actions')
        split_action = QAction('Split by Scenes', self)
        split_action.triggered.connect(self.split_by_scenes)
        actions_menu.addAction(split_action)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            self.open_directory(dir_path)
            self.update_recent_dirs(dir_path)

    def load_recent_dirs(self):
        try:
            if RECENT_DIRS_PATH.exists():
                with open(RECENT_DIRS_PATH, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def update_recent_dirs(self, dir_path):
        dirs = [dir_path] + [d for d in self.recent_dirs if d != dir_path]
        self.recent_dirs = dirs[:MAX_RECENT]
        RECENT_DIRS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RECENT_DIRS_PATH, 'w') as f:
            json.dump(self.recent_dirs, f)

    def open_directory(self, dir_path):
        self.list_widget.clear()
        thumb_dir = os.path.join(dir_path, THUMBNAIL_DIR)
        os.makedirs(thumb_dir, exist_ok=True)
        for filename in os.listdir(dir_path):
            if any(filename.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
                filepath = os.path.join(dir_path, filename)
                thumb_path = os.path.join(thumb_dir, f'{filename}.png')
                if not os.path.exists(thumb_path):
                    try:
                        cap = cv2.VideoCapture(filepath)
                        success, frame = cap.read()
                        cap.release()
                        if success:
                            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                            img.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)  # Resize, preserve aspect ratio
                            bg = Image.new('RGB', THUMBNAIL_SIZE, (0, 0, 0))  # Black background
                            x = (THUMBNAIL_SIZE[0] - img.width) // 2
                            y = (THUMBNAIL_SIZE[1] - img.height) // 2
                            bg.paste(img, (x, y))  # Center the image
                            bg.save(thumb_path)
                    except Exception as e:
                        thumb_path = None
                if os.path.exists(thumb_path):
                    pixmap = QPixmap(thumb_path)
                else:
                    pixmap = QPixmap()
                item = QListWidgetItem(filename)
                item.setIcon(QIcon(pixmap))
                item.setSizeHint(QSize(THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
                self.list_widget.addItem(item)

    def split_by_scenes(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection', 'Please select a video to split by scenes.')
            return
        filename = selected_items[0].text()
        dir_path = self.recent_dirs[0] if self.recent_dirs else None
        if not dir_path:
            QMessageBox.warning(self, 'No Directory', 'No directory found for splitting.')
            return
        filepath = os.path.join(dir_path, filename)
        # Ask user for output directory
        output_dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory for Scenes')
        if not output_dir:
            QMessageBox.information(self, 'Scene Split', 'No output directory selected.')
            return
        output_dir = os.path.join(output_dir, f'{filename}_scenes')
        os.makedirs(output_dir, exist_ok=True)
        try:
            from scenedetect import VideoManager, SceneManager
            from scenedetect.detectors import ContentDetector
            video_manager = VideoManager([filepath])
            scene_manager = SceneManager()
            scene_manager.add_detector(ContentDetector())
            video_manager.start()
            scene_manager.detect_scenes(frame_source=video_manager)
            scene_list = scene_manager.get_scene_list()
            if not scene_list:
                QMessageBox.information(self, 'Scene Split', 'No scenes detected.')
                return
            # Split video by scenes
            for i, (start, end) in enumerate(scene_list):
                out_path = os.path.join(output_dir, f'scene_{i+1}.mp4')
                start_time = start.get_seconds()
                duration = end.get_seconds() - start.get_seconds()
                cmd = f'ffmpeg -y -i "{filepath}" -ss {start_time} -t {duration} -c copy "{out_path}"'
                os.system(cmd)
            QMessageBox.information(self, 'Scene Split', f'Split into {len(scene_list)} scenes. Output: {output_dir}')
        except Exception as e:
            QMessageBox.critical(self, 'Scene Split Error', str(e))

if __name__ == '__main__':
    start_dir = sys.argv[1] if len(sys.argv) > 1 else None
    app = QApplication(sys.argv)
    window = VideoBrowser(start_dir)
    window.show()
    sys.exit(app.exec_())
