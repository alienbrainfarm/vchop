from PyQt5.QtWidgets import QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QPushButton, QWidget, QFileDialog, QMessageBox, QMenuBar, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
import os
import subprocess

class SceneListWidget(QListWidget):
    def __init__(self, parent=None, update_callback=None):
        super().__init__(parent)
        self.update_callback = update_callback

    def dropEvent(self, event):
        super().dropEvent(event)
        if self.update_callback:
            self.update_callback()


class SceneManagerWindow(QMainWindow):
    def __init__(self, scene_files, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Scene Manager')
        self.setGeometry(200, 200, 900, 600)
        self.scene_files = scene_files.copy()
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.list_widget = SceneListWidget(update_callback=self.sync_scene_files_with_widget)
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(200, 200))
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_widget.setSpacing(10)
        layout.addWidget(self.list_widget)
        
        # Add export button
        self.export_btn = QPushButton('Export All Scenes to Video')
        self.export_btn.clicked.connect(self.export_scenes)
        layout.addWidget(self.export_btn)
        
        # Add export selected button
        self.export_selected_btn = QPushButton('Export Selected Scenes to Video')
        self.export_selected_btn.clicked.connect(self.export_selected_scenes)
        layout.addWidget(self.export_selected_btn)
        
        self.populate_list()
        self.list_widget.installEventFilter(self)
        # No need to connect rowsMoved; handled by dropEvent
    def sync_scene_files_with_widget(self):
        # Update self.scene_files to match QListWidget order
        new_order = []
        for i in range(self.list_widget.count()):
            name = self.list_widget.item(i).text()
            for f in self.scene_files:
                if os.path.basename(f) == name:
                    new_order.append(f)
                    break
        self.scene_files = new_order

    def populate_list(self):
        from video_utils import get_thumbnail_path, create_thumbnail, THUMBNAIL_DIR
        self.list_widget.clear()
        for scene_file in self.scene_files:
            item = QListWidgetItem(os.path.basename(scene_file))
            
            # Use unified thumbnail cache location with blue border
            scene_dir = os.path.dirname(scene_file)
            thumb_dir = os.path.join(scene_dir, THUMBNAIL_DIR)
            os.makedirs(thumb_dir, exist_ok=True)
            thumb_path = get_thumbnail_path(scene_file, thumb_dir)
            
            if not os.path.exists(thumb_path):
                try:
                    create_thumbnail(scene_file, thumb_path, border_color=(0, 0, 255))  # Blue border for scene mode
                except Exception:
                    pass
            
            if os.path.exists(thumb_path):
                pixmap = QPixmap(thumb_path)
                item.setIcon(QIcon(pixmap))
            self.list_widget.addItem(item)

    def eventFilter(self, source, event):
        if source is self.list_widget and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Delete:
                for item in self.list_widget.selectedItems():
                    row = self.list_widget.row(item)
                    self.list_widget.takeItem(row)
                return True
        return super().eventFilter(source, event)

    def export_scenes(self):
        # Get reordered scene files
        reordered = []
        for i in range(self.list_widget.count()):
            name = self.list_widget.item(i).text()
            for f in self.scene_files:
                if os.path.basename(f) == name:
                    reordered.append(f)
                    break
        if not reordered:
            QMessageBox.warning(self, 'No Scenes', 'No scenes to export.')
            return
        output_file, _ = QFileDialog.getSaveFileName(self, 'Save Reordered Video', '', 'MP4 Files (*.mp4)')
        if not output_file:
            return
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            concat_file = os.path.join(tmpdir, 'concat.txt')
            with open(concat_file, 'w') as f:
                for pf in reordered:
                    f.write(f"file '{pf}'\n")
            cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output_file]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                QMessageBox.information(self, 'Export Complete', f'Exported to {output_file}')
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'Export Failed', f'FFmpeg failed: {e.stderr}')
            except FileNotFoundError:
                QMessageBox.critical(self, 'Export Failed', 'FFmpeg not found. Please install FFmpeg.')

    def export_selected_scenes(self):
        """Export only the selected scenes to a video file."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection', 'Please select scenes to export.')
            return
            
        # Get selected scene files in their current order
        selected_files = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.isSelected():
                name = item.text()
                for f in self.scene_files:
                    if os.path.basename(f) == name:
                        selected_files.append(f)
                        break
        
        if not selected_files:
            QMessageBox.warning(self, 'No Scenes', 'No valid scenes found to export.')
            return
            
        output_file, _ = QFileDialog.getSaveFileName(self, 'Save Selected Scenes Video', '', 'MP4 Files (*.mp4)')
        if not output_file:
            return
            
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            concat_file = os.path.join(tmpdir, 'concat.txt')
            with open(concat_file, 'w') as f:
                for pf in selected_files:
                    f.write(f"file '{pf}'\n")
            cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output_file]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                QMessageBox.information(self, 'Export Complete', 
                                      f'Exported {len(selected_files)} selected scenes to:\n{output_file}')
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'Export Failed', f'FFmpeg failed: {e.stderr}')
            except FileNotFoundError:
                QMessageBox.critical(self, 'Export Failed', 'FFmpeg not found. Please install FFmpeg.')
