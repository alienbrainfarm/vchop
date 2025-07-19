from PyQt5.QtWidgets import QMainWindow, QListWidget, QListWidgetItem, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
import os
from video_utils import VIDEO_EXTENSIONS, THUMBNAIL_SIZE, THUMBNAIL_DIR, load_recent_dirs, update_recent_dirs, is_video_file, create_thumbnail
from video_editor import VideoEditorWindow

class VideoBrowser(QMainWindow):
    def keyPressEvent(self, event):
        # Press 'j' to open join scenes editor from normal display
        if event.text() == 'j' and not hasattr(self, 'current_scene_files'):
            # Try to open the default scenes subdirectory if it exists
            base_dir = self.recent_dirs[0] if self.recent_dirs else os.getcwd()
            default_dir = os.path.join(base_dir, 'scenes')
            if os.path.exists(default_dir):
                self.show_scene_thumbnails(default_dir)
                return
        super().keyPressEvent(event)
    def eventFilter(self, source, event):
        # Handle '[' and ']' key for reordering when list_widget has focus
        if source is self.list_widget and event.type() == event.KeyPress:
            if hasattr(self, 'current_scene_files') and self.current_scene_files:
                selected = self.list_widget.currentRow()
                if selected == -1:
                    return False
                # Move up
                if event.text() == '[' and selected > 0:
                    self.current_scene_files[selected-1], self.current_scene_files[selected] = self.current_scene_files[selected], self.current_scene_files[selected-1]
                    self.save_scene_order(self.current_scene_dir, self.current_scene_files)
                    name = os.path.basename(self.current_scene_files[selected-1])
                    self.show_scene_thumbnails(self.current_scene_dir)
                    for i in range(self.list_widget.count()):
                        if self.list_widget.item(i).text() == name:
                            self.list_widget.setCurrentRow(i)
                            break
                    return True
                # Move down
                elif event.text() == ']' and selected < len(self.current_scene_files)-1:
                    self.current_scene_files[selected+1], self.current_scene_files[selected] = self.current_scene_files[selected], self.current_scene_files[selected+1]
                    self.save_scene_order(self.current_scene_dir, self.current_scene_files)
                    name = os.path.basename(self.current_scene_files[selected+1])
                    self.show_scene_thumbnails(self.current_scene_dir)
                    for i in range(self.list_widget.count()):
                        if self.list_widget.item(i).text() == name:
                            self.list_widget.setCurrentRow(i)
                            break
                    return True
                # Delete
                elif event.key() == Qt.Key_Delete:
                    file_to_delete = self.current_scene_files[selected]
                    thumb_to_delete = os.path.join(self.current_scene_dir, os.path.basename(file_to_delete) + '.png')
                    try:
                        if os.path.exists(file_to_delete):
                            os.remove(file_to_delete)
                        if os.path.exists(thumb_to_delete):
                            os.remove(thumb_to_delete)
                    except Exception:
                        pass
                    del self.current_scene_files[selected]
                    self.save_scene_order(self.current_scene_dir, self.current_scene_files)
                    self.show_scene_thumbnails(self.current_scene_dir)
                    # Select the next item if possible
                    if selected < len(self.current_scene_files):
                        self.list_widget.setCurrentRow(selected)
                    elif self.current_scene_files:
                        self.list_widget.setCurrentRow(len(self.current_scene_files)-1)
                    return True
        return super().eventFilter(source, event)
    def setup_scene_dragdrop(self):
        # Enable drag-and-drop reordering for the list_widget
        self.list_widget.setDragDropMode(self.list_widget.InternalMove)
        self.list_widget.model().rowsMoved.connect(self.on_scene_rows_moved)

    def on_scene_rows_moved(self, parent, start, end, dest, dest_row):
        # Update current_scene_files to match new order and save
        new_order = []
        for i in range(self.list_widget.count()):
            name = self.list_widget.item(i).text()
            for f in self.current_scene_files:
                if os.path.basename(f) == name:
                    new_order.append(f)
                    break
        self.current_scene_files = new_order
        self.save_scene_order(self.current_scene_dir, self.current_scene_files)
    def load_scene_order(self, dir_path, scene_files):
        order_file = os.path.join(dir_path, 'scene_order.txt')
        if os.path.exists(order_file):
            with open(order_file, 'r') as f:
                ordered_names = [line.strip() for line in f if line.strip()]
            # Only keep files that exist
            ordered_files = [os.path.join(dir_path, name) for name in ordered_names if os.path.join(dir_path, name) in scene_files]
            # Add any new files not in the order file at the end
            for f in scene_files:
                if f not in ordered_files:
                    ordered_files.append(f)
            return ordered_files
        else:
            # Default: sort by filename
            return sorted(scene_files)

    def save_scene_order(self, dir_path, scene_files):
        order_file = os.path.join(dir_path, 'scene_order.txt')
        with open(order_file, 'w') as f:
            for fpath in scene_files:
                f.write(f'{os.path.basename(fpath)}\n')

    def show_scene_thumbnails(self, dir_path):
        # Show all video files in dir_path as thumbnails in current list_widget, in order from order file if present
        from video_utils import is_video_file
        scene_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if is_video_file(f)]
        scene_files = self.load_scene_order(dir_path, scene_files)
        self.list_widget.clear()
        for f in scene_files:
            thumb_path = os.path.join(dir_path, f'{os.path.basename(f)}.png')
            if os.path.exists(thumb_path):
                pixmap = QPixmap(thumb_path)
            else:
                pixmap = QPixmap()
            item = QListWidgetItem(os.path.basename(f))
            item.setIcon(QIcon(pixmap))
            item.setSizeHint(QSize(THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
            self.list_widget.addItem(item)
        # Store for later use
        self.current_scene_dir = dir_path
        self.current_scene_files = scene_files
        self.setup_scene_dragdrop()

    def __init__(self, start_dir=None):
        super().__init__()
        self.setWindowTitle('vchop - Video Browser')
        self.setGeometry(100, 100, 800, 600)
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setSpacing(10)
        self.list_widget.setStyleSheet('background-color: black;')
        self.setCentralWidget(self.list_widget)
        self.list_widget.itemDoubleClicked.connect(self.open_video_editor)
        self.list_widget.installEventFilter(self)
        self.recent_dirs = load_recent_dirs()
        self.create_menu()
        if start_dir:
            self.open_directory(start_dir)
            self.recent_dirs = update_recent_dirs(start_dir, self.recent_dirs)
        elif self.recent_dirs:
            self.open_directory(self.recent_dirs[0])

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        open_action = QAction('Open Directory', self)
        open_action.triggered.connect(self.select_directory)
        file_menu.addAction(open_action)
        join_action = QAction('Join Scenes from Directory', self)
        join_action.triggered.connect(self.open_scene_manager_from_dir)
        file_menu.addAction(join_action)
        recent_menu = file_menu.addMenu('Recent Directories')
        for dir_path in self.recent_dirs:
            action = QAction(dir_path, self)
            action.triggered.connect(lambda checked, d=dir_path: self.open_directory(d))
            recent_menu.addAction(action)
        actions_menu = menubar.addMenu('Actions')
        split_action = QAction('Split by Scenes', self)
        split_action.triggered.connect(self.split_by_scenes)
        actions_menu.addAction(split_action)

    def open_scene_manager_from_dir(self):
        # Default to subdirectory of current directory if possible
        base_dir = self.recent_dirs[0] if self.recent_dirs else os.getcwd()
        default_dir = os.path.join(base_dir, 'scenes')
        if not os.path.exists(default_dir):
            default_dir = base_dir
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory of Split Scenes', default_dir)
        if not dir_path:
            return
        from video_utils import is_video_file
        scene_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if is_video_file(f)]
        if not scene_files:
            QMessageBox.warning(self, 'No Scenes', 'No video files found in selected directory.')
            return
        self.show_scene_thumbnails(dir_path)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            self.open_directory(dir_path)
            self.recent_dirs = update_recent_dirs(dir_path, self.recent_dirs)

    def open_directory(self, dir_path):
        self.list_widget.clear()
        thumb_dir = os.path.join(dir_path, THUMBNAIL_DIR)
        os.makedirs(thumb_dir, exist_ok=True)
        for filename in os.listdir(dir_path):
            if is_video_file(filename):
                filepath = os.path.join(dir_path, filename)
                thumb_path = os.path.join(thumb_dir, f'{filename}.png')
                if not os.path.exists(thumb_path):
                    try:
                        create_thumbnail(filepath, thumb_path)
                    except Exception:
                        thumb_path = None
                if os.path.exists(thumb_path):
                    pixmap = QPixmap(thumb_path)
                else:
                    pixmap = QPixmap()
                item = QListWidgetItem(filename)
                item.setIcon(QIcon(pixmap))
                item.setSizeHint(QSize(THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
                self.list_widget.addItem(item)

    def open_video_editor(self, item):
        dir_path = self.recent_dirs[0] if self.recent_dirs else None
        if not dir_path:
            QMessageBox.warning(self, 'No Directory', 'No directory found for editing.')
            return
        video_path = os.path.join(dir_path, item.text())
        self.editor = VideoEditorWindow(video_path, self)
        self.editor.show()

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
        video_path = os.path.join(dir_path, filename)
        self.editor = VideoEditorWindow(video_path, self)
        self.editor.show()
