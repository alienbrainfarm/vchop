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
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setSpacing(10)
        layout.addWidget(self.list_widget)
        
        # Add export button
        self.export_btn = QPushButton('Export Scenes to Video')
        self.export_btn.clicked.connect(self.export_scenes)
        layout.addWidget(self.export_btn)
        
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
        self.list_widget.clear()
        for scene_file in self.scene_files:
            item = QListWidgetItem(os.path.basename(scene_file))
            thumb_path = scene_file + '.png'
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
            cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_file}" -c copy "{output_file}"'
            subprocess.call(cmd, shell=True)
        QMessageBox.information(self, 'Export Complete', f'Exported to {output_file}')
