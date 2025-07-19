from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QWidget, QLabel, QFileDialog
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import os
import subprocess
import tempfile

class VideoEditorWindow(QMainWindow):
    def __init__(self, video_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Edit: {os.path.basename(video_path)}')
        self.setGeometry(150, 150, 700, 500)
        self.video_path = video_path
        self.scene_list = []
        self.selected_scenes = set()
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.info_label = QLabel('Analyze and split scenes, or chain scenes together.')
        layout.addWidget(self.info_label)
        self.scene_list_widget = QListWidget()
        layout.addWidget(self.scene_list_widget)
        btn_layout = QHBoxLayout()
        self.analyze_btn = QPushButton('Analyze Scenes')
        self.analyze_btn.clicked.connect(self.analyze_scenes)
        btn_layout.addWidget(self.analyze_btn)
        self.split_btn = QPushButton('Split Scenes')
        self.split_btn.clicked.connect(self.split_scenes)
        btn_layout.addWidget(self.split_btn)
        self.chain_btn = QPushButton('Chain Selected Scenes')
        self.chain_btn.clicked.connect(self.chain_scenes)
        btn_layout.addWidget(self.chain_btn)
        layout.addLayout(btn_layout)
        self.scene_list_widget.setSelectionMode(QListWidget.MultiSelection)

    def analyze_scenes(self):
        try:
            from scenedetect import open_video, SceneManager
            from scenedetect.detectors import ContentDetector
            video = open_video(self.video_path)
            scene_manager = SceneManager()
            scene_manager.add_detector(ContentDetector())
            scene_manager.detect_scenes(video)
            self.scene_list = scene_manager.get_scene_list()
            self.scene_list_widget.clear()
            for i, (start, end) in enumerate(self.scene_list):
                self.scene_list_widget.addItem(f'Scene {i+1}: {start.get_timecode()} - {end.get_timecode()}')
            self.info_label.setText(f'Found {len(self.scene_list)} scenes.')
        except Exception as e:
            self.info_label.setText(f'Error: {e}')

    def split_scenes(self):
        if not self.scene_list:
            self.info_label.setText('No scenes to split. Analyze first.')
            return
        output_dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory for Scenes')
        if not output_dir:
            self.info_label.setText('No output directory selected.')
            return
        scene_files = []
        import cv2
        from PIL import Image
        for i, (start, end) in enumerate(self.scene_list):
            out_path = os.path.join(output_dir, f'scene_{i+1:07d}.mp4')
            start_time = start.get_seconds()
            duration = end.get_seconds() - start.get_seconds()
            cmd = f'ffmpeg -y -i "{self.video_path}" -ss {start_time} -t {duration} -c copy "{out_path}"'
            subprocess.call(cmd, shell=True)
            scene_files.append(out_path)
            # Generate thumbnail for each scene if not present
            thumb_path = out_path + '.png'
            if not os.path.exists(thumb_path):
                cap = cv2.VideoCapture(out_path)
                success, frame = cap.read()
                cap.release()
                if success:
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    img.thumbnail((200, 200), Image.LANCZOS)
                    bg = Image.new('RGB', (200, 200), (0, 0, 0))
                    x = (200 - img.width) // 2
                    y = (200 - img.height) // 2
                    bg.paste(img, (x, y))
                    bg.save(thumb_path)
        self.info_label.setText(f'Split into {len(self.scene_list)} scenes.')
        # Open scene manager window
        from scene_manager_window import SceneManagerWindow
        self.scene_manager = SceneManagerWindow(scene_files, self)
        self.scene_manager.show()
        self.scene_manager.raise_()
        self.scene_manager.activateWindow()

    def chain_scenes(self):
        selected = self.scene_list_widget.selectedIndexes()
        if not selected:
            self.info_label.setText('Select scenes to chain.')
            return
        output_file, _ = QFileDialog.getSaveFileName(self, 'Save Chained Video', '', 'MP4 Files (*.mp4)')
        if not output_file:
            self.info_label.setText('No output file selected.')
            return
        with tempfile.TemporaryDirectory() as tmpdir:
            part_files = []
            for idx in selected:
                i = idx.row()
                start, end = self.scene_list[i]
                out_path = os.path.join(tmpdir, f'part_{i+1}.mp4')
                start_time = start.get_seconds()
                duration = end.get_seconds() - start.get_seconds()
                cmd = f'ffmpeg -y -i "{self.video_path}" -ss {start_time} -t {duration} -c copy "{out_path}"'
                subprocess.call(cmd, shell=True)
                part_files.append(out_path)
            concat_file = os.path.join(tmpdir, 'concat.txt')
            with open(concat_file, 'w') as f:
                for pf in part_files:
                    f.write(f"file '{pf}'\n")
            cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_file}" -c copy "{output_file}"'
            subprocess.call(cmd, shell=True)
        self.info_label.setText(f'Chained {len(selected)} scenes to {output_file}')
